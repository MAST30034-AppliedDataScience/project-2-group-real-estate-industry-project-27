import pandas as pd

def remove_redundant(df):
    '''Remove redundant rows/columns in the given historical 
    dataframe and return the cleaned one'''

    # Discard rows with areas outside of Melbourne Region
    # these are all the rows after Mornington Peninsula area
    index_value = df[df['Moving annual rent by suburb'] == 'Mornington Peninsula'].index[0]
    df = df.iloc[:index_value]

    # Drop a redundant column
    df.drop(columns=['Moving annual rent by suburb'], inplace=True)

    # Get the month and year to be the column name
    for i in range(1, len(df.columns)):
        df.columns.values[i] = df.iloc[0, i-1]

    df.rename(columns={'Unnamed: 1': 'suburb'}, inplace=True)

    # Remove the remaing redundant rows and columns 
    df = df.loc[:, ~df.columns.to_series().isna()]  # remove columns with name NaN
    df = df.iloc[2:].reset_index(drop=True)
    df = df[df['suburb'] != 'Group Total']

    return df

def split_suburbs(df):
    # Reset the index to turn the suburb back into a column
    df_reset = df.reset_index()
    new_rows = []
    for _, row in df_reset.iterrows():
        suburb = row['suburb']
        if '-' in suburb:
            # Split the suburb names by '-'
            suburbs = suburb.split('-')
            # For each suburb, create a new row with the same data
            for s in suburbs:
                new_row = row.to_dict()  # Convert the row to a dictionary
                new_row['suburb'] = s.strip()  # Assign new suburb name
                new_rows.append(new_row)  # Append the dictionary to the list
        else:
            # Append row as a dictionary if no '-' is present
            new_rows.append(row.to_dict())
       
    # Create a new DataFrame from the list of dictionaries
    new_df = pd.DataFrame(new_rows)
    return new_df

def remove_duplicated_postcodes(merged_df):
    '''Remove rows with duplicated postcodes, only keeping the first one
    Return the filtered df'''

    # Separate the rows with NaN postcodes
    nan_postcode_df = merged_df[merged_df['postcode'].isna()]

    # Remove duplicated postcodes on non Nan rows
    non_nan_postcode_df = merged_df.dropna(subset=['postcode']).drop_duplicates(subset='postcode', 
                                                                                keep='first')
    
    # Combine the NaN and cleaned non Nan together                                                       
    df_filtered = pd.concat([non_nan_postcode_df, nan_postcode_df], ignore_index=True)

    return df_filtered

def clean_merged_df(merged_df):
    '''Clean the merged dataframe by removing duplicate and
    reorder columns, return the cleaned dataframe'''

    # Reorder to make 'postcode' the first column in the merged df
    merged_df = merged_df[['postcode'] + [col for col in merged_df.columns if col != 'postcode']]
    
    # Convert postcode to integers
    merged_df['postcode'] = pd.to_numeric(merged_df['postcode'], errors='coerce').astype('Int64')

    # Remove duplicated postcodes
    df_filtered = remove_duplicated_postcodes(merged_df)

    nan_postcode_mask = df_filtered['postcode'].isna()
    duplicates_mask = df_filtered.duplicated(subset=df_filtered.columns.difference(['suburb', 'postcode']), 
                                           keep=False)
    df_cleaned = df_filtered[~(nan_postcode_mask & duplicates_mask)]

    return df_cleaned


    
