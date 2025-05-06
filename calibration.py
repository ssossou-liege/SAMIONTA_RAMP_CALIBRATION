import raw_data_preprocessing
import consumption_trend
import households_clustering
import load_profiles_matching
'''
This script orchestrates the Samionta electricity demand simulation by sequentially
importing and executing modules for raw data preprocessing, consumption trend analysis,
household clustering, load profile matching, and different scenarios simulation.
'''

if __name__ == '__main__':
    print("\nStarting Samionta electricity demand simulation...")
    
    print("\nProcessing hitorical data collected from smartmeters...")
    raw_data_preprocessing.run()
    
    print("\nCalculating consumption trends over the months...")
    consumption_trend.run()
    
    print("\nProceeding to households clustering...")
    lc, mc, hc = households_clustering.run()
    
    print("\nMatching RAMP generated profiles with historical data...")
    load_profiles_matching.run(lc, mc, hc)