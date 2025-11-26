import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from pages.alert_message import aqi_message_category, aqi_message_cautionary_statements, aqi_message_description, aqi_message_health
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from io import StringIO

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



def send_email(to_email, subject, html_message):
    # Email configuration
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "sapkotarex29@gmail.com"  # Replace with your email
    sender_password = "zwhi szsz uwqy dxzd"     # Replace with your email password

    try:
        # Set up the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        #msg.attach(MIMEText(message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))

        # Establish a connection and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"

def send_email_with_attachment(to_email, subject, html_message, attachment):
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "sapkotarex29@gmail.com"  # Replace with your email
    sender_password = "zwhi szsz uwqy dxzd"     # Replace with your email password

    try:
        # Set up the email content
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = subject
        #msg.attach(MIMEText(message, 'plain'))
        msg.attach(MIMEText(html_message, 'html'))

        for i, dataframe in enumerate(attachment, start=1):  # Enumerate to create filenames
            # Convert DataFrame to CSV in memory
            csv_buffer = StringIO()
            dataframe.to_csv(csv_buffer, index=False)
            csv_buffer.seek(0)

            # Generate a dynamic filename for each DataFrame
            filename = f"AQI_Report_{i}.csv"

            # Attach the CSV
            part = MIMEBase("application", "octet-stream")
            part.set_payload(csv_buffer.getvalue())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename={filename}"
            )
            msg.attach(part)

        

        # Establish a connection and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        return "Email sent successfully!"
    except Exception as e:
        return f"Failed to send email: {e}"


algorithms = ["GBM", "CatBoost", "RFRegressor"]

st.title("🍁ALERT MESSAGE/RECOMMENDATION GENERATION")
st.divider()

st.write("**AQI based Alert Message Generation and Automated Reporting System**")
st.markdown(
    """

    This functionality generates alert messages/recommendations based on the forecasted AQI values.
    - **Generate caution message/recommendation card for citizen**
    - **Information dissemination to the citizens of Kathmandu through email**
    - **Automated AQI status Reporting System.** The AQI status is reported to the concerned authorities of the Central Government
""")
st.divider()

st.title ("AUTOMATED ALERT MESSAGE GENERATION")
st.header("A. FOR STATION AT MAHARAJGUNJ")
st.divider()

median_algo0 = []
median_algo1 = []
median_algo2 = []
median_algo0_phora = []
median_algo1_phora = []
median_algo2_phora = []

max_algo0 = []
max_algo1 = []
max_algo2 = []
max_algo0_phora = []
max_algo1_phora = []
max_algo2_phora = []

min_algo0 = []
min_algo1 = []
min_algo2 = []
min_algo0_phora = []
min_algo1_phora = []
min_algo2_phora = []


formatted_date = datetime.now().strftime("%Y-%m-%d")  # Example format: YYYY-MM-DD
date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")

year = date_obj.year
month = date_obj.month
day = date_obj.day


def process_day_data_maharajgunj(i, algorithms):
    """Helper function to process data for a given day and algorithms."""
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
    """Helper function to process data for a given day and algorithms."""
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

#For Maharajgunj
for i in range (7):
    df1 = process_day_data_maharajgunj(i+1, algorithms)

    #numeric_values0 = [item.item() for item in df1[0]['AQI_GBM']]
    df1[0]['AQI_GBM'] = pd.to_numeric(df1[0]['AQI_GBM'])
    median_value0 = df1[0]['AQI_GBM'].median()
    max_value0=  df1[0]['AQI_GBM'].max()
    min_value0=  df1[0]['AQI_GBM'].min()
    median_algo0.append(median_value0)
    max_algo0.append(max_value0)
    min_algo0.append(min_value0)

    #numeric_values1 = [item.item() for item in df1[1]['AQI_CatBoost']]
    df1[1]['AQI_CatBoost'] = pd.to_numeric(df1[1]['AQI_CatBoost'])
    median_value1 = df1[1]['AQI_CatBoost'].median()
    max_value1 = df1[1]['AQI_CatBoost'].max()
    min_value1 = df1[1]['AQI_CatBoost'].min()
    median_algo1.append(median_value1)
    max_algo1.append(max_value1)
    min_algo1.append(min_value1)
    
    #numeric_values2 = [item.item() for item in df1[2]['AQI_RFRegressor']]
    df1[2]['AQI_RFRegressor'] = pd.to_numeric( df1[2]['AQI_RFRegressor'])
    median_value2 = df1[2]['AQI_RFRegressor'].median()
    max_value2 = df1[2]['AQI_RFRegressor'].max()
    min_value2 = df1[2]['AQI_RFRegressor'].min()
    median_algo2.append(median_value2)
    max_algo2.append(max_value2)
    min_algo2.append(min_value2)

