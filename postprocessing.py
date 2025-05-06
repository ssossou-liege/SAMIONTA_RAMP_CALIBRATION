import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import seaborn as sns

def resample(historical_path: str) -> np.ndarray:
            # Load the Excel file
    df = pd.read_excel(historical_path, sheet_name='15-Minute (Wh)')
            # Convert timestamp to datetime and set as index
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
            # Compute total energy consumption (Wh) across all consumers
    df['total_Wh'] = df.sum(axis=1, skipna=True)    
            # Convert Wh/15min to average power in W over 15 minutes
    df['power_W'] = df['total_Wh'] * 4  # 1 Wh per 15min = 4 W
            # Expand each 15-minute power value into 15 one-minute values
    power_minute_records = []
    timestamps = df.index
    powers = df['power_W'].values

    for i in range(len(timestamps) - 1):
        start_time = timestamps[i]
        start_power = powers[i]
        end_time = timestamps[i+1]
        end_power = powers[i+1]
        duration_minutes = (end_time - start_time).total_seconds() / 60
        if duration_minutes > 1:
            # Create a time range at 1-minute resolution
            minute_range = pd.date_range(start=start_time, end=end_time, freq='1Min', inclusive='left')
            num_points = len(minute_range)
            if num_points > 0:
                # Perform linear interpolation
                interpolated_powers = np.linspace(start_power, end_power, num_points)
                power_minute_records.extend(zip(minute_range, interpolated_powers))
        elif duration_minutes == 1:
            power_minute_records.append((start_time, start_power))

    # Add the last data point
    if timestamps.size > 0:
        power_minute_records.append((timestamps[-1], powers[-1]))    
            # Rebuild the 1-minute resolution time series
    power_per_minute = pd.Series(
        data=[val for _, val in power_minute_records],
        index=[ts for ts, _ in power_minute_records]
                                )    
            # Group by day and identify incomplete days
    daily_power = power_per_minute.groupby(power_per_minute.index.normalize())    
            # Construct the final numpy array, including only complete days (1440 values)
    daily_array = np.vstack([
        group.values[:1440] for _, group in daily_power if len(group) == 1440
    ])

    return daily_array

def Profile_cloud_plot(stoch_profiles, stoch_profiles_avg, hist_profiles_avg=None, figsize=(16, 8)):
    plt.rcParams.update({"font.size": 22})
    fig, ax = plt.subplots(figsize=figsize)
    first_profile = True
    label_single = "Single days"
    label_average = "Daily average"
    if hist_profiles_avg is not None:
        label_single = "RAMP daily generated"
        label_average = "RAMP average"
    for n in stoch_profiles:
        if first_profile:
            ax.plot(np.arange(1440), n, "#D3D3D3", label=label_single)
            first_profile = False
        else:
            ax.plot(np.arange(1440), n, "#b0c4de")
    ax.plot(np.arange(1440), stoch_profiles_avg, "#4169e1", lw=5, label=label_average)
    if hist_profiles_avg is not None:
        ax.plot(np.arange(1440), hist_profiles_avg, "#228B22", lw=5, label="Historical data average")
    ax.set_xlabel("Time (hours)")
    ax.set_ylabel("Power (W)", fontsize="large", labelpad=20)
    ax.set_ylim(ymin=0)
    ax.margins(x=0)
    ax.margins(y=0)
    ax.set_xticks([0, 240, 480, (60 * 12), (60 * 16), (60 * 20), (60 * 24)])
    ax.set_xticklabels([0, 4, 8, 12, 16, 20, 24])
    ax.legend(framealpha=0.1)
    plt.title("Load profiles")
    return fig, ax

def Profile_series_plot(stoch_profiles_series, start_date, figsize=(16, 8)):
    start_date = pd.to_datetime(start_date)
    time_index = pd.date_range(start=start_date, periods=len(stoch_profiles_series), freq="1Min")
    profiles_series = pd.Series(stoch_profiles_series, index=time_index)
    plt.rcParams.update({"font.size": 22})
    fig, ax = plt.subplots(figsize=figsize)
    month_fmt = mdates.DateFormatter('%B')
    ax.plot(profiles_series.index, profiles_series.values, "#4169e1")
    ax.set_ylabel("Power (W)", fontsize="large")
    ax.set_ylim(ymin=0)
    ax.margins(x=0)
    ax.margins(y=0)
    ax.xaxis.set_major_formatter(month_fmt)
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    plt.xlabel("Month", fontsize="large", labelpad=20)
    plt.title("Time series")
    plt.xticks(ha='left')
    plt.tight_layout()
    plt.title("Time series")
    return fig, ax

