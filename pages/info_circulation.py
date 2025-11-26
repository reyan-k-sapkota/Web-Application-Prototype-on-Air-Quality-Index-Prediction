import streamlit as st
import folium

from streamlit_folium import st_folium
import pandas as pd
from folium.plugins import MarkerCluster
from datetime import datetime
from pages.alert_message_new import process_day_data_phora
from pages.alert_message_new import process_day_data_maharajgunj




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

st.title("🗺️KATHMANDU MAP VISUALIZATION")
st.divider()

st.write("**Mapping of the hourly predicted AQI values on the map of Kathmandu**")
st.markdown(
    """

    This functionality allows the Kathmandu Metro to monitor hourly predicted values of AQI on the map of Kathmandu.
""")
st.divider()



maharajgunj = [27.7364, 85.3304]
ratnapark = [27.7062, 85.3151]
phora_durbar = [27.7174, 85.3197]
khumaltaar = [27.6536, 85.3285]

formatted_date = datetime.now().strftime("%Y-%m-%d")  # Example format: YYYY-MM-DD
date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")

year = date_obj.year
month = date_obj.month
day = date_obj.day


algorithms = ["GBM", "CatBoost", "RFRegressor"]

hour_from_input = st.slider("Select Hour", min_value=0, max_value=23, value=1, )
day_from_input = st.selectbox("Which day's mapping would you like to generate?",
    (1, 2, 3, 4, 5, 6, 7),)

dataframe_maharajgunj = process_day_data_maharajgunj(day_from_input, algorithms)
dataframe_phora = process_day_data_phora(day_from_input, algorithms)
#dataframe_ratnapark = process_day_data_ratnapark(day_from_input, algorithms)
#dataframe_khumaltaar = process_day_data_khumaltaar(day_from_input, algorithms)


m = folium.Map(location=[27.7172, 85.3165], zoom_start=20)

marker_cluster = MarkerCluster().add_to(m)

dataframe_maharajgunj[2]["Hour"] = dataframe_maharajgunj[2]["Hour"].astype(int)
dataframe_phora[2]["Hour"] = dataframe_phora[2]["Hour"].astype(int)
#dataframe_ratnapark[2]["Hour"] = dataframe_ratnapark[2]["Hour"].astype(int)
#dataframe_khumaltaar[2]["Hour"] = dataframe_khumaltaar[2]["Hour"].astype(int)

filtered_df = dataframe_maharajgunj[2][dataframe_maharajgunj[2]["Hour"] == hour_from_input]
filtered_df_phora = dataframe_phora[2][dataframe_phora[2]["Hour"] == hour_from_input]
#filtered_df_ratnapark = dataframe_ratnapark[2][dataframe_ratnapark[2]["Hour"] == hour_from_input]
#filtered_df_khumaltaar = dataframe_khumaltaar[2][dataframe_khumaltaar[2]["Hour"] == hour_from_input]

c1, c2 = st.columns(2)

c1.write(filtered_df)
c2.write (filtered_df_phora)
#st.write(filtered_df_ratnapark)
#st.write (filtered_df_khumaltaar)



filtered_df = filtered_df.copy()
filtered_df['Lat'] =  27.7364789
filtered_df['Lon'] = 85.3304212

#filtered_df.loc[:, 'Lon'] = 85.3310
#filtered_df.loc[:, 'Lat'] = 27.7320

#filtered_df['Lon'] = 85.3310


if filtered_df.empty or filtered_df_phora.empty:
    st.warning("No AQI data available for the selected hour.")
else:
    # Create a Folium map centered at an average location
    
    m = folium.Map(location= maharajgunj, zoom_start=14)

    # Add markers to the map
    for _, row in filtered_df.iterrows():
        color1 = (
        "green" if row['AQI_RFRegressor'] <= 50 else
        "yellow" if row['AQI_RFRegressor'] <= 100 else
        "orange" if row['AQI_RFRegressor'] <= 150 else
        "red" if row['AQI_RFRegressor'] <= 200 else
        "purple" if row['AQI_RFRegressor'] <= 300 else
        "maroon"
    )
        folium.CircleMarker(
            location=maharajgunj,
            popup=f"Maharajgunj AQI: {row['AQI_RFRegressor']} (Hour: {row['Hour']})",
            radius =25,
            color = color1,
            fill = True,
            fill_color = color1,
            fill_opacity = 0.7,
            tooltip=f"AQI: {row['AQI_RFRegressor']}",
        ).add_to(m)
        folium.Marker(
            location=maharajgunj,
            popup=f"AQI: {row['AQI_RFRegressor']} (Hour: {row['Hour']})",
            tooltip = f"Maharajgunj",
            icon=folium.Icon(
                icon = "cloud",
                color="red" if row["AQI_RFRegressor"] > 150 else "green",
            )
        ).add_to(m)
           
    



    for _, row in filtered_df_phora.iterrows():

        color1 = (
        "green" if row['AQI_RFRegressor'] <= 50 else
        "yellow" if row['AQI_RFRegressor'] <= 100 else
        "orange" if row['AQI_RFRegressor'] <= 150 else
        "red" if row['AQI_RFRegressor'] <= 200 else
        "purple" if row['AQI_RFRegressor'] <= 300 else
        "maroon")


        folium.CircleMarker(
            location=phora_durbar,
            popup=f"Phora Durbar AQI: {row['AQI_RFRegressor']} (Hour: {row['Hour']})",
            radius =25,
            color = color1,
            fill = True,
            fill_color = color1,
            fill_opacity = 0.7,
            tooltip=f"AQI: {row['AQI_RFRegressor']}",
        ).add_to(m)

        folium.Marker(
            location=phora_durbar,
            popup=f"AQI: {row['AQI_RFRegressor']} (Hour: {row['Hour']})",
            tooltip="Phora Durbar",
            icon=folium.Icon(
                icon = "cloud",
                color="red" if row["AQI_RFRegressor"] > 150 else "green")
        ).add_to(m)


    st.write(f"Map showing AQI: **Hour {hour_from_input}**")
    st_folium(m, width=800, height=600)