#For Phora Durbar
for i in range (7):
    df1 = process_day_data_phora(i+1, algorithms)

    #numeric_values0 = [item.item() for item in df1[0]['AQI_GBM']]
    df1[0]['AQI_GBM'] = pd.to_numeric(df1[0]['AQI_GBM'])
    median_value0 = df1[0]['AQI_GBM'].median()
    max_value0=  df1[0]['AQI_GBM'].max()
    min_value0=  df1[0]['AQI_GBM'].min()
    median_algo0_phora.append(median_value0)
    max_algo0_phora.append(max_value0)
    min_algo0_phora.append(min_value0)

    #numeric_values1 = [item.item() for item in df1[1]['AQI_CatBoost']]
    df1[1]['AQI_CatBoost'] = pd.to_numeric(df1[1]['AQI_CatBoost'])
    median_value1 = df1[1]['AQI_CatBoost'].median()
    max_value1 = df1[1]['AQI_CatBoost'].max()
    min_value1 = df1[1]['AQI_CatBoost'].min()
    median_algo1_phora.append(median_value1)
    max_algo1_phora.append(max_value1)
    min_algo1_phora.append(min_value1)
    
    #numeric_values2 = [item.item() for item in df1[2]['AQI_RFRegressor']]
    df1[2]['AQI_RFRegressor'] = pd.to_numeric( df1[2]['AQI_RFRegressor'])
    median_value2 = df1[2]['AQI_RFRegressor'].median()
    max_value2 = df1[2]['AQI_RFRegressor'].max()
    min_value2 = df1[2]['AQI_RFRegressor'].min()
    median_algo2_phora.append(median_value2)
    max_algo2_phora.append(max_value2)
    min_algo2_phora.append(min_value2)


st.subheader("i. Displaying Median values for each alogorithm")
col1, col2, col3 = st.columns(3)

if col1.button("Using GradientBoostingRegressor"):
    col1.write(median_algo0)
    col1.write(max_algo0)
    col1.write(min_algo0)

if col2.button("Using CatBoostingRegressor"):
    col2.write(median_algo1)
    col2.write(max_algo1)
    col2.write(min_algo1)

if col3.button("Using Random Forest Regressor"):
    col3.write(median_algo2)
    col3.write(max_algo2)
    col3.write(min_algo2)

st.divider()
st.subheader("ii. Display the Status of Air Quality and generate alert/recommendation messages for Maharajgunj")


#returns a list for highest_aqi_hour for three algorithms respectively
def max_value_times_daily_maharajgunj(day):
    
    df = process_day_data_maharajgunj(day, algorithms)
    highest_aqi_hour = []
    for j in range (3):
        highest = df[j].loc[df[j][f'AQI_{algorithms[j]}'].idxmax()]
        hour = highest['Hour']
        
        highest_aqi_hour.append(hour)

    
    return highest_aqi_hour        

#returns a list for aqi value at specific hour of a specific day for three algorithms respectively
def value_at_specific_hour_maharajgunj(hour, day):
    df = process_day_data_maharajgunj(day, algorithms)
    aqi_value = []
    for j in range (3):
        aqi_at_hour = df[j].loc[df[j]['Hour'] == hour, f'AQI_{algorithms[j]}']
        
        aqi_value.append(aqi_at_hour.values)

    return aqi_value

formatted_date = datetime.now().strftime("%Y-%m-%d")  
date_obj = datetime.strptime(formatted_date, "%Y-%m-%d")

cl1, cl2, cl3, cl4, cl5, cl6, cl7 = st.columns(7)

