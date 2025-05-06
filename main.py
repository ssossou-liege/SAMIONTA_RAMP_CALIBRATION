import subprocess

def run_script(script_name):
    """
    Executes a given Python script using subprocess.

    Args:
        script_name (str): The name of the Python script file.
    """
    try:
        if script_name == 'raw_data_preprocessing.py':
            print("\nProcessing hitorical data collected from smartmeters...")
        elif script_name == 'consumption_trend.py':
            print("\nCalculating consumption trends over the months...")
        elif script_name == 'households_clustering.py':
            print("\nProceeding to households clustering...")
        elif script_name == 'load_profiles_matching.py':
            print("\nMatching RAMP generated profiles with historical data...")
        elif script_name == 'scenarios_simulation.py':
            print("\nSimulating electricity demand scenarios...")
        process = subprocess.run(['python', script_name], capture_output=True, text=True, check=True)
        if process.stdout:
            print(f"Result:\n{process.stdout}")
        if process.stderr:
            print(f"\n{process.stderr}")
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}: {e}")
        if e.stdout:
            print(f"Stdout from {script_name} (error):\n{e.stdout}")
        if e.stderr:
            print(f"Stderr from {script_name} (error):\n{e.stderr}")
    except FileNotFoundError:
        print(f"Error: Script '{script_name}' not found in the current directory.")
    except Exception as e:
        print(f"An unexpected error occurred while running {script_name}: {e}")

if __name__ == "__main__":
    scripts_to_run = [
        'raw_data_preprocessing.py',
        'consumption_trend.py',
        'households_clustering.py',
        'load_profiles_matching.py',
        'scenarios_simulation.py'
    ]

    print("\nStarting Samionta electricity demand simulation...")
    for script in scripts_to_run:
        run_script(script)
    print("Simulation completed.")