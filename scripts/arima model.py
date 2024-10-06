import pandas as pd
import os
from pmdarima import auto_arima

def prepare_for_arima(df, target):
    '''Prepare the given dataframe for the ARIMA model
    return the prepared dataframe'''

    if target == 'suburb':
        df.set_index('suburb', inplace=True)
    elif target == 'postcode':  
        df = df.drop('suburb', axis=1)
        df.set_index('postcode', inplace=True)

    # Remove any extra characters besides month and year in column name
    df.columns = df.columns.str.extract(r'([a-zA-Z]+\s?\d{4})')[0]
    df.columns = pd.to_datetime(df.columns, format='%b %Y')

    return df

def read_make_list(folder_path, file_names):
    '''Read each file in the file names and return
     a list of Pandas dataframes read'''
    dataframe_list = []
    for name in file_names:
          file_path = folder_path + name
          df = pd.read_csv(file_path)
          dataframe_list.append(df)  
    return dataframe_list

def predict_for_df(df, predict_df, predict_dates):
    '''Predict the future rental prices for the indicated predict dates 
    and dataframe, store predictions in predict df and return predict df'''

    for suburb in df.index:
        # Extract the rental prices for the suburb
        rental_prices = df.loc[suburb].dropna() 
        
        # Fit auto_arima to find the best ARIMA parameters
        model = auto_arima(rental_prices, seasonal=False, stepwise=True, suppress_warnings=True)
        
        # Make predictions
        predictions = model.predict(n_periods=15)
        predictions.index = predict_dates

        # Add the predictions of the suburb to the dataframe
        predict_df[suburb] = predictions
    
    return predict_df

def predict_rental_prices(dataframe_list, folder_path, predict_filename):
    '''Predict future rental prices for each type in the dataframe list,
    then save the predictions under the indicated filename and folder path'''

    # Loop through each property type
    for i in range(len(dataframe_list)):
        # Create a DataFrame to store the predictions
        predict_dates = pd.date_range(start=dataframe_list[i].columns[-1], periods=15, freq='Q')                                                          
        predict_df = pd.DataFrame(index=predict_dates)

        predict_df = predict_for_df(dataframe_list[i], predict_df, predict_dates)
        
        # Save the final result to a CSV file
        file_name = predict_filename[i]
        file_path = os.path.join(folder_path, file_name)
        
        # Create the folder if it is not existed
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        predict_df.reset_index().to_csv(file_path, index=False) 

def predict_growth(predict_df):
    '''Calculate growth rate of each suburb using the predicted
    rental price, return the series growth rate by suburb'''
 
    first_price = predict_df.iloc[0]  # First row (initial predicted price)
    last_price = predict_df.iloc[-1]  # Last row (final predicted price)

    # Calculate the growth rate
    growth = (last_price - first_price) / first_price   # growth after 3 years
    growth_rate = growth/3  # annual growth
    return growth_rate
        
