import streamlit as st

from pages.charts import send_features_maharajgunj, send_features_phora123, generate_final_dataframe_with_AQI_with_time_per_day, generate_final_dataframe_with_AQI_with_time


page_bg_color = """
<style>
    .stApp {
    background-color: #0093E9;
    background-image: linear-gradient(160deg, #0093E9 0%, #80D0C7 100%);

    background-attachment: fixed;
    color: black;
    }
</style>
"""

# Inject CSS into the Streamlit app
st.markdown(page_bg_color, unsafe_allow_html=True)


algorithms = ["GBM", "CatBoost", "RFRegressor"]

#test = generate_final_dataframe_with_AQI_with_time(algorithms[1], p)
#p = send_features_maharajgunj()
#st.write (p)

st.write("# Welcome to Kathmandu Metropolitan City's Air Quality Index Monitoring Portal! 👋")

st.markdown(
    """
    Kathmandu Metro Air Quality Index Monitoring Portal is a dedicated web application that employs
    Machine Learning based predictive techniques to forecast the hourly values
    of 7-day Air Quality Index in Kathmandu. 
    
    **This system integrates 3 Machine
    Learning models, real-time data fetching/processing, and an intuitive user interface (UI) to provide accurate
    AQI predictions/visualizations, personalized recommendations/ email alerts for residents, and the federal
    government, and station-wise mapping on Kathmandu Metropolitan City’s map.**


    **👈 Navigate through the functionalities of the web application from the sidebar** 

    ### INSTRUCTIONS
    - Visit **DataAnalytics Section** to obtain forecast data and run necessary data visualizations. **Predict Yourself** feature can also be used. 
    - Visit the **Alert Message and Reporting Section** to generate cautionary messages card based on the forecasted AQI data. To disseminate the information to the citizens or to report an automated message to the Federal Government, use the email feature.
    - Visit the **Mapping Portal** to see the mapped AQI status of the available stations on Kathmandu Map. 
"""
)