for i, cols in enumerate([cl1, cl2, cl3, cl4, cl5, cl6, cl7], start =1):
    selected_date = date_obj + timedelta(days=i - 1)
    date_label = selected_date.strftime("%Y-%m-%d")
    
    if cols.button(f"{date_label}", use_container_width=True, key = f"Day{i}"):

        mean = (median_algo0[i-1] + median_algo1[i-1] + median_algo2[i-1] )/3
        largest = (max_algo0[i-1] + max_algo1[i-1] + max_algo2[i-1] )/3
        

        html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air Pollution Alert</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef2f3;
            color: #2e4053;
        }}
        .alert-container {{
            max-width: 650px;
            margin: 20px auto;
            border: 1px solid #ccc;
            border-radius: 8px;
            overflow: hidden;
            background-color: #ffffff;
        }}
        .header {{
            background-color: #ff6f61;
            color: #ffffff;
            text-align: center;
            padding: 15px 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 20px;
        }}
        .content h2 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #ff6f61;
        }}
        .content p {{
            margin: 10px 0;
            color: #2c3e50;
        }}
        .aqi-box {{
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            color: #fff;
            text-align: center;
        }}
        .unhealthy {{
            background-color: #ff6f61;
        }}
        .data-section {{
            margin: 20px 0;
        }}
        .data-section h3 {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #5bc0de;
        }}
        .data-section table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .data-section th, .data-section td {{
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }}
        .data-section th {{
            background-color: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            background-color: #f5f5f5;
            padding: 10px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="alert-container">
        <div class="header">
            <h1>Air Pollution Status Alert</h1>
            <p><strong>STATION</strong>: MAHRAJGUNJ</p>
            <p> {date_label}</p>
        </div>
        <div class="content">
            <h2>Today's Air Quality Index</h2>
            <div class="aqi-box unhealthy">
                <strong>Mean AQI: {round(mean,2)} </strong> {aqi_message_category(mean)}
            </div>
            <div class="data-section">
    <h3>Highest AQI and respective time</h3>
    <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Time</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Machine Learning Model</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">AQI Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(i)[0]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Gradient Boosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(i)[0], i)[0]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(i)[1]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">CatBoosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(i)[1], i)[1]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(i)[2]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Random Forest</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(i)[2], i)[2]}</td>
        </tr>
    </table>
</div>
            <h2>Health Alert</h2>
            <p>{aqi_message_health(mean)}</p>
            <h2>Description</h2>
            <p>{aqi_message_description(mean)}</p>
            <h2>Caution</h2>
            <p>{aqi_message_cautionary_statements(mean)}</p>
        </div>
        <div class="footer">
            <p>This is an automated alert message. Stay safe and take the necessary precautions.</p>
        </div>
    </div>
</body>
</html>

"""

        #st.write (f"Mean of AQI predicted from three algorithms: **{mean}**")
        #st.write (f"Largest value of AQI on day {i}: **{largest}**")
        st.divider()
        st.markdown(html_message, unsafe_allow_html=True)
        


st.divider()
st. subheader("B. FOR STATION AT PHORA DURBAR")

st.subheader("i. Displaying Median values for each alogorithm")

col1_p, col2_p, col3_p = st.columns(3)
if col1_p.button("Using GradientBoostingRegressor for phora"):
    col1_p.write(median_algo0_phora)
    col1_p.write(max_algo0_phora)
    col1_p.write(min_algo0_phora)

if col2_p.button("Using CatBoostingRegressor for phora"):
    col2_p.write(median_algo1_phora)
    col2_p.write(max_algo1_phora)
    col2_p.write(min_algo1_phora)

if col3_p.button("Using Random Forest Regressor for phora"):

    col3_p.write(median_algo2_phora)
    col3_p.write(max_algo2_phora)
    col3_p.write(min_algo2_phora)

st.divider()
st.subheader("ii. Display the Status of Air Quality and generate alert/recommendation messages for Maharajgunj")

#returns a list for highest_aqi_hour for three algorithms respectively
def max_value_hour_daily_phora(day):
    
    df = process_day_data_phora(day, algorithms)
    highest_aqi_hour = []
    for j in range (3):
        highest = df[j].loc[df[j][f'AQI_{algorithms[j]}'].idxmax()]
        hour = highest['Hour']
        
        highest_aqi_hour.append(hour)

    
    return highest_aqi_hour        

#returns a list for aqi value at specific hour of a specific day for three algorithms respectively
def value_at_specific_hour_phora(hour, day):
    df = process_day_data_phora(day, algorithms)
    aqi_value = []
    for j in range (3):
        aqi_at_hour = df[j].loc[df[j]['Hour'] == hour, f'AQI_{algorithms[j]}']
        
        aqi_value.append(aqi_at_hour.values)

    return aqi_value


cl1, cl2, cl3, cl4, cl5, cl6, cl7 = st.columns(7)

for i, cols in enumerate([cl1, cl2, cl3, cl4, cl5, cl6, cl7], start =1):
    selected_date = date_obj + timedelta(days=i - 1)
    date_label2 = selected_date.strftime("%Y-%m-%d")

    if cols.button(f"{date_label2}", use_container_width=True, key = f"Phora_Day{i}"):
        
        mean = (median_algo0_phora[i-1] + median_algo1_phora[i-1] + median_algo2_phora[i-1] )/3
        largest = (max_algo0_phora[i-1] + max_algo1_phora[i-1] + max_algo2_phora[i-1] )/3
    
        html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air Pollution Alert</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef2f3;
            color: #2e4053;
        }}
        .alert-container {{
            max-width: 650px;
            margin: 20px auto;
            border: 1px solid #ccc;
            border-radius: 8px;
            overflow: hidden;
            background-color: #ffffff;
        }}
        .header {{
            background-color: #ff6f61;
            color: #ffffff;
            text-align: center;
            padding: 15px 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 20px;
        }}
        .content h2 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #ff6f61;
        }}
        .content p {{
            margin: 10px 0;
            color: #2c3e50;
        }}
        .aqi-box {{
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            color: #fff;
            text-align: center;
        }}
        .unhealthy {{
            background-color: #ff6f61;
        }}
        .data-section {{
            margin: 20px 0;
        }}
        .data-section h3 {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #5bc0de;
        }}
        .data-section table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .data-section th, .data-section td {{
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }}
        .data-section th {{
            background-color: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            background-color: #f5f5f5;
            padding: 10px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="alert-container">
        <div class="header">
            <h1>Air Pollution Status Alert</h1>
            <p><strong>STATION</strong>: Phora Durbar</p>
            <p> {date_label2}</p>
        </div>
        <div class="content">
            <h2>Today's Air Quality Index</h2>
            <div class="aqi-box unhealthy">
                <strong>Mean AQI: {round(mean,2)} </strong> {aqi_message_category(mean)}
            </div>
            <div class="data-section">
    <h3>Highest AQI and respective time</h3>
    <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Time</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Machine Learning Model</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">AQI Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(i)[0]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Gradient Boosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(i)[0], i)[0]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(i)[1]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">CatBoosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(i)[1], i)[1]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(i)[2]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Random Forest</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(i)[1], i)[2]}</td>
        </tr>
    </table>
</div>
            <h2>Health Alert</h2>
            <p>{aqi_message_health(mean)}</p>
            <h2>Description</h2>
            <p>{aqi_message_description(mean)}</p>
            <h2>Caution</h2>
            <p>{aqi_message_cautionary_statements(mean)}</p>
        </div>
        <div class="footer">
            <p>This is an automated alert message. Stay safe and take the necessary precautions.</p>
        </div>
    </div>
</body>
</html>

"""

        



        #st.write (f"Mean of AQI predicted from three algorithms: **{mean}**")
        #st.write (f"Largest value of AQI on day {i}: **{largest}**")
        st.divider()
        #st.write(recommendation)
        st.markdown(html_message, unsafe_allow_html=True)
        



