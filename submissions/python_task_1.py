
import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\Users\HIKI\Desktop\TASK\MapUp-Data-Assessment-F\datasets\dataset-1.csv")
df2=pd.read_csv(r"C:\Users\HIKI\Desktop\TASK\MapUp-Data-Assessment-F\datasets\dataset-2.csv")

def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values,
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = df.pivot_table(index='id_1', columns='id_2', values='car', fill_value=0)

    # Set diagonal values to 0 using NumPy operations
    np.fill_diagonal(df.values, 0)

    return df

generate_car_matrix(df)

def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    conditions = [
        (df['car'] <= 15),
        (df['car'] > 15) & (df['car'] <= 25),
        (df['car'] > 25)
    ]

    car_types = ['low', 'medium', 'high']

    df['car_type'] = pd.Series(np.select(conditions, car_types))

    # Count occurrences of each car type
    type_counts = df['car_type'].value_counts().to_dict()

    return type_counts

get_type_count(df)

def get_bus_indexes(df) -> list:
    """
    Returns the indices where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame): Input DataFrame.

    Returns:
        list: List of indices where 'bus' values exceed twice the mean, sorted in ascending order.
    """
    # Calculate the mean of 'bus' values
    bus_mean = df['bus'].mean()

    # Filter indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the indices in ascending order
    bus_indexes.sort()

    return bus_indexes

print(get_bus_indexes(df))

def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Group by 'route' and calculate the average 'truck' values
    average_truck_by_route = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' values are greater than 7
    filtered_routes = average_truck_by_route[average_truck_by_route > 7].index.tolist()

    # Sort the routes in ascending order
    filtered_routes.sort()

    return filtered_routes

print(filter_routes(df))

def multiply_matrix(matrix) -> pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame): Input DataFrame (matrix).

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
     # Apply custom conditions to multiply matrix values using DataFrame.apply
    modified_matrix = matrix.apply(lambda row: row.apply(lambda x: x * 0.75 if x > 20 else x * 1.25), axis=1)

    # Round the values to 1 decimal place
    modified_matrix = modified_matrix.round(1)

    return modified_matrix

val=generate_car_matrix(df)
multiply_matrix(val)

def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
# Combine date and time columns and convert to datetime objects
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], format='%A %H:%M:%S')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], format='%A %H:%M:%S')

    # Check if the timestamps cover a full 24-hour period and span all 7 days
    df['full_coverage'] = (
        (df['end_timestamp'] - df['start_timestamp'] == pd.Timedelta(days=6, hours=23, minutes=59, seconds=59)) &
        (df['start_timestamp'].dt.time == pd.Timestamp('00:00:00').time()) &
        (df['end_timestamp'].dt.time == pd.Timestamp('23:59:59').time())
    )

    # Create a boolean series with multi-index (id, id_2)
    result_series = df.groupby(['id', 'id_2'])['full_coverage'].all()

    return result_series

print(time_check(df2))

