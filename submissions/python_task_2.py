import pandas as pd
from datetime import time

df=pd.read_csv(r"C:\Users\HIKI\Desktop\TASK\MapUp-Data-Assessment-F\datasets\dataset-3.csv")

df.head()

df.columns

df.isna().sum()

def calculate_distance_matrix(df):
    unique_ids = pd.Index(df[['id_start', 'id_end']].stack().unique(), name='ID')
    distance_matrix = pd.DataFrame(index=unique_ids, columns=unique_ids, dtype=float)

    def fill_distance(row):
        distance_matrix.at[row['id_start'], row['id_end']] = row['distance']
        distance_matrix.at[row['id_end'], row['id_start']] = row['distance']

    df.apply(fill_distance, axis=1)

    distance_matrix.fillna(0, inplace=True)
    return distance_matrix

# Question 1: Calculate Distance Matrix
distance_matrix = calculate_distance_matrix(df)
print(distance_matrix)

def unroll_distance_matrix(df):
    # Reset the index to convert 'ID' to a regular column
    distance_matrix_reset = df.reset_index()

    unrolled_df = distance_matrix_reset.melt(id_vars=['ID'], var_name='id_end', value_name='distance')
    unrolled_df['id_end'] = unrolled_df['id_end'].astype(int)
    unrolled_df.rename(columns={'ID': 'id_start'}, inplace=True)  # Rename the 'ID' column to 'id_start'
    return unrolled_df

# Question 2: Unroll Distance Matrix
unrolled_matrix = unroll_distance_matrix(distance_matrix)
print(unrolled_matrix)

def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
# Calculate the reference average distance
    reference_average = df[df['id_start'] == reference_id]['distance'].mean()

    # Calculate the threshold range
    threshold_min = reference_average * 0.9
    threshold_max = reference_average * 1.1

    # Filter the DataFrame based on the threshold
    result_df = df.groupby('id_start')['distance'].mean().reset_index()
    result_df = result_df[(result_df['distance'] >= threshold_min) & (result_df['distance'] <= threshold_max)]

    return result_df

# Question 3: Find IDs within Ten Percentage Threshold
reference_id = 1001400  # Replace with the desired reference ID
ids_within_threshold = find_ids_within_ten_percentage_threshold(unrolled_matrix, reference_id)
print(ids_within_threshold)

def calculate_toll_rate(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    for vehicle_type in rate_coefficients:
        df[vehicle_type] = df['distance'] * rate_coefficients[vehicle_type]

    return df

a=calculate_toll_rate(unrolled_matrix)

a.head(30)

import pandas as pd
from datetime import time, timedelta

def calculate_time_based_toll_rates(df):
    # Define rate coefficients for each vehicle type
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}

    # Define time ranges for weekdays
    weekday_ranges = [
        {'start': time(0, 0, 0), 'end': time(10, 0, 0), 'factor': 0.8},
        {'start': time(10, 0, 0), 'end': time(18, 0, 0), 'factor': 1.2},
        {'start': time(18, 0, 0), 'end': time(23, 59, 59), 'factor': 0.8}
    ]

    # Define constant discount factor for weekends
    weekend_factor = 0.7

    # Create a new list to hold rows for the result DataFrame
    result_rows = []

    # Iterate through each row in the original DataFrame
    for index, row in df.iterrows():
        # Extract the day of the week and time
        start_day = row['start_day']
        start_time = time(0, 0, 0)  # Assuming a starting time of 00:00:00
        end_day = row['start_day']
        end_time = time(23, 59, 59)  # Assuming an ending time of 23:59:59

        # Determine the discount factor based on the day of the week and time
        if start_day in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']:
            for time_range in weekday_ranges:
                if time_range['start'] <= start_time <= time_range['end']:
                    discount_factor = time_range['factor']
                    break
        else:
            discount_factor = weekend_factor

        # Calculate toll rates for each vehicle type
        toll_rates = {vehicle_type: row['distance'] * rate_coefficients[vehicle_type] * discount_factor for vehicle_type in rate_coefficients}

        # Append a new row to the result list
        result_rows.append({
            'id_start': row['id_start'],
            'id_end': row['id_end'],
            'distance': row['distance'],
            'start_day': start_day,
            'start_time': start_time,
            'end_day': end_day,
            'end_time': end_time,
            'bus': toll_rates['bus'],
            'truck': toll_rates['truck'],
            'moto': toll_rates['moto'],
            'car': toll_rates['car'],
            'rv': toll_rates['rv']
        })

    # Create the result DataFrame from the list of rows
    result_df = pd.DataFrame(result_rows)

    return result_df

# Assuming 'id_start', 'id_end', 'distance', and 'start_day' columns are present in your original DataFrame
# df_result = calculate_time_based_toll_rates(df)
# print(df_result)

# Assuming 'id_start', 'id_end', 'distance', and 'start_day' columns are present in your original DataFrame
df_result = calculate_time_based_toll_rates(df)

df_result