def calculations(hist_data, ramp_data):   
    #------------NMRSE calculation--------------------------------------
    """
    Trim the first and last 30 minutes of the daily data to 
    mitigate the RAMP limitation at those edges
    """
    hist_data_trim = hist_data[30:-30]
    ramp_data_trim = ramp_data[30:-30]
    MSE = np.mean((hist_data_trim - ramp_data_trim)**2)
    RMSE = np.sqrt(MSE)
    NRMSE = RMSE / np.mean(hist_data_trim)
    
    #-----------Peak Load calutation-----------------------------------
    peak_hist = hist_data.max()     # W
    peak_ramp = ramp_data.max()     # W
                    # ERROR
    error_peak =  abs((peak_ramp - peak_hist)/peak_hist)
    
    #--------Load factor calculation-----------------------------------
    LF_hist = np.mean(hist_data)/peak_hist
    LF_ramp = np.mean(ramp_data)/peak_ramp
                    # ERROR
    error_LF =  abs((LF_ramp - LF_hist)/LF_hist)
    
    #--------Daily average demand-------------------------------------
    demand_hist = (np.sum(hist_data))/60    # Wh
    demand_ramp = (np.sum(ramp_data))/60    # Wh
                # ERROR
    error_demand =  abs((demand_ramp - demand_hist)/demand_hist)
    
    #--------Results printing----------------------------------------
    print("\nRESULTS")    
    col1 = 22
    col2 = 20
    col3 = 12
    col4 = 10    
    print(f"{' ':<{col1}}{'Historical data':<{col2}}{'Ramp data':<{col3}}{'Error':<{col4}}")
    print("-" * (col1 + col2 + col3 + col4))    
    print(f"{'Peak load (kW)':<{col1}}{peak_hist/1000:<{col2}.2f}{peak_ramp/1000:<{col3}.2f}{error_peak:<{col4}.2%}")
    print(f"{'Load Factor':<{col1}}{LF_hist:<{col2}.2%}{LF_ramp:<{col3}.2%}{error_LF:<{col4}.2%}")
    print(f"{'Average demand (kWh)':<{col1}}{demand_hist/1000:<{col2}.2f}{demand_ramp/1000:<{col3}.2f}{error_demand:<{col4}.2%}")
    print(f"{'NRMSE':<{col1}}{' ':<{col2}}{NRMSE:<{col3}.2%}{' ':<{col4}}")
    
