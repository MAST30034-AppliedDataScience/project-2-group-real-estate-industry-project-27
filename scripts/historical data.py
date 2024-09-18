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