def alert_generator_maharajgunj(day1):
    
    mean = (median_algo0[day1-1] + median_algo1[day1-1] + median_algo2[day1-1])/3

    recommendation = f'''**Air Pollution Status in Station at US Embassy** 

Date: {month}/{day+day1-1}/{year}

The mean AQI value for {month}/{day+day1-1}/{year} is {mean}. The highest pollution level forecasted for today would occur at respective times:

i. **By Gradient Boosting :** {max_value_times_daily_maharajgunj(day1)[0]}:00----The AQI value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[0], day1)[0]}

ii. **By CatBoosting:** {max_value_times_daily_maharajgunj(day1)[1]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[1], day1)[1]}

iii. **By Random Forest:** {max_value_times_daily_maharajgunj(day1)[2]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[2], day1)[2]}
        
a. **Pollution Category For day average:** {aqi_message_category(mean)}

b. **Health Alert:** {aqi_message_health(mean)}
        
c. **Description**: {aqi_message_description(mean)}

d.. **Caution**: {aqi_message_cautionary_statements(mean)} 
        '''
    return recommendation
def alert_html_generator_maharajgunj(day1):
    
    mean = (median_algo0[day1-1] + median_algo1[day1-1] + median_algo2[day1-1])/3

    recommendation = f'''**Air Pollution Status in Station at US Embassy** 

Date: {month}/{day+day1-1}/{year}

The mean AQI value for {month}/{day+day1-1}/{year} is {mean}. The highest pollution level forecasted for today would occur at respective times:

i. **By Gradient Boosting :** {max_value_times_daily_maharajgunj(day1)[0]}:00----The AQI value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[0], day1)[0]}

ii. **By CatBoosting:** {max_value_times_daily_maharajgunj(day1)[1]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[1], day1)[1]}

iii. **By Random Forest:** {max_value_times_daily_maharajgunj(day1)[2]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[2], day1)[2]}
        
a. **Pollution Category For day average:** {aqi_message_category(mean)}

b. **Health Alert:** {aqi_message_health(mean)}
        
c. **Description**: {aqi_message_description(mean)}

d.. **Caution**: {aqi_message_cautionary_statements(mean)}
    
        '''
    
    html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air Pollution Alert</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef2f3;
            color: #2e4053;
        }}
        .alert-container {{
            max-width: 650px;
            margin: 20px auto;
            border: 1px solid #ccc;
            border-radius: 8px;
            overflow: hidden;
            background-color: #ffffff;
        }}
        .header {{
            background-color: #ff6f61;
            color: #ffffff;
            text-align: center;
            padding: 15px 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 20px;
        }}
        .content h2 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #ff6f61;
        }}
        .content p {{
            margin: 10px 0;
            color: #2c3e50;
        }}
        .aqi-box {{
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            color: #fff;
            text-align: center;
        }}
        .unhealthy {{
            background-color: #ff6f61;
        }}
        .data-section {{
            margin: 20px 0;
        }}
        .data-section h3 {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #5bc0de;
        }}
        .data-section table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .data-section th, .data-section td {{
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }}
        .data-section th {{
            background-color: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            background-color: #f5f5f5;
            padding: 10px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="alert-container">
        <div class="header">
            <h1>Air Pollution Status Alert</h1>
            <p><strong>STATION</strong>: MAHRAJGUNJ</p>
            <p> {month}/{day+day1-1}/{year}</p>
        </div>
        <div class="content">
            <h2>Today's Air Quality Index</h2>
            <div class="aqi-box unhealthy">
                <strong>Mean AQI: {mean} </strong> {aqi_message_category(mean)}
            </div>
            <div class="data-section">
    <h3>Highest AQI and respective time</h3>
    <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Time</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Machine Learning Model</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">AQI Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(day1)[0]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Gradient Boosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[0], day1)[0]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(day1)[1]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">CatBoosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[1], day1)[1]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(day1)[2]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Random Forest</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[2], day1)[2]}</td>
        </tr>
    </table>
