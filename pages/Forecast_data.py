import streamlit as st
from datetime import datetime, timedelta



page_bg_color = """
<style>
    .stApp {
    background-color: #0093E9;
    background-image: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);

    background-attachment: fixed;
    color: black;
    }
    div.stButton > button {
        color: white; /* Change button text color */
        
        border-radius: 5px; /* Optional: Rounded corners */
        background-color: #0078D4;  /* Optional: Set a custom background color */
        padding: 10px 20px;  /* Optional: Add padding to the button */
        font-weight: bold; /* Optional: Bold text */
    }

    div.stButton >button:hover {
        background-color: #005A8B;  /* Optional: Change the background color on hover */
        color: white;
        border:blue;    }

    div.stDownloadButton > button {
    color: white; /* Change this to the desired text color */
    background-color: #0078D4;
    }

    div.stDownloadButton >button:hover {
        background-color: #005A8B;  /* Optional: Change the background color on hover */
        color: white;
        border:blue;    }


</style>
"""

# Inject CSS into the Streamlit app
st.markdown(page_bg_color, unsafe_allow_html=True)


st.title("⏲️7-DAY HOURLY FORECASTING")
st.divider()

st.write("**Air Quality Index (AQI) in Kathmandu for available stations**")
st.markdown(
    """

    This functionality predicts the Air Quality Index for the available stations. The prediction is done individually by the following three machine learning algorithms:
    - **Gradient Boosting Regressor**
    - **Cat Boost Regressor**
    - **Random Forest Regressor**
""")
st.divider()


st.header("A. MAHARAJGUNJ")

algorithms = ["GBM", "CatBoost", "RFRegressor"]

formatted_date = datetime.now().strftime("%Y-%m-%d")  # Example format: YYYY-MM-DD
date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")

st.write(f"Today's date: {formatted_date}. Click on the following buttons to view the forecasted data for respective day")
# Extract year, month, and day
year = date_obj.year
month = date_obj.month
day = date_obj.day

col1, col2, col3, col4, col5, col6, col7 = st.columns(7)

@st.cache_data
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


def process_day_data(i, algorithms):
    #Helper function to process data for a given day and algorithms.
    dataframeslist = []
    
    for algo in algorithms:
        if 'dataframes' in st.session_state:
            key = f"Maharajgunj_day{i}_{algo}"
            if key in st.session_state['dataframes']:
                df = st.session_state['dataframes'][key]
        # Ensure object columns are cast to strings
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)
        dataframeslist.append(df)
        
    return dataframeslist

def process_day_data_phora(i, algorithms):
    #Helper function to process data for a given day and algorithms.
    dataframeslist = []
    
    for algo in algorithms:
        if 'dataframes_phora' in st.session_state:
            key = f"Phora_day{i}_{algo}"
            if key in st.session_state['dataframes_phora']:
                df = st.session_state['dataframes_phora'][key]
        # Ensure object columns are cast to strings
        for col in df.select_dtypes(include=['object']).columns:
            df[col] = df[col].astype(str)
        dataframeslist.append(df)
        
    return dataframeslist
    


# Add buttons and spinner logic for each day
for i, col in enumerate([col1, col2, col3, col4, col5, col6, col7], start=1):
    selected_date1 = date_obj + timedelta(days=i - 1)
    date_label1 = selected_date1.strftime("%Y-%m-%d")
    if col.button(f"{date_label1}", use_container_width=True):
        
        with st.status("Making Predictions...", expanded=True) as status:
            st.write("Fetching weather data...")

            dataframes = process_day_data(i, algorithms)
            
            st.write("Predicting using Machine learning algorithms.")
            
            st.write("Preparing ...")
            

            status.update(
                label="Predictions complete!", state="complete", expanded=False
            )


        # Display the dataframes in three columns
        c1, c2, c3 = st.columns(3)
        c1.dataframe(dataframes[0], use_container_width=True)
        csv1 = convert_df(dataframes[0])
        c1.download_button(label=f"Download Day {i} data predicted with algorithm: Gradient Boosting Regressor", data=csv1, file_name=f"day{i}_AQI_GBM.csv", mime="text/csv")
        c2.dataframe(dataframes[1], use_container_width=True)
        csv2 = convert_df(dataframes[1])
        c2.download_button(label=f"Download Day {i} data predicted with algorithm: CatBoost Regressor", data=csv2, file_name=f"day{i}_AQI_CatBoosting.csv", mime="text/csv")
        c3.dataframe(dataframes[2], use_container_width=True)
        csv3 = convert_df(dataframes[2])
        c3.download_button(label=f"Download Day {i} data predicted with algorithm: Random Forest Regressor", data=csv3, file_name=f"day{i}_AQI_RandomForest.csv", mime="text/csv")



st.header("A. PHORA DURBAR")
st.write(f"Today's date: {formatted_date}. Click on the following buttons to view the forecasted data for respective day")



col_p1, col_p2, col_p3, col_p4, col_p5, col_p6, col_p7 = st.columns(7)
# Add buttons and spinner logic for each day
for i, col_p in enumerate([col_p1, col_p2, col_p3, col_p4, col_p5, col_p6, col_p7], start=1):
    selected_date2 = date_obj + timedelta(days=i - 1)
    date_label2 = selected_date2.strftime("%Y-%m-%d")
    if col_p.button(f"{date_label2}", use_container_width=True, key = f"Day{i}"):
        
        with st.status("Making Predictions...", expanded=True) as status:
            st.write("Fetching weather data...")

            dataframes_phora = process_day_data_phora(i, algorithms)
            
            st.write("Predicting using Machine learning algorithms.")
            
            st.write("Preparing ...")
            

            status.update(
                label="Predictions complete!", state="complete", expanded=False
            )


        # Display the dataframes in three columns
        cp1, cp2, cp3 = st.columns(3)
        cp1.dataframe(dataframes_phora[0], use_container_width=True)
        csv1 = convert_df(dataframes_phora[0])
        cp1.download_button(label=f"Download Day {i} data predicted with algorithm: Gradient Boostin Regressor", data=csv1, file_name=f"day{i}_AQI_GBM.csv", mime="text/csv")
        cp2.dataframe(dataframes_phora[1], use_container_width=True)
        csv2 = convert_df(dataframes_phora[1])
        cp2.download_button(label=f"Download Day {i} data predicted with algorithm: CatBoost Regressor", data=csv2, file_name=f"day{i}_AQI_CatBoosting.csv", mime="text/csv")
        cp3.dataframe(dataframes_phora[2], use_container_width=True)
        csv3 = convert_df(dataframes_phora[2])
        cp3.download_button(label=f"Download Day {i} data predicted with algorithm: Random Forest Regressor", data=csv3, file_name=f"day{i}_AQI_RandomForest.csv", mime="text/csv")
