import openmeteo_requests
import requests_cache
import pandas as pd
from retry_requests import retry
import pickle
from datetime import datetime, timedelta
#from contacts import extract_time_aqi
#from contacts import final_convert_to_dataframe


def extract_time_aqi(forecasted_dataframe, algo):
    forecasted = pd.DataFrame(columns = ['Month', 'Day', 'Hour', f'AQI_{algo}'])
    for i in range (len(forecasted_dataframe)):
        forecasted.loc[i, 'Month'] = forecasted_dataframe.loc[i, 'Month']
        forecasted.loc[i, 'Day'] = forecasted_dataframe.loc[i, 'Day']
        forecasted.loc[i, 'Hour'] = forecasted_dataframe.loc[i, 'Hour']
        forecasted.loc[i, f'AQI_{algo}'] = forecasted_dataframe.loc[i, f'AQI_{algo}']
    
    return forecasted

def final_convert_to_dataframe(predicted_aqis, algo, features):
    aqi_df = pd.DataFrame(columns=[f'AQI_{algo}'])
    for i in range (len(predicted_aqis)):
        aqi_df.loc[i, f'AQI_{algo}'] = predicted_aqis[i]
        
    final_forecast = pd.concat([features, aqi_df], axis = 1)
    return final_forecast


# Setup the Open-Meteo API client with cache and retry on error
cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
openmeteo = openmeteo_requests.Client(session = retry_session)

# Make sure all required weather variables are listed here
# The order of variables in hourly or daily is important to assign them correctly below

lat_maharjgunj = 27.7364
long_maharajgunj = 85.3304

lat_phora = 27.7174
long_phora = 85.3197

lat_ratnapark = 27.7062
long_ratnapark = 85.3151

lat_khumaltaar = 27.6536
long_khumaaltar = 85.3285

def open_meteo_weather_data(lat, long):
    
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
	"latitude": lat,
	"longitude": long,
	"hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "precipitation", "wind_speed_10m", "pressure_msl"],
	"forecast_days": 7
    }
    
    responses = openmeteo.weather_api(url, params=params)
    
    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]
    #print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
    # #print(f"Elevation {response.Elevation()} m asl")
    # #print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
    # #print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
    hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
    hourly_dew_point_2m = hourly.Variables(2).ValuesAsNumpy()
    hourly_precipitation = hourly.Variables(3).ValuesAsNumpy()
    hourly_wind_speed_10m = hourly.Variables(4).ValuesAsNumpy()
    hourly_pressure = hourly.Variables(5).ValuesAsNumpy()
    
    hourly_data = {"date": pd.date_range(
	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
	freq = pd.Timedelta(seconds = hourly.Interval()),
	inclusive = "left"
    )}
    
    hourly_data["Temperature (°C)"] = hourly_temperature_2m
    hourly_data["Relative Humidity (%)"] = hourly_relative_humidity_2m
    hourly_data["dewpoint_2m"] = hourly_dew_point_2m
    hourly_data["Precipitation (mm)"] = hourly_precipitation
    hourly_data["windspeed_10m"] = hourly_wind_speed_10m
    hourly_data["Pressure (hPa)"] = hourly_pressure
    hourly_dataframe = pd.DataFrame(data = hourly_data)
    
    
    hourly_dataframe['date'] = pd.to_datetime(hourly_dataframe['date'])
    hourly_dataframe['Year'] = hourly_dataframe['date'].dt.year
    hourly_dataframe['Month'] = hourly_dataframe['date'].dt.month
    hourly_dataframe['Day'] = hourly_dataframe['date'].dt.day
    hourly_dataframe['Hour'] = hourly_dataframe['date'].dt.hour
    
    features = hourly_dataframe [['Month','Day', 'Hour', 'Temperature (°C)', 'dewpoint_2m', 'Relative Humidity (%)', 'Precipitation (mm)', 'windspeed_10m', 'Pressure (hPa)']]
    return features

predicted_aqi1 = []
predicted_aqi2 = []
predicted_aqi3 = []
    

#Extracting Gradient Boosting for both
with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\AQI_GBM_maharajgunj_newest.pkl', 'rb') as file1:
    aqi_model1 = pickle.load(file1)

with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\AQI_GBM_phora_newest.pkl', 'rb') as file_p1:
    aqi_model1_phora = pickle.load(file_p1)


#Extracting Cat Boosting for both
with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\AQI_Catboosting_maharajgunj_newest.pkl', 'rb') as file2:
    aqi_model2 = pickle.load(file2)    

with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\AQI_Catboosting_phora_newest.pkl', 'rb') as file_p2:
    aqi_model2_phora = pickle.load(file_p2)    

#Extracting Random Forest for both
with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\AQI_RandomForest_maharajgunj_newest.pkl', 'rb') as file3:
    aqi_model3 = pickle.load(file3)


