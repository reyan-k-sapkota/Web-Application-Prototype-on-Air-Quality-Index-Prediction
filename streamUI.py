import streamlit as st
from pages.charts import generate_final_dataframe_with_AQI_with_time_per_day
from pages.charts import generate_final_dataframe_with_AQI_with_time_per_day_phora



from pages.charts import send_features_maharajgunj
from datetime import datetime

about = st.Page(
    page = "pages/about.py",
    title = '👉Air Pollution Portal: Kathmandu Metro',
    default = True,
)

forecast_data = st.Page(
    page = "pages/Forecast_data.py",
    title = '⏲️7-Day Hourly Forecasting',
)

data_visualization = st.Page(
    page = "pages/AQI_Visualization.py",
    title = '📈AQI Data Visualization',
)

alert_message = st.Page(
    page = "pages/alert_message_new.py",
    title = '🍁Alert Message/Recommendation Generation',
)

info_circulation = st.Page(
    page = "pages/info_circulation.py",
    title = '🗺️Kathmandu Map Visualization',
)

user_entry = st.Page(
    page = "pages/user_entry.py",
    title = '🔨Predict Yourself',
)



st.set_page_config(layout="wide")

algorithms = ["GBM", "CatBoost", "RFRegressor"]

formatted_date = datetime.now().strftime("%Y-%m-%d")  # Example format: YYYY-MM-DD
date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")
year = date_obj.year
month = date_obj.month
day = date_obj.day

def process_day_data(day_num, algorithms):
    """Helper function to process data for a given day and algorithms."""
    dataframes = []
    for algo in algorithms:
        df = generate_final_dataframe_with_AQI_with_time_per_day(day_num, algo)
        # Ensure object columns are cast to strings
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)
        dataframes.append(df)
    return dataframes

def process_day_data_phora(day_num, algorithms):
    dataframes = []
    for algo in algorithms:
        df = generate_final_dataframe_with_AQI_with_time_per_day_phora(day_num, algo)
        # Ensure object columns are cast to strings
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)
        dataframes.append(df)
    return dataframes


if 'dataframes' not in st.session_state:
    st.session_state.dataframes = {}

if 'dataframes_phora' not in st.session_state:
    st.session_state.dataframes_phora = {}



for day in range(1, 7 + 1):
    for algo in algorithms:
        key_1 = f"Maharajgunj_day{day}_{algo}"
        key_2 = f"Phora_day{day}_{algo}"
       
        if key_1 not in st.session_state['dataframes']:
            df = generate_final_dataframe_with_AQI_with_time_per_day(day, algo)
            st.session_state['dataframes'][key_1] = df
            
        if key_2 not in st.session_state['dataframes_phora']:
            df_phora =generate_final_dataframe_with_AQI_with_time_per_day_phora(day, algo)
            st.session_state['dataframes_phora'][key_2] = df_phora
        


#if "df_page1" not in st.session_state:
#    st.session_state.df_page1 = df_maharajgunj

pg = st.navigation(
    {
        "🎯INSTRUCTION MANUAL": [about],
        "🎯DATA ANALYTICS" : [forecast_data, data_visualization, user_entry],
        "🎯ALERT MESSAGE AND REPORTING SYSTEM": [alert_message],
        "🎯MAPPING PORTAL": [info_circulation]
        
    }
    )

pg.run()





