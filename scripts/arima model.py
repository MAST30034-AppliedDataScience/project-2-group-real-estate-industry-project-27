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

def predict_growth(rental_prices, predictions):
    '''Calculate predicted growth rate using the the given historical data
    and the predictions, return the growth rate'''
    # Calculate the last known price and the predicted price at the end of 3 years
    last_known_price = rental_prices.iloc[-1]
    predicted_final_price = predictions.iloc[-1]
    predicted_growth_rate = (predicted_final_price - last_known_price) / last_known_price
    growth_rate_per_year = predicted_growth_rate/3

    return growth_rate_per_year


def predict_for_df(df, target, predict_df, predict_dates):
    '''Predict the future rental prices for the indicated predict dates 
    and dataframe, store predictions in predict df and return predict df'''
    if target == 'suburb':
        predicted_growth_rates = {}

    for suburb in df.index:
        # Extract the rental prices for the suburb
        rental_prices = df.loc[suburb].dropna() 
        
        # Fit auto_arima to find the best ARIMA parameters
        model = auto_arima(rental_prices, seasonal=False, stepwise=True, suppress_warnings=True)
        
        # Make predictions
        predictions = model.predict(n_periods=20)

        if target == 'suburb':
            growth_rate = predict_growth(rental_prices, predictions)
            # Store the predicted growth rate for the suburb
            predicted_growth_rates[suburb] = growth_rate
                
        predictions.index = predict_dates

        # Add the predictions of the suburb to the dataframe
        predict_df[suburb] = predictions

    if target == 'suburb':
        predicted_growth_rate_series = pd.Series(predicted_growth_rates)
        return predict_df, predicted_growth_rate_series
    
    return predict_df

def predict_rental_prices(dataframe_list, target, folder_path, predict_filename):
    '''Predict future rental prices for each type in the dataframe list,
    then save the predictions under the indicated filename and folder path'''
    if target == 'suburb':
        growth_rates = []
    # Loop through each property type
    for i in range(len(dataframe_list)):
        # Create a DataFrame to store the predictions
        predict_dates = pd.date_range(start=dataframe_list[i].columns[-1], periods=20, freq='Q')                                                          
        predict_df = pd.DataFrame(index=predict_dates)

        if target == 'suburb':
            predict_df, predicted_growth_rates = predict_for_df(dataframe_list[i], target, 
                                                                predict_df, predict_dates)
            growth_rates.append(predicted_growth_rates)

        elif target == 'postcode':
            predict_df = predict_for_df(dataframe_list[i], target, 
                                                                predict_df, predict_dates)
        
        # Save the final result to a CSV file
        file_name = predict_filename[i]
        file_path = os.path.join(folder_path, file_name)
        
        # Create the folder if it is not existed
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        predict_df.reset_index().to_csv(file_path, index=False) 
           
    if target == 'suburb':
        return growth_rates
        