with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\AQI_RandomForest_phora_newest.pkl', 'rb') as file_p3:
    aqi_model3_phora = pickle.load(file_p3)


def make_list (n):
    features = open_meteo_weather_data(lat_maharjgunj, long_maharajgunj)
    b = features.iloc[n]
    list = [[]]
    f = ['Month','Day', 'Hour', 'Temperature (°C)', 'dewpoint_2m', 'Relative Humidity (%)', 'Precipitation (mm)', 'windspeed_10m', 'Pressure (hPa)']
    for i in range(9):
        c = str(b[f'{f[i]}'])
        list[0].insert(i, str(c))
    
    return list

#Extracting Gradient Boosting Scaler
with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Scaler_GBM_maharajgunj_newest.pkl', 'rb') as file4:
    scaler1 = pickle.load(file4)

with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Scaler_GBM_phora_newest.pkl', 'rb') as file_p4:
    scaler1_phora = pickle.load(file_p4)


#Extracting Cat Boosting Scaler
with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Scaler_catBoosting_maharajgunj_newest.pkl', 'rb') as file5:
    scaler2 = pickle.load(file5)


with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Scaler_catboosting_phora_newest.pkl', 'rb') as file_p5:
    scaler2_phora = pickle.load(file_p5)



#Extracting Random Forest Scaler
with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Scaler_RandomForest_maharajgunj_newest.pkl', 'rb') as file6:
    scaler3 = pickle.load(file6)


with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Scaler_RandomForest_phora_newest.pkl', 'rb') as file_p6:
    scaler3_phora = pickle.load(file_p6)


#Extracting Random Forest Poly
with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Poly_RandomForest_maharajgunj_newest.pkl', 'rb') as file7:
    poly = pickle.load(file7)

with open('D:\\ML Predictions\\AirPollutionUI\\air-pollution-ml\\flask-server\\pages\\Newest_models\\Poly_RandomForest_phora_newest.pkl', 'rb') as file_p7:
    poly_phora = pickle.load(file_p7)



example_features = {
    "Month": '12',
    "Day": '1',
    "Hour": '24',
    "Temperature (°C)": '23',
    "dewpoint_2m": '9.6',
    "Relative Humidity (%)": '91',
    "Precipitation (mm)": '2',
    "windspeed_10m": '6.6',
    "Pressure (hPa)": '1014.7'
}


def generate_final_dataframe_with_AQI_with_time(algo, features):
    predicted_aqi = []
    for i in range(len(features)):
        b = features.iloc[i]
        f = ['Month','Day', 'Hour', 'Temperature (°C)', 'dewpoint_2m', 'Relative Humidity (%)', 'Precipitation (mm)', 'windspeed_10m', 'Pressure (hPa)']
        example_features1 = {
            "Month": b[f'{f[0]}'],
            "Day": b[f'{f[1]}'],
            "Hour": b[f'{f[2]}'],
            "Temperature (°C)": b[f'{f[3]}'],
            "dewpoint_2m": b[f'{f[4]}'],
            "Relative Humidity (%)": b[f'{f[5]}'],
            "Precipitation (mm)": b[f'{f[6]}'],
            "windspeed_10m": b[f'{f[7]}'],
            "Pressure (hPa)": b[f'{f[8]}']
        }
        
        input_data1 = pd.DataFrame([example_features1])
        #Using Gradient Boosting
        
        if algo == 'GBM':
            #input_data1 = pd.DataFrame([example_features1])
            scaled_input1 = scaler1.transform(input_data1)
            predicted_aqi.append(aqi_model1.predict(scaled_input1))
        
        #Using Cat Gradient Boosting    
        elif algo =='CatBoost':
            scaled_input2 = scaler2.transform(input_data1)
            predicted_aqi.append(aqi_model2.predict(scaled_input2))
            
        #Using Random Forest
        elif algo == 'RFRegressor': 
            #First apply poly scale
            X_poly_sample1 = poly.transform(input_data1)
            #Then apply Scaler3
            X_scaled_sample1 = scaler3.transform(X_poly_sample1)
            predicted_aqi.append(aqi_model3.predict(X_scaled_sample1))
            
    
    final_forecast = final_convert_to_dataframe(predicted_aqi, algo, features)
    forecast_with_time = extract_time_aqi(final_forecast, algo)
    return forecast_with_time
    
