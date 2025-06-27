import pandas as pd

def parse_time_str(t_str):
    # Parses "MM:SS.s" to total seconds as float
    parts = t_str.split(':')
    minutes = int(parts[0])
    seconds = float(parts[1])
    return minutes * 60 + seconds

def load_and_filter_ualf_files(time_frame, cloud_indicator_filter=[0,1]):
    """
    Load UALF fixed-width files 50.txt-59.txt, filter by CloudIndicator,
    then filter by time frame (MM:SS.s), and sort by Minute, Second, Nanosecond.

    Args:
        folder_path (str): Directory containing files named '50.txt' to '59.txt'
        time_frame (list[str]): ["MM:SS.s", "MM:SS.s"] start and end of filter time
        cloud_indicator_filter (int): 0 or 1 to filter CloudIndicator

    Returns:
        pd.DataFrame: filtered and sorted DataFrame
    """
    field_widths = [4] * 30
    column_names = [
        'RecordType', 'NetworkType', 'Year', 'Month', 'Day',
        'Hour', 'Minute', 'Second', 'Nanosecond',
        'Latitude', 'Longitude', 'Altitude', 'AltitudeUncertainty', 'Current',
        'RangePower', 'Multiplicity', 'CloudPulseCount',
        'SensorCount', 'DegreesFreedom', 'ErrorEllipseAngle', 'ErrorEllipseMajorAxis',
        'ErrorEllipseMinorAxis', 'ChiSquared', 'RiseTime', 'PeakToZeroTime',
        'MaxRateOfRise', 'CloudIndicator', 'AngleIndicator', 'SignalIndicator',
        'TimingIndicator'
    ]

    # Parse time frame boundaries to seconds
    start_sec = parse_time_str(time_frame[0])
    end_sec = parse_time_str(time_frame[1])

    df_list = []
    for minute in range(50, 60):
        filename = f"info_storage/{minute}.txt"
        try:
            df = pd.read_csv(filename, sep='\t', header=None, names=column_names)
        except FileNotFoundError:
            print(f"File not found: {filename}, skipping.")
            continue

        # Convert necessary columns to numeric
        df['CloudIndicator'] = pd.to_numeric(df['CloudIndicator'], errors='coerce').fillna(-1).astype(int)
        df['Minute'] = pd.to_numeric(df['Minute'], errors='coerce').fillna(-1).astype(int)
        df['Second'] = pd.to_numeric(df['Second'], errors='coerce').fillna(-1).astype(int)
        df['Nanosecond'] = pd.to_numeric(df['Nanosecond'], errors='coerce').fillna(0).astype(int)

        if cloud_indicator_filter is not None:
            if isinstance(cloud_indicator_filter, (list, set, tuple)):
                df = df[df['CloudIndicator'].isin(cloud_indicator_filter)]
            else:
                df = df[df['CloudIndicator'] == cloud_indicator_filter]


        # Calculate time in seconds for each row: total = Minute*60 + Second + Nanosecond/1e9
        df['TimeSeconds'] = df['Minute'] * 60 + df['Second'] + df['Nanosecond'] / 1_000_000_000

        # Filter rows that fall inside the time frame range
        df = df[(df['TimeSeconds'] >= start_sec) & (df['TimeSeconds'] <= end_sec)]

        df_list.append(df)

    if not df_list:
        print("No data loaded or matched filter.")
        return pd.DataFrame()

    combined_df = pd.concat(df_list, ignore_index=True)

    # Sort by Minute, Second, Nanosecond
    combined_df_sorted = combined_df.sort_values(by=['Minute', 'Second', 'Nanosecond']).reset_index(drop=True)


  

    # 1. Make sure all time-related columns are numeric
    for col in ["Year", "Month", "Day", "Hour", "Minute", "Second", "Nanosecond"]:
        combined_df_sorted[col] = pd.to_numeric(combined_df_sorted[col], errors='coerce').astype("Int64")

    # 2. Create a base timestamp (accurate to seconds)
    combined_df_sorted["Timestamp"] = pd.to_datetime({
        "year": combined_df_sorted["Year"],
        "month": combined_df_sorted["Month"],
        "day": combined_df_sorted["Day"],
        "hour": combined_df_sorted["Hour"],
        "minute": combined_df_sorted["Minute"],
        "second": combined_df_sorted["Second"]
    }, errors='coerce')

    # 3. Add nanosecond precision as timedelta
    combined_df_sorted["Timestamp"] += pd.to_timedelta(combined_df_sorted["Nanosecond"], unit='ns')
    combined_df_sorted["TimeStr"] = combined_df_sorted["Timestamp"].dt.strftime("%H:%M:%S.%f")
    # 4. Optional: display or use the timestamp
    print(combined_df_sorted[["Timestamp", "Minute", "Second", "Nanosecond"]].head())


    combined_df_sorted["Minute"] = pd.to_numeric(combined_df_sorted["Minute"], errors='coerce')
    combined_df_sorted["Second"] = pd.to_numeric(combined_df_sorted["Second"], errors='coerce')
    combined_df_sorted["Nanosecond"] = pd.to_numeric(combined_df_sorted["Nanosecond"], errors='coerce')
    combined_df_sorted = combined_df_sorted.dropna(subset=["Minute", "Second", "Nanosecond"])
    combined_df_sorted["TotalTimeMinutes"] = combined_df_sorted["Minute"] + (combined_df_sorted["Second"] + combined_df_sorted["Nanosecond"] / 1e9)/60

    return combined_df_sorted