def plot_scenario_results(results, horizon, save=False, filename=None):
    """
    Plots the consumption stacked bars for each scenario.    
     """ 
    # Extract scenario names and consumption data
    scenarios = list(results.keys())
    households = [data[0] for data in results.values()]
    sme = [data[1] for data in results.values()]
    public = [data[2] for data in results.values()]

    # Calculate the total energy consumption for each scenario
    totals = [h + s + p for h, s, p in zip(households, sme, public)]

    # Configure figure and axes parameters
    plt.rcParams.update({"font.size": 20})
    sns.set_style("whitegrid")
    fig, ax = plt.subplots(figsize=(5, 7))
    bar_width = 0.3
    positions = np.arange(len(scenarios))

    # Create stacked bar chart with hatching for visual differentiation
    ax.bar(positions, households, color='#FFA07A', width=bar_width, label='Households', hatch='//', edgecolor='black', zorder=3)
    ax.bar(positions, sme, bottom=households, color='#20B2AA', width=bar_width, label='SME', hatch='//', edgecolor='black', zorder=3)
    ax.bar(positions, public, bottom=np.array(households) + np.array(sme),
                    color='#778899', width=bar_width, label='Community services', hatch='//', edgecolor='black', zorder=3)

    # Annotate bars with percentage contribution of each sector to the total consumption
    for i in range(len(scenarios)):
        ax.text(positions[i], households[i] / 2, f'{(households[i] / totals[i]) * 100:.1f}%', ha='center', va='center', fontsize=11, color='white', fontweight='bold')
        ax.text(positions[i], households[i] + sme[i] / 2, f'{(sme[i] / totals[i]) * 100:.1f}%', ha='center', va='center', fontsize=11, color='white', fontweight='bold')
        ax.text(positions[i], totals[i] - public[i] / 2, f'{(public[i] / totals[i]) * 100:.1f}%', ha='center', va='center', fontsize=11, color='white', fontweight='bold')

    # Annotate bars with total consumption values
    for i in range(len(scenarios)):
        ax.text(positions[i], totals[i] + 0.25, f'{totals[i]:.2f}', ha='center', fontsize=12, fontweight='bold')

    # Customize axes labels, ticks, and title
    ax.set_xticks(positions)
    ax.set_xticklabels(scenarios, fontsize=12)
    ax.set_ylabel('Yearly consumption (MWh)', fontsize=12, fontweight='bold')
    ax.set_xlabel('Categories', fontsize=12, fontweight='bold')
    ax.set_title(f'Archetypes ({horizon})', fontsize=14, fontweight='bold')

    # Display legend
    ax.legend(fontsize=10, loc='lower center')

    # Apply visual enhancements: background color, grid, and spine removal
    ax.set_facecolor('#EAEAF2')  # Light gray background
    plt.gcf().set_facecolor('white')  # Figure background

    # Remove ticks and adjust tick label size
    ax.tick_params(axis='both', which='both', length=0)
    ax.tick_params(axis='y', labelsize=10)

    # Add grid lines
    ax.grid(axis='y', color='white', linestyle='--', linewidth=0.7, zorder=0)
    ax.grid(axis='x', color='white', linestyle='-', linewidth=1.2, zorder=0)

    # Remove spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    if save and filename:
        plt.savefig(filename, bbox_inches='tight')
        plt.close(fig)
    else:
        return fig
    
    # Display the plot
    plt.show()

def plot_scenario_profiles(profiles, horizon, save=False, filename=None):
    """
    Cloud plots load profiles for each scenario.    
     """ 
    plt.rcParams.update({"font.size": 14})
    figs = []
    for scenario_name, profiles_list in profiles.items():       
        profile_series = np.array([])
        profile_avg = np.zeros(1440)
        for profile in profiles_list:
            profile_series = np.append(profile_series, profile)
            profile_avg = profile_avg + profile
        
        Peak= profile_series.max()/1000 # kW
        
        # Plot daily average load profile
        profile_avg = profile_avg / len(profiles_list)
        fig_lp, ax_lp = plt.subplots(figsize=(10, 5))
        
        for n in profiles_list:
            ax_lp.plot(np.arange(1440), n, '#b0c4de')
        ax_lp.plot(np.arange(1440), profile_avg, "#4169e1")
        ax_lp.set_xlabel('Time (hours)')
        ax_lp.set_ylabel("Power (W)")
        ax_lp.set_ylim(ymin=0)
        ax_lp.margins(x=0)
        ax_lp.margins(y=0)
        ax_lp.set_xticks([0, (2 * 60), (4 * 60), (6 * 60), (8 * 60), (10 * 60), (60 * 12), (14 * 60), (60 * 16),
                         (18 * 60), (60 * 20), (22 * 60), (60 * 24)],
                        [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24])
        ax_lp.set_title(f"Load profile ({scenario_name}) {horizon}", fontsize=16, fontweight='bold')
        daily_average_consumption = (profile_avg / (60 * 1000)).sum()
        ax_lp.text(-0.35, max(profile_avg) * 1.01, f'Daily average consumption: {round(daily_average_consumption, 2)} kWh',
                    ha='left', va='top', fontsize=12, fontweight='bold', color='darkblue')
        ax_lp.text(-0.35, max(profile_series)*1.02, f'Peak: {round(Peak, 2)} kW', 
             ha='left', va='top', fontsize=12, fontweight='bold', color='darkblue')
        figs.append(fig_lp)
        if save and f"{filename}_lp":
            plt.savefig(f"{filename}_lp", bbox_inches='tight')
            plt.close(fig_lp)
    plt.show()
    if not save:
        return figs
    