import pandas as pd

def filter_and_sort_csv(file_path: str, hour_col: str, minute_col: str, second_col: str, 
                        millisecond_col: str, start_time: str, end_time: str, ascending: bool = True):
    """
    Reads a CSV file, corrects time formatting issues, filters rows within a time range, and sorts them.

    :param file_path: Path to the CSV file.
    :param hour_col: Name of the column containing hours (with .0).
    :param minute_col: Name of the column containing minutes (with .0).
    :param second_col: Name of the column containing seconds (with .0).
    :param millisecond_col: Name of the column containing fractional seconds (e.g., 0.1924).
    :param start_time: Start time in "HH:MM:SS.sss" format.
    :param end_time: End time in "HH:MM:SS.sss" format.
    :param ascending: Sort order (True for earliest first, False for latest first).
    :return: A filtered and sorted Pandas DataFrame.
    """
    # Read CSV file
    df = pd.read_csv(file_path)

    # Convert hour, minute, and second columns to integers (removes .0)
    df[hour_col] = df[hour_col].astype(int)
    df[minute_col] = df[minute_col].astype(int)
    df[second_col] = df[second_col].astype(int)

    # Convert "millisecond" column (which is actually fractional seconds) to real milliseconds
    df[millisecond_col] = (df[millisecond_col] * 1000).round().astype(int)

    # 🔹 Handle Negative Seconds (Borrowing) 🔹
    negative_seconds = df[df[second_col] < 0]
    if not negative_seconds.empty:
        df.loc[df[second_col] < 0, minute_col] -= 1  # Subtract 1 from minutes
        df.loc[df[second_col] < 0, second_col] += 60  # Add 60 seconds to balance

    # 🔹 Handle Negative Minutes (Borrowing) 🔹
    negative_minutes = df[df[minute_col] < 0]
    if not negative_minutes.empty:
        df.loc[df[minute_col] < 0, hour_col] -= 1  # Subtract 1 from hours
        df.loc[df[minute_col] < 0, minute_col] += 60  # Add 60 minutes to balance

    # Create a proper timestamp column
    df["time"] = pd.to_datetime(df[hour_col].astype(str) + ":" + 
                                df[minute_col].astype(str) + ":" + 
                                df[second_col].astype(str) + "." + 
                                df[millisecond_col].astype(str).str.zfill(3), 
                                format="%H:%M:%S.%f", errors='coerce')  # Handle conversion errors

    
    # Convert start and end times to proper format
    start_time = pd.to_datetime(start_time, format="%H:%M:%S.%f")
    end_time = pd.to_datetime(end_time, format="%H:%M:%S.%f")

    # Filter rows within the time range
    df_filtered = df[(df["time"] >= start_time) & (df["time"] <= end_time)]

    # Sort by time
    df_sorted = df_filtered.sort_values(by="time", ascending=ascending)

    # Drop the temporary time column
    df_sorted = df_sorted.drop(columns=["time"])

    return df_sorted

if __name__ == "__main__":
    csv_file = r"C:\Users\Samuel Halperin\OneDrive\Documents\GitHub\lightening_plotting\info_storage\GLM_9_7_filtered2.csv"
    
    sorted_filtered_df = filter_and_sort_csv(csv_file, "hour", "minute", "second", "millisecond", 
                                             "00:29:06.100", "00:29:40.100", ascending=True)
    
    print(sorted_filtered_df)