</div>
            <h2>Health Alert</h2>
            <p>{aqi_message_health(mean)}</p>
            <h2>Description</h2>
            <p>{aqi_message_description(mean)}</p>
            <h2>Caution</h2>
            <p>{aqi_message_cautionary_statements(mean)}</p>
        </div>
        <div class="footer">
            <p>This is an automated alert message. Stay safe and take the necessary precautions.</p>
        </div>
    </div>
</body>
</html>

"""
    #return recommendation
    return html_message



def alert_generator_govt_maharajgunj(day1):
    mean = (median_algo0[day1-1] + median_algo1[day1-1] + median_algo2[day1-1])/3

    recommendation = f'''**Air Pollution Status in Station at US Embassy** 
    
Kathmandu Metropolitan City hereby reports the Air Quality Index Status and recommended alerts to the central government through this email. The detailed hourly AQI values for {month}/{day+day1-1}/{year}  are attached below.

Date: {month}/{day+day1-1}/{year}

The mean AQI value for {month}/{day+day1-1}/{year} is {mean}. The highest pollution level forecasted for today would occur at respective times:

i. **By Gradient Boosting :** {max_value_times_daily_maharajgunj(day1)[0]}:00----The AQI value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[0], day1)[0]}

ii. **By CatBoosting:** {max_value_times_daily_maharajgunj(day1)[1]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[1], day1)[1]}

iii. **By Random Forest:** {max_value_times_daily_maharajgunj(day1)[2]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[2], day1)[2]}
        
a. **Pollution Category For day average:** {aqi_message_category(mean)}

b. **Health Alert:** {aqi_message_health(mean)}
        
c. **Description**: {aqi_message_description(mean)}

d.. **Caution**: {aqi_message_cautionary_statements(mean)} 
        '''
    return recommendation

def alert_html_generator_govt_maharajgunj(day1):
    mean = (median_algo0[day1-1] + median_algo1[day1-1] + median_algo2[day1-1])/3
    html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air Pollution Alert</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef2f3;
            color: #2e4053;
        }}
        .alert-container {{
            max-width: 650px;
            margin: 20px auto;
            border: 1px solid #ccc;
            border-radius: 8px;
            overflow: hidden;
            background-color: #ffffff;
        }}
        .header {{
            background-color: #ff6f61;
            color: #ffffff;
            text-align: center;
            padding: 15px 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 20px;
        }}
        .content h2 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #ff6f61;
        }}
        .content p {{
            margin: 10px 0;
            color: #2c3e50;
        }}
        .aqi-box {{
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            color: #fff;
            text-align: center;
        }}
        .unhealthy {{
            background-color: #ff6f61;
        }}
        .data-section {{
            margin: 20px 0;
        }}
        .data-section h3 {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #5bc0de;
        }}
        .data-section table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .data-section th, .data-section td {{
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }}
        .data-section th {{
            background-color: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            background-color: #f5f5f5;
            padding: 10px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="alert-container">
        <div class="header">
            <h1>Air Pollution Reporting for Federal Government</h1>
            <p><strong>STATION</strong>: Maharajgunj</p>
            <p> {month}/{day+day1-1}/{year}</p>
        </div>
        <div class="content">
            <h2>Today's Air Quality Index</h2>
            <div class="aqi-box unhealthy">
                <strong>Mean AQI: {mean} </strong> {aqi_message_category(mean)}
            </div>
            <div class="data-section">
    <h3>Highest AQI and respective time</h3>
    <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Time</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Machine Learning Model</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">AQI Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(day1)[0]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Gradient Boosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[0], day1)[0]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(day1)[1]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">CatBoosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[1], day1)[1]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_times_daily_maharajgunj(day1)[2]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Random Forest</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[1], day1)[2]}</td>
        </tr>
    </table>
</div>
            <h2>Health Alert</h2>
            <p>{aqi_message_health(mean)}</p>
            <h2>Description</h2>
            <p>{aqi_message_description(mean)}</p>
            <h2>Caution</h2>
            <p>{aqi_message_cautionary_statements(mean)}</p>
        </div>
        <div class="footer">
            <p>This is an automated alert message. Stay safe and take the necessary precautions.</p>
        </div>
    </div>
</body>
</html>

"""
    return html_message


