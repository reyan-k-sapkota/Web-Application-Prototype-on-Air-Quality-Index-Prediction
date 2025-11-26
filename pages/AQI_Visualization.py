import streamlit as st
from pages.Forecast_data import process_day_data
from pages.Forecast_data import process_day_data_phora
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

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

</style>
"""

st.markdown(page_bg_color, unsafe_allow_html=True)

algorithms = ["GBM", "CatBoost", "RFRegressor"]

st.title ("📈AQI DATA VISUALIZATION")
st.divider()

st.markdown(
    """
    **This functionality plots the hourly AQI values vs time for all the three algorithms.** The follwing visualization tools are employed: 
    - Line Chart
    - Heatmap
""")
st. divider()

formatted_date = datetime.now().strftime("%Y-%m-%d")  
date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")


st.subheader("A. FOR MAHARAJGUNJ")
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
for i, col in enumerate([col1, col2, col3, col4, col5, col6, col7], start = 1):
    selected_date3 = date_obj + timedelta(days=i - 1)
    date_label3 = selected_date3.strftime("%Y-%m-%d")
    if col.button(f"{date_label3}", use_container_width=True, key =f"Maharajgunj_Day{i}" ):
        
        
        
        st.write("Fetching data and plotting...")
        dataframes = process_day_data(i, algorithms)
        combined = pd.concat(dataframes, axis=0)
        
        plt.figure(figsize=(12, 6))
        for df, algo in zip(dataframes, algorithms):
            plt.plot(df["Hour"], df[f"AQI_{algo}"], marker="o", label=algo)
            
      

        plt.title(f"Hourly AQI for {date_label3}", fontsize=16)
        plt.xlabel("Hour of the Day", fontsize=12)
        plt.ylabel("AQI", fontsize=12)
        plt.legend(title="Algorithm")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt)
        plt.close()

        combined['Hour'] = pd.to_numeric(combined['Hour'], errors='coerce')
        heatmap_data = []
        for hour in sorted(combined["Hour"].unique()):
            row = [hour]  # Start with the hour
            for algo in algorithms:
                # Extract AQI value for the specific hour and algorithm
                aqi_value = combined.loc[
                    (combined["Hour"] == hour), f"AQI_{algo}"
                ].mean()  # Use mean if duplicates exist
                row.append(aqi_value)
            heatmap_data.append(row)

        # Create a DataFrame for the heatmap
        heatmap_df = pd.DataFrame(
            heatmap_data,
            columns=["Hour"] + algorithms
        ).set_index("Hour")

        # Plot the heatmap
        plt.figure(figsize=(10, 6))
        
        sns.heatmap(
            heatmap_df,
            annot=True,
            fmt=".1f",
            cmap="plasma",
            cbar_kws={"label": "AQI"},
        )

       
        plt.title(f"Heatmap of Hourly AQI for {date_label3}", fontsize=16)
        plt.xlabel("Algorithm", fontsize=12)
        plt.ylabel("Hour", fontsize=12)
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()

        
st.subheader("B. FOR PHORA DURBAR")
col1p, col2p, col3p, col4p, col5p, col6p, col7p = st.columns(7)
for i, colp in enumerate([col1p, col2p, col3p, col4p, col5p, col6p, col7p], start = 1):
    selected_date4 = date_obj + timedelta(days=i - 1)
    date_label4 = selected_date4.strftime("%Y-%m-%d")
    if colp.button(f"{date_label4}", use_container_width=True, key = f"Daysss{i}"):

        
        st.write("Fetching weather data and plotting...")
        dataframes_p = process_day_data_phora(i, algorithms)

        combined_p = pd.concat(dataframes_p, axis=0)
        
        plt.figure(figsize=(12, 6))
        for df, algo in zip(dataframes_p, algorithms):
            plt.plot(df["Hour"], df[f"AQI_{algo}"], marker="o", label=algo)

        plt.title(f"Hourly AQI for {date_label4}", fontsize=16)
        plt.xlabel("Hour of the Day", fontsize=12)
        plt.ylabel("AQI", fontsize=12)
        plt.legend(title="Algorithm")
        plt.grid(True, linestyle="--", alpha=0.7)
        plt.tight_layout()

        # Display the plot in Streamlit
        st.pyplot(plt)
        plt.close()

        combined_p['Hour'] = pd.to_numeric(combined_p['Hour'], errors='coerce')
        heatmap_data = []
        for hour in sorted(combined_p["Hour"].unique()):
            row = [hour]  # Start with the hour
            for algo in algorithms:
                # Extract AQI value for the specific hour and algorithm
                aqi_value = combined_p.loc[
                    (combined_p["Hour"] == hour), f"AQI_{algo}"
                ].mean()  # Use mean if duplicates exist
                row.append(aqi_value)
            heatmap_data.append(row)

        # Create a DataFrame for the heatmap
        heatmap_df = pd.DataFrame(
            heatmap_data,
            columns=["Hour"] + algorithms
        ).set_index("Hour")

        # Plot the heatmap
        plt.figure(figsize=(10, 6))
        
        sns.heatmap(
            heatmap_df,
            annot=True,
            fmt=".1f",
            cmap="plasma",
            cbar_kws={"label": "AQI"},
        )

       
        plt.title(f"Heatmap of Hourly AQI for {date_label4}", fontsize=16)
        plt.xlabel("Algorithm", fontsize=12)
        plt.ylabel("Hour", fontsize=12)
        plt.tight_layout()
        st.pyplot(plt)
        plt.close()

