import pandas as pd
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from threadpoolctl import threadpool_limits
from matplotlib.gridspec import GridSpec
import os


def read_and_filter_customers(input_file):
    try:    
        # Read the Excel file        
        df = pd.read_excel(input_file, sheet_name='Customer Consumption (kWh)')      
    
        # Filter customers whose names start with "HH"    
        df_hh = df[df['customer_name'].str.startswith('HH')]      
    
        return df_hh

    except FileNotFoundError:
            print(f"Error: File '{input_file}' not found.")
            return None

    except Exception as e:
        print(f"An error occurred while processing the Excel file: {e}")        
        return None

def clustering (df):
    # Data standardization
    scaler = StandardScaler()
    df['Avg_Daily_consumption_scaled'] = scaler.fit_transform(df[['Avg_Daily_consumption']])
    
    # Elbow method for determining the optimal number of clusters
    wcss = []
    for i in range(1, 11):
        with threadpool_limits(limits=1, user_api='openmp'):    
            kmeans = KMeans(n_clusters=i, random_state=0, n_init="auto")        
            kmeans.fit(df[['Avg_Daily_consumption_scaled']])        
            wcss.append(kmeans.inertia_)

    # K-means implementation with the optimal number of clusters
    optimal_clusters = 3
    with threadpool_limits(limits=1, user_api='openmp'):
        kmeans = KMeans(n_clusters=optimal_clusters, random_state=0)    
        df['Cluster'] = kmeans.fit_predict(df[['Avg_Daily_consumption_scaled']])
    
    return df, wcss

def ploting(df, wcss):
    # Create figures directory if it doesn't exist
    os.makedirs('figures', exist_ok=True)
    
    # Create a figure with 2x2 subplots
    fig = plt.figure(figsize=(20, 16))
    gs = GridSpec(2, 2, figure=fig)
    
    # Top Left: Daily consumption histogram
    ax1 = fig.add_subplot(gs[0, 0])
    sns.histplot(df['Avg_Daily_consumption'], bins=30, kde=True, ax=ax1)
    ax1.set_title('Daily consumption distribution', fontsize=25)
    ax1.set_xlabel('Daily consumption (kWh)', fontsize=22)
    ax1.set_ylabel('Frequency', fontsize=22)
    
    # Top Right: Daily consumption box plot
    ax2 = fig.add_subplot(gs[0, 1])
    sns.boxplot(x=df['Avg_Daily_consumption'], ax=ax2)
    ax2.set_title('Daily consumption box plot', fontsize=25)
    ax2.set_xlabel('Daily consumption (kWh)', fontsize=22)
    
    # Bottom Left: Elbow plot
    ax3 = fig.add_subplot(gs[1, 0])
    ax3.plot(range(1, 11), wcss, marker='o')
    ax3.set_title('Elbow method', fontsize=25)
    ax3.set_xlabel('Number of clusters', fontsize=22)
    ax3.set_ylabel('WCSS', fontsize=22)
    
    # Bottom Right: Clusters visualization
    ax4 = fig.add_subplot(gs[1, 1])
    for cluster_num in df['Cluster'].unique():
        cluster_data = df[df['Cluster'] == cluster_num]    
        ax4.scatter(cluster_data['customer_name'], 
                   cluster_data['Avg_Daily_consumption'], 
                   label=f'Cluster {cluster_num}', 
                   s=100, edgecolors='black', linewidths=1)
    
    ax4.set_title('Households connections clustering with k-means', fontsize=23)
    ax4.set_xlabel('Household', fontsize=22)
    ax4.set_ylabel('Daily consumption (kWh)', fontsize=22)
    ax4.tick_params(axis='x', rotation=90)
    ax4.legend()
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure first
    plt.savefig(os.path.join('figures', 'clustering.png'), dpi=300, bbox_inches='tight')
    
    # Then show it
    plt.show()
    
    # Close the figure to free memory
    plt.close(fig)

def get_clusters_stats(df):
    # Calculate and print cluster statistics
    cluster_stats = df.groupby('Cluster')['Avg_Daily_consumption'].agg(['min', 'max', 'mean', 'count'])
    print("\nCluster Consumption Ranges:")
    print(cluster_stats)
    
    # Calculates lc_count, mc_count, and hc_count from the cluster statistics
    sorted_cluster_stats = cluster_stats.sort_values(by='mean')
    lc_count = int(sorted_cluster_stats.iloc[0]['count'])
    mc_count = int(sorted_cluster_stats.iloc[1]['count'])
    hc_count = int(sorted_cluster_stats.iloc[2]['count'])
    
    return lc_count, mc_count, hc_count

def run():
    # Excel File reading and preprocessing
    input_file = 'historical_data.xlsx'
    df = read_and_filter_customers(input_file)   
    df_with_clusters, wcss = clustering(df)    
    ploting(df_with_clusters, wcss)
    
    lc, mc, hc = get_clusters_stats(df_with_clusters)
    print(f"\nLow consumption households: {lc}")
    print(f"Medium consumption households: {mc}")
    print(f"High consumption households: {hc}")
    
    return lc, mc, hc

if __name__ == "__main__":
    run()