def alert_generator_phora(day1):
    
    mean = (median_algo0_phora[day1-1] + median_algo1_phora[day1-1] + median_algo2_phora[day1-1])/3

    recommendation = f'''**Air Pollution Status in Station at Phora Durbar** 

Date: {month}/{day+day1-1}/{year}

The mean AQI value for {month}/{day+day1-1}/{year} is {mean}. The highest pollution level forecasted for today would occur at respective times:

i. **By Gradient Boosting :** {max_value_hour_daily_phora(day1)[0]}:00----The AQI value is {value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[0], day1)[0]}

ii. **By CatBoosting:** {max_value_hour_daily_phora(day1)[1]}:00 --- The AQI Value is {value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[1], day1)[1]}

iii. **By Random Forest:** {max_value_hour_daily_phora(day1)[2]}:00 --- The AQI value is {value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[2], day1)[2]}
        
a. **Pollution Category For day average:** {aqi_message_category(mean)}

b. **Health Alert:** {aqi_message_health(mean)}
        
c. **Description**: {aqi_message_description(mean)}

d.. **Caution**: {aqi_message_cautionary_statements(mean)} 
        '''
    return recommendation

def alert_html_generator_phora(day1):
    
    mean = (median_algo0_phora[day1-1] + median_algo1_phora[day1-1] + median_algo2_phora[day1-1])/3

    recommendation = f'''**Air Pollution Status in Station at US Embassy** 

Date: {month}/{day+day1-1}/{year}

The mean AQI value for {month}/{day+day1-1}/{year} is {mean}. The highest pollution level forecasted for today would occur at respective times:

i. **By Gradient Boosting :** {max_value_times_daily_maharajgunj(day1)[0]}:00----The AQI value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[0], day1)[0]}

ii. **By CatBoosting:** {max_value_times_daily_maharajgunj(day1)[1]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[1], day1)[1]}

iii. **By Random Forest:** {max_value_times_daily_maharajgunj(day1)[2]}:00 --- The AQI Value is {value_at_specific_hour_maharajgunj(max_value_times_daily_maharajgunj(day1)[2], day1)[2]}
        
a. **Pollution Category For day average:** {aqi_message_category(mean)}

b. **Health Alert:** {aqi_message_health(mean)}
        
c. **Description**: {aqi_message_description(mean)}

d.. **Caution**: {aqi_message_cautionary_statements(mean)}
    
        '''
    
    html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air Pollution Alert</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef2f3;
            color: #2e4053;
        }}
        .alert-container {{
            max-width: 650px;
            margin: 20px auto;
            border: 1px solid #ccc;
            border-radius: 8px;
            overflow: hidden;
            background-color: #ffffff;
        }}
        .header {{
            background-color: #ff6f61;
            color: #ffffff;
            text-align: center;
            padding: 15px 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 20px;
        }}
        .content h2 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #ff6f61;
        }}
        .content p {{
            margin: 10px 0;
            color: #2c3e50;
        }}
        .aqi-box {{
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            color: #fff;
            text-align: center;
        }}
        .unhealthy {{
            background-color: #ff6f61;
        }}
        .data-section {{
            margin: 20px 0;
        }}
        .data-section h3 {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #5bc0de;
        }}
        .data-section table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .data-section th, .data-section td {{
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }}
        .data-section th {{
            background-color: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            background-color: #f5f5f5;
            padding: 10px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="alert-container">
        <div class="header">
            <h1>Air Pollution Status Alert</h1>
            <p><strong>STATION</strong>: Phora Durbar</p>
            <p> {month}/{day+day1-1}/{year}</p>
        </div>
        <div class="content">
            <h2>Today's Air Quality Index</h2>
            <div class="aqi-box unhealthy">
                <strong>Mean AQI: {mean} </strong> {aqi_message_category(mean)}
            </div>
            <div class="data-section">
    <h3>Highest AQI and respective time</h3>
    <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Time</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Machine Learning Model</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">AQI Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(day1)[0]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Gradient Boosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[0], day1)[0]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(day1)[1]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">CatBoosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[1], day1)[1]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(day1)[2]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Random Forest</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[1], day1)[2]}</td>
        </tr>
    </table>
