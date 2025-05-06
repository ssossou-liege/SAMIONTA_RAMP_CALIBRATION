from Samionta import LC, MC, HC, CH, SME, PUE_old
from ramp.post_process import post_process as pp
import postprocessing as psp
from ramp import UseCase
import matplotlib.pyplot as plt
import households_clustering as hcl
import os

def run(lc, mc, hc):
    LC.num_users = lc
    MC.num_users = mc
    HC.num_users = hc
    Users = [LC, MC, HC, CH, SME, PUE_old]
    
    start_date = "2024-02-01"
    end_date = "2024-07-31"
    uc = UseCase(
        users=Users,
        parallel_processing=False, 
        date_start=start_date, 
        date_end=end_date
        )

    # Generate and formate load profiles
    Profiles_list = uc.generate_daily_load_profiles(flat=False)    
    Profiles_avg, Profiles_list_kW, Profiles_series = pp.Profile_formatting(Profiles_list)   
    
    # Load, resample and formate historical data
    Hist_list = psp.resample("historical_data.xlsx")
    Hist_profiles_avg, Hist_list_kW, Hist_series = pp.Profile_formatting(Hist_list)
    
    # Plot and match the generated and historical data load profiles
    fig, ax = psp.Profile_cloud_plot(Profiles_list, Profiles_avg, Hist_profiles_avg)
    
    # Calculate validation criterias 
    psp.calculations(Hist_profiles_avg, Profiles_avg)
    
    # Save and show plot    
    os.makedirs('figures', exist_ok=True)
    plt.savefig(os.path.join('figures', 'comparison.png'), dpi=300, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    
    # INITIALISATION
    df = hcl.read_and_filter_customers("historical_data.xlsx")   
    df_with_clusters, wcss = hcl.clustering(df)
    lc, mc, hc = hcl.get_clusters_stats(df_with_clusters)
        
    run(lc, mc, hc)
