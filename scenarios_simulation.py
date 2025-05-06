from ramp import UseCase
import postprocessing as psp
import matplotlib.pyplot as plt
from Samionta import LC, MC, HC, CH, SME, PUE_old, PUE, SCH, HOS, SC, PL
import warnings
import os, io
from PIL import Image

warnings.filterwarnings(
    "ignore",
    message="The app Grain mill has duty cycle option on.*",
    category=UserWarning,
    module="ramp.core.core"
)

def scenario_simulator(horizon):
    results = {}
    profiles = {}
    if '1-year' in horizon:
        LC.num_users = 20
        MC.num_users = 20
        HC.num_users = 10
        
        # GENERATE PROFILES
        # SCENARIO 1
        print('\nScenario 1')
        print('\tFor Households...')
        uc_hh = UseCase(users=[LC, MC, HC], parallel_processing=False,
                         date_start="2024-01-01",
                         date_end="2024-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)        
        print('\tFor Small and medium enterprises...')
        uc_sme1 = UseCase(users=[SME, PUE_old], parallel_processing=False,
                         date_start="2024-01-01",
                         date_end="2024-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)        
        print('\tFor Community services...')
        uc_public = UseCase(users=[PL, SC, CH], parallel_processing=False,
                         date_start="2024-01-01",
                         date_end="2024-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)
        
        # SCENARIO 2
        print('\nScenario 2')
        print('\tAdding new PUEs...')
        uc_sme2 = UseCase(users=[SME, PUE_old, PUE], parallel_processing=False,
                         date_start="2024-01-01",
                         date_end="2024-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)        
        
        profiles_hh = uc_hh.generate_daily_load_profiles(flat=False)        
        profiles_sme1 = uc_sme1.generate_daily_load_profiles(flat=False)
        profiles_sme2 = uc_sme2.generate_daily_load_profiles(flat=False)        
        profiles_public = uc_public.generate_daily_load_profiles(flat=False)
        
        # CALCULATE CONSUMPTION PER CATEGORY
        consumption_hh = (sum(profile.sum() for profile in profiles_hh)) / 6e7  # Convert W-minute to MWh
        consumption_sme1 = (sum(profile.sum() for profile in profiles_sme1)) / 6e7  
        consumption_sme2 = (sum(profile.sum() for profile in profiles_sme2)) / 6e7 
        consumption_public = (sum(profile.sum() for profile in profiles_public)) / 6e7   
        
        # OUTPUT
        results['Scenario 1'] = [consumption_hh, consumption_sme1, consumption_public]
        results['Scenario 2'] = [consumption_hh, consumption_sme2, consumption_public]
        
        profiles['Scenario 1'] = profiles_hh + profiles_sme1 + profiles_public
        profiles['Scenario 2'] = profiles_hh + profiles_sme2 + profiles_public
        
        return results, profiles
    
    elif '5-year' in horizon:
        LC.num_users = 64
        MC.num_users = 64
        HC.num_users = 32
        
        # GENRATE PROFILES
        # SCENARIO 1
        print('\nScenario 1')
        print('\tFor Households...')
        uc_hh = UseCase(users=[LC, MC, HC], parallel_processing=False,
                         date_start="2029-01-01",
                         date_end="2029-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)
        print('\tFor Small and medium enterprises...')
        uc_sme = UseCase(users=[SME, PUE_old, PUE], parallel_processing=False,
                         date_start="2029-01-01",
                         date_end="2029-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)
        print('\tFor Community services...')
        uc_public1 = UseCase(users=[PL, SC, CH], parallel_processing=False,
                         date_start="2029-01-01",
                         date_end="2029-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)
        
        # SCENARIO 2
        print('\nScenario 2')
        print('\tAdding the School...')
        uc_public2 = UseCase(users=[PL, SC, CH, SCH], parallel_processing=False,
                         date_start="2029-01-01",
                         date_end="2029-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)
        
        # SCENARIO 3
        print('\nScenario 3')
        print('\tAdding the Health Center...')
        uc_public3 = UseCase(users=[PL, SC, CH, SCH, HOS], parallel_processing=False,
                         date_start="2029-01-01",
                         date_end="2029-12-31",                             
                         peak_enlarge=0.15, random_seed=20240201)
               
        profiles_hh = uc_hh.generate_daily_load_profiles(flat=False)
        profiles_sme = uc_sme.generate_daily_load_profiles(flat=False)        
        profiles_public1 = uc_public1.generate_daily_load_profiles(flat=False)        
        profiles_public2 = uc_public2.generate_daily_load_profiles(flat=False)        
        profiles_public3 = uc_public3.generate_daily_load_profiles(flat=False)
        
        # CALCULATE CONSUMPTION PER CATEGORY
        consumption_hh = (sum(profile.sum() for profile in profiles_hh)) / 6e7  # Convert W-minute to MWh
        consumption_sme = (sum(profile.sum() for profile in profiles_sme)) / 6e7 
        consumption_public1 = (sum(profile.sum() for profile in profiles_public1)) / 6e7   
        consumption_public2 = (sum(profile.sum() for profile in profiles_public2)) / 6e7
        consumption_public3 = (sum(profile.sum() for profile in profiles_public3)) / 6e7
        
        # OUTPUT
        results['Scenario 1'] = [consumption_hh, consumption_sme, consumption_public1]
        results['Scenario 2'] = [consumption_hh, consumption_sme, consumption_public2]
        results['Scenario 3'] = [consumption_hh, consumption_sme, consumption_public3]
        
        profiles['Scenario 1'] = profiles_hh + profiles_sme + profiles_public1
        profiles['Scenario 2'] = profiles_hh + profiles_sme + profiles_public2
        profiles['Scenario 3'] = profiles_hh + profiles_sme + profiles_public3
        
        return results, profiles
    
def run():
    figures_dir = "figures"
    os.makedirs(figures_dir, exist_ok=True)

    # --- 1-year horizon ---
    horizon = '1-year horizon'
    print("\nProcessing 1-year horizon...")
    results_1yr, profiles_1yr = scenario_simulator(horizon)
    fig_archetype_1yr = psp.plot_scenario_results(results_1yr, horizon, save=False)
    figs_profiles_1yr = psp.plot_scenario_profiles(profiles_1yr, horizon, save=False)
    
    # Combine and save the figures
    if fig_archetype_1yr and len(figs_profiles_1yr) >= 2:
        images_1yr = [fig_archetype_1yr] + figs_profiles_1yr[:2]
        widths_1yr, heights_1yr = zip(*(fig.get_size_inches() * fig.dpi for fig in images_1yr))
        total_width_1yr = sum(widths_1yr)
        max_height_1yr = max(heights_1yr)

        combined_image_1yr = Image.new('RGB', (int(total_width_1yr), int(max_height_1yr)), color='white')
        x_offset_1yr = 0
        rightmost_pixel_1yr = 0
        for fig, width in zip(images_1yr, widths_1yr):
            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, format='png', bbox_inches='tight')
            img_bytes.seek(0)
            pil_img = Image.open(img_bytes)
            combined_image_1yr.paste(pil_img, (int(x_offset_1yr), int((max_height_1yr - pil_img.height) / 2)))
            rightmost_pixel_1yr = max(rightmost_pixel_1yr, int(x_offset_1yr + pil_img.width))
            x_offset_1yr += pil_img.width

        # Crop the combined image
        cropped_image_1yr = combined_image_1yr.crop((0, 0, rightmost_pixel_1yr, max_height_1yr))
        cropped_image_1yr.save(os.path.join(figures_dir, "horizon_1.png"))
        plt.close('all') # Close individual figures
        
    # --- 5-year horizon ---
    horizon = '5-year horizon'
    print("\nProcessing 5-year horizon...")
    results_5yr, profiles_5yr = scenario_simulator(horizon)
    fig_archetype_5yr = psp.plot_scenario_results(results_5yr, horizon, save=False)
    figs_profiles_5yr = psp.plot_scenario_profiles(profiles_5yr, horizon, save=False)
    
    # Combine and save the figures
    if fig_archetype_5yr and len(figs_profiles_5yr) >= 3:
        images_5yr = [fig_archetype_5yr] + figs_profiles_5yr[:3]
        widths_5yr, heights_5yr = zip(*(fig.get_size_inches() * fig.dpi for fig in images_5yr))
        total_width_5yr = sum(widths_5yr)
        max_height_5yr = max(heights_5yr)

        combined_image_5yr = Image.new('RGB', (int(total_width_5yr), int(max_height_5yr)), color='white')
        x_offset_5yr = 0
        rightmost_pixel_5yr = 0
        for fig, width in zip(images_5yr, widths_5yr):
            img_bytes = io.BytesIO()
            fig.savefig(img_bytes, format='png', bbox_inches='tight')
            img_bytes.seek(0)
            pil_img = Image.open(img_bytes)
            combined_image_5yr.paste(pil_img, (int(x_offset_5yr), int((max_height_5yr - pil_img.height) / 2)))
            rightmost_pixel_5yr = max(rightmost_pixel_5yr, int(x_offset_5yr + pil_img.width))
            x_offset_5yr += pil_img.width

        # Crop the combined image
        cropped_image_5yr = combined_image_5yr.crop((0, 0, rightmost_pixel_5yr, max_height_5yr))
        cropped_image_5yr.save(os.path.join(figures_dir, "horizon_5.png"))
        plt.close('all') # Close individual figures
        
    print(f"\nThe graphs are saved in '{figures_dir}'.")

# RUN
if __name__ == "__main__":
    run()