</div>
            <h2>Health Alert</h2>
            <p>{aqi_message_health(mean)}</p>
            <h2>Description</h2>
            <p>{aqi_message_description(mean)}</p>
            <h2>Caution</h2>
            <p>{aqi_message_cautionary_statements(mean)}</p>
        </div>
        <div class="footer">
            <p>This is an automated alert message. Stay safe and take the necessary precautions.</p>
        </div>
    </div>
</body>
</html>

"""
    #return recommendation
    return html_message



def alert_generator_govt_phora(day1):

    mean = (median_algo0_phora[day1-1] + median_algo1_phora[day1-1] + median_algo2_phora[day1-1])/3

    recommendation = f'''**Air Pollution Status in Station at Phora Durbar** 
    
Kathmandu Metropolitan City hereby reports the Air Quality Index Status and recommended alerts to the central government through this email. The detailed hourly AQI values for {month}/{day+day1-1}/{year}  are attached below.

Date: {month}/{day+day1-1}/{year}

The mean AQI value for {month}/{day+day1-1}/{year} is {mean}. The highest pollution level forecasted for today would occur at respective times:

i. **By Gradient Boosting :** {max_value_hour_daily_phora(day1)[0]}:00----The AQI value is {value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[0], day1)[0]}

ii. **By CatBoosting:** {max_value_hour_daily_phora(day1)[1]}:00 --- The AQI Value is {value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[1], day1)[1]}

iii. **By Random Forest:** {max_value_hour_daily_phora(day1)[2]}:00 --- The AQI Value is {value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[2], day1)[2]}
        
a. **Pollution Category For day average:** {aqi_message_category(mean)}

b. **Health Alert:** {aqi_message_health(mean)}
        
c. **Description**: {aqi_message_description(mean)}

d.. **Caution**: {aqi_message_cautionary_statements(mean)} 
        '''
    return recommendation
def alert_html_generator_govt_phora(day1):
    mean = (median_algo0_phora[day1-1] + median_algo1_phora[day1-1] + median_algo2_phora[day1-1])/3
    html_message = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Air Pollution Alert</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #eef2f3;
            color: #2e4053;
        }}
        .alert-container {{
            max-width: 650px;
            margin: 20px auto;
            border: 1px solid #ccc;
            border-radius: 8px;
            overflow: hidden;
            background-color: #ffffff;
        }}
        .header {{
            background-color: #ff6f61;
            color: #ffffff;
            text-align: center;
            padding: 15px 20px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
        }}
        .content {{
            padding: 20px;
        }}
        .content h2 {{
            font-size: 20px;
            margin-bottom: 10px;
            color: #ff6f61;
        }}
        .content p {{
            margin: 10px 0;
            color: #2c3e50;
        }}
        .aqi-box {{
            margin: 20px 0;
            padding: 15px;
            border-radius: 5px;
            color: #fff;
            text-align: center;
        }}
        .unhealthy {{
            background-color: #ff6f61;
        }}
        .data-section {{
            margin: 20px 0;
        }}
        .data-section h3 {{
            font-size: 18px;
            margin-bottom: 10px;
            color: #5bc0de;
        }}
        .data-section table {{
            width: 100%;
            border-collapse: collapse;
        }}
        .data-section th, .data-section td {{
            border: 1px solid #ddd;
            text-align: left;
            padding: 8px;
        }}
        .data-section th {{
            background-color: #f8f9fa;
        }}
        .footer {{
            text-align: center;
            font-size: 12px;
            background-color: #f5f5f5;
            padding: 10px;
            color: #777;
        }}
    </style>
</head>
<body>
    <div class="alert-container">
        <div class="header">
            <h1>Air Pollution Status Reporting to Federal Government</h1>
            <p><strong>STATION</strong>: Phora Durbar</p>
            <p> {month}/{day+day1-1}/{year}</p>
        </div>
        <div class="content">
            <h2>Today's Air Quality Index</h2>
            <div class="aqi-box unhealthy">
                <strong>Mean AQI: {mean} </strong> {aqi_message_category(mean)}
            </div>
            <div class="data-section">
    <h3>Highest AQI and respective time</h3>
    <table style="width: 100%; border-collapse: collapse; border: 1px solid #ddd;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Time</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">Machine Learning Model</th>
            <th style="border: 1px solid #ddd; padding: 8px; text-align: left; color: #2c3e50">AQI Value</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(day1)[0]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Gradient Boosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[0], day1)[0]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(day1)[1]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">CatBoosting</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[1], day1)[1]}</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">{max_value_hour_daily_phora(day1)[2]}:00</td>
            <td style="border: 1px solid #ddd; padding: 8px; color:#2e4053">Random Forest</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: #d9534f;">{value_at_specific_hour_phora(max_value_hour_daily_phora(day1)[1], day1)[2]}</td>
        </tr>
    </table>
</div>
            <h2>Health Alert</h2>
            <p>{aqi_message_health(mean)}</p>
            <h2>Description</h2>
            <p>{aqi_message_description(mean)}</p>
            <h2>Caution</h2>
            <p>{aqi_message_cautionary_statements(mean)}</p>
        </div>
        <div class="footer">
            <p>This is an automated alert message. Stay safe and take the necessary precautions.</p>
        </div>
    </div>
</body>
</html>

"""
    return html_message



