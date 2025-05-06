import pandas as pd

def process_excel_data(input_file, output_file):
    """
    Reads an Excel file, processes it, and writes the result to two new Excel files.
    """
    try:
        df = pd.read_excel(input_file)
        df['timestamp'] = pd.to_datetime(df['timestamp']).dt.tz_localize(None)
        df['kilowatt_hours'] = pd.to_numeric(df['kilowatt_hours'].replace(',', '.', regex=True))

        def custom_round_hour(ts):
            minute = ts.minute
            if minute < 59:
                return ts.replace(minute=0, second=0, microsecond=0)
            else:
                return (ts + pd.Timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

        df['hourly_timestamp'] = df['timestamp'].apply(custom_round_hour)

        # Pivot tables
        pivot_df = df.pivot_table(index='timestamp', columns='customer_name', values='kilowatt_hours').reset_index()
        pivot_df.iloc[:, 1:] *= 1000  # Convert to Wh

        # Aggregate data by hour
        df_hourly = df.groupby(['hourly_timestamp', 'customer_name'])['kilowatt_hours'].sum().reset_index()

        hourly_pivot = df_hourly.pivot_table(index='hourly_timestamp', columns='customer_name', values='kilowatt_hours').reset_index()
        hourly_pivot.iloc[:, 1:] *= 1000  # Convert to Wh

        # Average hourly consumption calculations
        unique_hours = df_hourly['hourly_timestamp'].dt.hour.unique()
        unique_hours.sort()

        avg_hourly_data = []
        for hour in unique_hours:
            hour_data = df_hourly[df_hourly['hourly_timestamp'].dt.hour == hour]
            avg_hour = hour_data.groupby('customer_name')['kilowatt_hours'].mean().round(3).reset_index()
            avg_hour['hour'] = hour
            avg_hourly_data.append(avg_hour)

        avg_hourly = pd.concat(avg_hourly_data).pivot(index='hour', columns='customer_name', values='kilowatt_hours').reset_index()
        avg_hourly.iloc[:, 1:] *= 1000  # Convert to Wh
        avg_hourly['hourly_timestamp'] = pd.to_datetime(avg_hourly['hour'], unit='h').dt.time
        avg_hourly = avg_hourly[['hourly_timestamp'] + list(avg_hourly.columns[1:-1])]
        
        # Daily consumption
        df_daily = df_hourly.copy()
        df_daily['daily_timestamp'] = df_daily['hourly_timestamp'].dt.to_period('D').dt.to_timestamp()
        daily_consumption = df_daily.pivot_table(index='daily_timestamp', columns='customer_name', values='kilowatt_hours', aggfunc='sum').reset_index()
        
        # Monthly consumption
        df_monthly = df_hourly.copy()
        df_monthly['monthly_timestamp'] = df_monthly['hourly_timestamp'].dt.to_period('M').dt.to_timestamp()
        monthly_consumption = df_monthly.pivot_table(index='monthly_timestamp', columns='customer_name', values='kilowatt_hours', aggfunc='sum').reset_index()
        
        # Calculate average monthly and daily consumption
        avg_daily_consumption = daily_consumption.mean(numeric_only=True).round(3)
        avg_monthly_consumption = monthly_consumption.mean(numeric_only=True).round(3)
        
        customer_consumption = pd.DataFrame({
            'customer_name': avg_daily_consumption.index,
            'Avg_Monthly_consumption': avg_monthly_consumption.values,
            'Avg_Daily_consumption': avg_daily_consumption.values
        })
        
        # Calculate total monthly consumption for all customers
        total_monthly_consumption = monthly_consumption.set_index('monthly_timestamp').sum(axis=1).reset_index()
        total_monthly_consumption.columns = ['Month', 'Consumption (kWh)']
        total_monthly_consumption['Month'] = total_monthly_consumption['Month'].dt.strftime('%B')
        
        # Output to Excel files
            # Improve the display of dates
        daily_consumption['daily_timestamp'] = pd.to_datetime(daily_consumption['daily_timestamp']).dt.strftime('%Y-%m-%d')
        monthly_consumption['monthly_timestamp'] = pd.to_datetime(monthly_consumption['monthly_timestamp']).dt.strftime('%B %Y')
        with pd.ExcelWriter(output_file) as writer:
            pivot_df.to_excel(writer, sheet_name='15-Minute (Wh)', index=False)
            hourly_pivot.to_excel(writer, sheet_name='Hourly (Wh)', index=False)
            avg_hourly.to_excel(writer, sheet_name='Avg Hourly (Wh)', index=False)
            daily_consumption.to_excel(writer, sheet_name='Daily (kWh)', index=False)
            monthly_consumption.to_excel(writer, sheet_name='Monthly (kWh)', index=False)
            customer_consumption.to_excel(writer, sheet_name='Customer Consumption (kWh)', index=False)
            total_monthly_consumption.to_excel(writer, sheet_name='Total Monthly Consumption (kWh)', index=False)

        print(f"File created: {output_file}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"Error: {e}")

# RUN
def run():
    input_excel_file = 'raw_data.xlsx'
    output_excel_file = 'historical_data.xlsx'
    process_excel_data(input_excel_file, output_excel_file)
    
if __name__ == '__main__':
    run()