def generate_final_dataframe_with_AQI_with_time_phora(algo, features):
    predicted_aqi = []
    for i in range(len(features)):
        b = features.iloc[i]
        f = ['Month','Day', 'Hour', 'Temperature (°C)', 'dewpoint_2m', 'Relative Humidity (%)', 'Precipitation (mm)', 'windspeed_10m', 'Pressure (hPa)']
        example_features1 = {
            "Month": b[f'{f[0]}'],
            "Day": b[f'{f[1]}'],
            "Hour": b[f'{f[2]}'],
            "Temperature (°C)": b[f'{f[3]}'],
            "dewpoint_2m": b[f'{f[4]}'],
            "Relative Humidity (%)": b[f'{f[5]}'],
            "Precipitation (mm)": b[f'{f[6]}'],
            "windspeed_10m": b[f'{f[7]}'],
            "Pressure (hPa)": b[f'{f[8]}']
        }
        
        input_data1 = pd.DataFrame([example_features1])
        #Using Gradient Boosting
        
        if algo == 'GBM':
            #input_data1 = pd.DataFrame([example_features1])
            scaled_input1 = scaler1_phora.transform(input_data1)
            predicted_aqi.append(aqi_model1_phora.predict(scaled_input1))
        
        #Using Cat Gradient Boosting    
        elif algo =='CatBoost':
            scaled_input2 = scaler2_phora.transform(input_data1)
            predicted_aqi.append(aqi_model2_phora.predict(scaled_input2))
            
        #Using Random Forest
        elif algo == 'RFRegressor': 
            #First apply poly scale
            X_poly_sample1 = poly_phora.transform(input_data1)
            #Then apply Scaler3
            X_scaled_sample1 = scaler3_phora.transform(X_poly_sample1)
            predicted_aqi.append(aqi_model3_phora.predict(X_scaled_sample1))
            
    
    final_forecast = final_convert_to_dataframe(predicted_aqi, algo, features)
    forecast_with_time = extract_time_aqi(final_forecast, algo)
    return forecast_with_time

"""
def generate_final_dataframe_with_AQI_with_time_ratnapark(algo, features):
    predicted_aqi = []
    for i in range(len(features)):
        b = features.iloc[i]
        f = ['Month','Day', 'Hour', 'Temperature (°C)', 'dewpoint_2m', 'Relative Humidity (%)', 'Precipitation (mm)', 'windspeed_10m', 'Pressure (hPa)']
        example_features1 = {
            "Month": b[f'{f[0]}'],
            "Day": b[f'{f[1]}'],
            "Hour": b[f'{f[2]}'],
            "Temperature (°C)": b[f'{f[3]}'],
            "dewpoint_2m": b[f'{f[4]}'],
            "Relative Humidity (%)": b[f'{f[5]}'],
            "Precipitation (mm)": b[f'{f[6]}'],
            "windspeed_10m": b[f'{f[7]}'],
            "Pressure (hPa)": b[f'{f[8]}']
        }
        
        input_data1 = pd.DataFrame([example_features1])
        #Using Gradient Boosting
        
        if algo == 'GBM':
            #input_data1 = pd.DataFrame([example_features1])
            scaled_input1 = scaler1.transform(input_data1)
            predicted_aqi.append(aqi_model1.predict(scaled_input1))
        
        #Using Cat Gradient Boosting    
        elif algo =='CatBoost':
            scaled_input2 = scaler2.transform(input_data1)
            predicted_aqi.append(aqi_model2.predict(scaled_input2))
            
        #Using Random Forest
        elif algo == 'RFRegressor': 
            #First apply poly scale
            X_poly_sample1 = poly.transform(input_data1)
            #Then apply Scaler3
            X_scaled_sample1 = scaler3.transform(X_poly_sample1)
            predicted_aqi.append(aqi_model3.predict(X_scaled_sample1))
            
    
    final_forecast = final_convert_to_dataframe(predicted_aqi, algo, features)
    forecast_with_time = extract_time_aqi(final_forecast, algo)
    return forecast_with_time


def generate_final_dataframe_with_AQI_with_time_khumaltaar(algo, features):
    predicted_aqi = []
    for i in range(len(features)):
        b = features.iloc[i]
        f = ['Month','Day', 'Hour', 'Temperature (°C)', 'dewpoint_2m', 'Relative Humidity (%)', 'Precipitation (mm)', 'windspeed_10m', 'Pressure (hPa)']
        example_features1 = {
            "Month": b[f'{f[0]}'],
            "Day": b[f'{f[1]}'],
            "Hour": b[f'{f[2]}'],
            "Temperature (°C)": b[f'{f[3]}'],
            "dewpoint_2m": b[f'{f[4]}'],
            "Relative Humidity (%)": b[f'{f[5]}'],
            "Precipitation (mm)": b[f'{f[6]}'],
            "windspeed_10m": b[f'{f[7]}'],
            "Pressure (hPa)": b[f'{f[8]}']
        }
        
        input_data1 = pd.DataFrame([example_features1])
        #Using Gradient Boosting
        
        if algo == 'GBM':
            #input_data1 = pd.DataFrame([example_features1])
            scaled_input1 = scaler1_phora.transform(input_data1)
            predicted_aqi.append(aqi_model1_phora.predict(scaled_input1))
        
        #Using Cat Gradient Boosting    
        elif algo =='CatBoost':
            scaled_input2 = scaler2_phora.transform(input_data1)
            predicted_aqi.append(aqi_model2_phora.predict(scaled_input2))
            
        #Using Random Forest
        elif algo == 'RFRegressor': 
            #First apply poly scale
            X_poly_sample1 = poly_phora.transform(input_data1)
            #Then apply Scaler3
            X_scaled_sample1 = scaler3_phora.transform(X_poly_sample1)
            predicted_aqi.append(aqi_model3_phora.predict(X_scaled_sample1))
            
    
    final_forecast = final_convert_to_dataframe(predicted_aqi, algo, features)
    forecast_with_time = extract_time_aqi(final_forecast, algo)
    return forecast_with_time

"""

