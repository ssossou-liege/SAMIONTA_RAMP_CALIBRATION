import pandas as pd
import matplotlib.pyplot as plt
import os

def plot_histogram(file_path):
    """Load and clean monthly consumption data from Excel"""
    data = pd.read_excel(file_path, sheet_name="Total Monthly Consumption (kWh)")
    
    # Convert consumption to numeric - handles both string and numeric inputs
    if pd.api.types.is_string_dtype(data['Consumption (kWh)']):
        data['Consumption (kWh)'] = data['Consumption (kWh)'].str.replace(',', '').astype(float)
    else:
        data['Consumption (kWh)'] = data['Consumption (kWh)'].astype(float)
    
    """Create 2D plot with 3D-style cube bars"""
    plt.rcParams.update({"font.size": 20})
    # Create figures directory if it doesn't exist
    os.makedirs('figures', exist_ok=True)
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Colors
    face_color = '#4285F4'  # Blue
    edge_color = '#3367D6'  # Darker blue for edges
    top_color = '#669DF6'   # Lighter blue for top
    
    # Plot each bar as a 3D-looking cube
    for i, (month, value) in enumerate(zip(data['Month'], data['Consumption (kWh)'])):
        # Main bar
        ax.bar(i, value, width=0.6, color=face_color, edgecolor=edge_color, linewidth=1.5)
        
        # Add 3D effect (top and side)
        x = i - 0.3
        w = 0.6
        h = value
        
        # Top face
        ax.plot([x, x+w], [h, h], color=top_color, linewidth=2)
        ax.plot([x, x], [h-0.01*h, h], color=top_color, alpha=0.7)
        ax.plot([x+w, x+w], [h-0.01*h, h], color=top_color, alpha=0.7)
        
        # Right face
        ax.plot([x+w, x+w+0.03], [0, 0], color=edge_color, alpha=0.5)
        ax.plot([x+w, x+w+0.03], [h, h], color=edge_color, alpha=0.5)
        ax.plot([x+w+0.03, x+w+0.03], [0, h], color=edge_color, alpha=0.3)
    
    # Customize axes
    ax.set_xticks(range(len(data['Month'])))
    ax.set_xticklabels(data['Month'], ha='center')
    
    # Add value labels
    for i, val in enumerate(data['Consumption (kWh)']):
        ax.text(i, val + (data['Consumption (kWh)'].max() * 0.05), 
                f'{val:,.0f}', ha='center', va='bottom')
    
    # Styling
    ax.set_title('Monthly Energy Consumption Trend (2024)', fontweight='bold', pad=20, fontsize=24)
    ax.set_xlabel('Month', labelpad=10, fontsize=22, ha='right')
    ax.set_ylabel('Consumption (kWh)', labelpad=10, fontsize=22)
    ax.grid(axis='y', linestyle='--', alpha=0.7)
    ax.set_ylim(0, data['Consumption (kWh)'].max() * 1.15)
    
    # Remove top and right spines
    for spine in ['top', 'right']:
        ax.spines[spine].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(os.path.join('figures', 'demand_trend.png'), dpi=300, bbox_inches='tight')
    plt.show()

def run():
    monthly_data = 'historical_data.xlsx'    
    plot_histogram(monthly_data)
    
if __name__ == "__main__":
    run()