emails = "reyansapkota.108@gmail.com"

st.divider()
st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)



st.title("EMAIL DISSEMINATION SYSTEM")
st. divider()
st. title ("A. For Maharajgunj")
st.header("a. Send Email to the residents of Maharajgunj")


recipient = emails
option = st.selectbox(
    "Which day's AQI based Alert message would you like to generate?",
    (1, 2, 3, 4, 5, 6, 7),
    key = "box-1"
)
subject = "Warning about the Air Pollution in your region: Maharajgunj"
html_message_01 = alert_html_generator_maharajgunj(option)
submit_button = st.button("Send Email", key = "citizen")
    
if submit_button:
    if recipient and subject and html_message_01:
        result = send_email(recipient, subject, html_message_01)
        st.success(result) if "successfully" in result else st.error(result)
    else:
        st.error("Please fill in all fields.")
    
st. header ("b. Report the AQI Status to Federal Government")
recipient1 = "subedichiranjivee@gmail.com"
option1 = st.selectbox(
"Which day's AQI Reporting would you like to automate?",
    (1, 2, 3, 4, 5, 6, 7),
    key = "government"
)
    
subject1 = f"Federal Government Report: Reporting of Maharajgunj for Day{option1}"
html_message_02 = alert_html_generator_govt_maharajgunj(option1)
submit_button1 = st.button("Send Email to government", key = f"Government")
    
if submit_button1:
    if recipient1 and subject1 and html_message_02:
        result1 = send_email_with_attachment(recipient1, subject1, html_message_02, process_day_data_maharajgunj(option1, algorithms))
        st.success(result1) if "successfully" in result1 else st.error(result1)
    else:
        st.error("Please fill in all fields.")


st.divider()

st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='margin-bottom: -20px;'></div>", unsafe_allow_html=True)
st.title("B. For Phora Durbar")

st.header("a.Email Sender For residents of Phora Durbar")
recipient = "subedichiranjivee@gmail.com"
option = st.selectbox(
    "Which day's AQI based Alert message would you like to generate?",
    (1, 2, 3, 4, 5, 6, 7),
    key = "phora-select"
)
subject = f"Air Quality Status Alert for Citizens of Phora Durbar [Day{option}]"
html_message_03 = alert_html_generator_phora(option)
submit_button = st.button("Send Email", key = "phora-submit")

if submit_button:
    if recipient and subject and html_message_03:
        result = send_email(recipient, subject, html_message_03)
        st.success(result) if "successfully" in result else st.error(result)
    else:
        st.error("Please fill in all fields.")


st. header ("b. Report the AQI Status to Federal Government")
recipient1 = "079bce098.narayan@pcampus.edu.np"
option1 = st.selectbox(
    "Which day's AQI Reporting would you like to automate?",
    (1, 2, 3, 4, 5, 6, 7),
    key = "government-phora"
)

subject1 = f"Federal Government Report Reporting of day{option1}"
html_message_04 = alert_html_generator_govt_phora(option1)
submit_button1 = st.button("Send Email to government", key = "Government-phora")

if submit_button1:
    if recipient1 and subject1 and html_message_04:
        result1 = send_email_with_attachment(recipient1, subject1, html_message_04, process_day_data_phora(option1, algorithms))
        st.success(result1) if "successfully" in result1 else st.error(result1)
    else:
        st.error("Please fill in all fields.")