def generate_final_dataframe_with_AQI_with_time_per_day(n, algo):
    features = open_meteo_weather_data(lat_maharjgunj, long_maharajgunj)
    all_data = generate_final_dataframe_with_AQI_with_time(algo, features)

    #current_year = datetime.now()
    #default_year = 2024
    #base_date = datetime(current_year, int(all_data.iloc[0]["Month"]), int(all_data.iloc[0]["Day"]))
    #target_date = current_year + timedelta(days=n - 1)
    #first_day_value = target_date.day
    day = all_data.iloc[0]["Day"]
    month = all_data.iloc[0]["Month"]

    current_year = datetime.now().year
    base_date = datetime(current_year, month, day)
    target_date = base_date + timedelta(days=n - 1)

    target_month = target_date.month
    target_year = target_date.year

    a= day
    first_day = a +(n-1)

    if first_day >31:
        first_day_value = first_day-31
    else:
        first_day_value = first_day

    data_single_day = pd.DataFrame(columns=all_data.columns)
    for i in range (len(all_data)):
        if all_data.iloc[i]["Day"] == first_day_value:
            data_single_day = pd.concat([data_single_day, all_data.iloc[[i]]], ignore_index=True)
        

    return data_single_day

def generate_final_dataframe_with_AQI_with_time_per_day_phora(n, algo):
    features = open_meteo_weather_data(lat_phora, long_phora)
    all_data = generate_final_dataframe_with_AQI_with_time_phora(algo, features)
    day = all_data.iloc[0]["Day"]
    a= day
    first_day = a +(n-1)
    if first_day >31:
        first_day_value = first_day-31
    else:
        first_day_value = first_day
    data_single_day = pd.DataFrame(columns=all_data.columns)
    for i in range (len(all_data)):
        if all_data.iloc[i]["Day"] == first_day_value:
            data_single_day = pd.concat([data_single_day, all_data.iloc[[i]]], ignore_index=True)
    
    return data_single_day

"""
def generate_final_dataframe_with_AQI_with_time_per_day_ratnapark(n, algo):
    features = open_meteo_weather_data(lat_ratnapark, long_ratnapark)
    all_data = generate_final_dataframe_with_AQI_with_time_ratnapark(algo, features)
    day = all_data.iloc[0]["Day"]
    a= day
    first_day = a +(n-1)
    if first_day >31:
        first_day_value = first_day-31
    else:
        first_day_value = first_day
    data_single_day = pd.DataFrame(columns=all_data.columns)
    for i in range (len(all_data)):
        if all_data.iloc[i]["Day"] == first_day_value:
            data_single_day = pd.concat([data_single_day, all_data.iloc[[i]]], ignore_index=True)
    
    return data_single_day


def generate_final_dataframe_with_AQI_with_time_per_day_khumaltaar(n, algo):
    features = open_meteo_weather_data(lat_khumaltaar, long_khumaaltar)
    all_data = generate_final_dataframe_with_AQI_with_time_khumaltaar(algo, features)
    day = all_data.iloc[0]["Day"]
    a= day
    first_day = a +(n-1)
    if first_day >31:
        first_day_value = first_day-31
    else:
        first_day_value = first_day
    data_single_day = pd.DataFrame(columns=all_data.columns)
    for i in range (len(all_data)):
        if all_data.iloc[i]["Day"] == first_day_value:
            data_single_day = pd.concat([data_single_day, all_data.iloc[[i]]], ignore_index=True)
    
    return data_single_day
"""


def send_features_maharajgunj():

    features = open_meteo_weather_data(lat_maharjgunj, long_maharajgunj)
    return features

def send_features_phora123():
    features = open_meteo_weather_data(lat_phora, long_phora)
    return features




algorithms = ["GBM", "CatBoost", "RFRegressor"]
