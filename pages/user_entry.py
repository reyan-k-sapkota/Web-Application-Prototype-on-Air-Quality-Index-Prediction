import streamlit as st
import pickle
import pandas as pd
import calendar

page_bg_color = """
<style>
    .stApp {
    background-color: #0093E9;
    background-image: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);

    background-attachment: fixed;
    color: black;
    }

    .stForm button {
        color: white;  /* Change button text color to white */
        background-color: #0078D4;  /* Optional: Set a custom background color */
        border-radius: 8px;  /* Optional: Change the button's border radius */
        padding: 10px 20px;  /* Optional: Add padding to the button */
    }

    .stForm button:hover {
        background-color: #005A8B;  /* Optional: Change the background color on hover */
        color: white;
        border:blue;    }

   

</style>
"""
st.markdown(page_bg_color, unsafe_allow_html=True)

st.title ("🔨PREDICT YOURSELF")
st.divider()

st.markdown(
    """
    **This functionality allows you to change the values of the dependent features and make predictions for the data of your choice.** The follwing features are allowed to be changed: 
    - Location
    - Month
    - Day
    - Hour
    - Dew Point (°C)
    - Temperature (in °C)
    - Relative Humidity (in percentage)
    - Wind Speed (10m) [km/h]
    - Pressure (in hectoPascals)
    - Precipitation (mm)
""")
st. divider()


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



algorithms = ["Gradient Boost Regressor", "CatBoost Regressor", "RandomForest Regressor"]

def get_days_in_month(month):
    
    _, num_days = calendar.monthrange(2024, month) 
    return list(range(1, num_days + 1))

def days_in_month(month):
    if month ==2:
        return 28


with st.form("prediction_form"):

    location = st.selectbox("Which Location's data would you like to predict?", options = ('Maharajgunj','Phora Durbar'))
    
    month = st.slider("Select Month", min_value=1, max_value=12, value=1, )

    day_count = get_days_in_month(month)
    day_from_input = st.selectbox("Which day's mapping would you like to generate?", options = day_count)

    hour_from_input = st.slider("Select Hour", min_value=0, max_value=23, value=1, )
    
    dew_point = st.slider("Dew Point (°C)", min_value=0.0, max_value=30.0, value=0.01, )
    #dew_point = st.number_input("Dew Point (°C)", min_value=-50.0,  step=0.1)
    temperature = st.number_input("Temperature (in °C)", min_value=-10.0, step=0.1)
    relative_humidity = st.slider("Relative Humidity (in percentage)", min_value=0.0, max_value=100.0, step=0.1)
    windspeed = st.slider("Wind Speed (10m) [km/h]", min_value=0.0, max_value=36.0, value=0.01, )
    #windspeed = st.number_input("Windspeed (10m)", min_value=0.0, step=0.1)
    pressure = st.number_input("Pressure (in HectoPascals)", min_value=0.0, step=0.1)
    precipitation = st.slider("Precipitation (mm)", min_value=0.0, max_value=50.0, value=0.1, )

    #precipitation = st.number_input("Precipitation (mm)", min_value=0.0, step=0.1)

    c1, c2, c3 = st.columns(3)
    with c1:
        submit_button1 = st.form_submit_button(label="Predict using Gradient Boost Regressor")
    
    with c2:
        submit_button2 = st.form_submit_button(label="Predict using CatBoost Regressor")

    with c3:
        submit_button3 = st.form_submit_button(label="Predict using Random Forest Regressor")
    

user_entered_features = {
    "Month": month,
    "Day": day_from_input,
    "Hour": hour_from_input,
    "Temperature (°C)": temperature,
    "dewpoint_2m": dew_point,
    "Relative Humidity (%)": relative_humidity,
    "Precipitation (mm)": precipitation,
    "windspeed_10m": windspeed,
    "Pressure (hPa)": pressure
}
input_data1 = pd.DataFrame([user_entered_features])


if submit_button1:
    if location == 'Maharajgunj':
        scaled_input_aqi = scaler1.transform(input_data1)
        prediction_aqi = aqi_model1.predict(scaled_input_aqi)
        st.write(f"Your chosen location is **{location}** and you wish to use **{algorithms[0]}**")
        st.write(f"Predicted AQI value is **{prediction_aqi}**")
    elif location=='Phora Durbar':
        scaled_input_aqi_p = scaler1_phora.transform(input_data1)
        prediction_aqi_p = aqi_model1_phora.predict(scaled_input_aqi_p)
        st.write(f"Your choses location is **{location}** and you wish to use **{algorithms[0]}**")
        st.write(f"Predicted AQI value is **{prediction_aqi_p}**")


if submit_button2:
    if location == 'Maharajgunj':
        scaled_input_aqi = scaler2.transform(input_data1)
        prediction_aqi = aqi_model2.predict(scaled_input_aqi)
        st.write(f"Your chosen location is **{location}** and you wish to use **{algorithms[1]}**")
        st.write(f"Predicted AQI value is **{prediction_aqi}**")
    elif location=='Phora Durbar':
        scaled_input_aqi_p = scaler2_phora.transform(input_data1)
        prediction_aqi_p = aqi_model2_phora.predict(scaled_input_aqi_p)
        st.write(f"Your chosen location is **{location}** and you wish to use **{algorithms[1]}**")
        st.write(f"Predicted AQI value is **{prediction_aqi_p}**")


    
if submit_button3:
    if location == 'Maharajgunj':
        X_poly_sample1 = poly.transform(input_data1)
        scaled_input_aqi = scaler3.transform(X_poly_sample1)
        prediction_aqi = aqi_model3.predict(scaled_input_aqi)
        st.write(f"Your chosen location is **{location}** and you wish to use **{algorithms[2]}**")
        st.write(f"Predicted AQI value is **{prediction_aqi}**")
    elif location=='Phora Durbar':
        X_poly_sample1_p = poly.transform(input_data1)
        scaled_input_aqi_p = scaler3.transform(X_poly_sample1_p)
        prediction_aqi_p = aqi_model3_phora.predict(scaled_input_aqi_p)
        st.write(f"Your chosen location is **{location}** and you wish to use **{algorithms[2]}**")
        st.write(f"Predicted AQI value is **{prediction_aqi_p}**")
   
        
