import streamlit as st
import datetime
import os
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

# Create a list of options for the dropdown
event_options = [
    "App Installed",
    "App Uninstalled",
    "Notification Clicked",
    "UTM Visited",
    "Advertisement Viewed",
    "Blog Views",
    "Book Now",
    "Call Merchant",
    "Charged",
    "Charged / Payment",
    "Checkout",
    "Choose City",
    "Choose City / Area",
    "Curated list button press/screen",
    "Curated List Tab",
    "Custom Ads click",
    "Successful Payment",
]


def get_clevertap_data(event_name, start_date, end_date):
    headers = {
        "X-CleverTap-Account-Id": st.secrets["CLEVERTAP_ACCOUNT_ID"],
        "X-CleverTap-Passcode": st.secrets["CLEVERTAP_PASSCODE"],
        "Content-Type": "application/json",
    }

    date_range = (
        f'"from":{start_date.strftime("%Y%m%d")},"to":{end_date.strftime("%Y%m%d")}'
    )
    data = '{"event_name":"' + event_name + '",' + date_range + "}"

    response = requests.post(
        "https://api.clevertap.com/1/counts/events.json", headers=headers, data=data
    )

    response_output = response.text
    # st.write("CleverTap API Response:")
    # st.write(response_output)  # Print the entire response for inspection

    json_obj = json.loads(response_output)
    req_id = json_obj["req_id"]

    response_f = requests.post(
        "https://api.clevertap.com/1/counts/events.json?req_id=" + req_id + "",
        headers=headers,
        data=data,
    )

    json_obj = json.loads(response_f.text)
    count_value = json_obj.get("count", 0)  # Extract the count value or default to 0

    return count_value


def get_technodata(event_name, from_date, to_date):
    # Headers using environment variables
    headers = {
        "X-CleverTap-Account-Id": st.secrets["CLEVERTAP_ACCOUNT_ID"],
        "X-CleverTap-Passcode": st.secrets["CLEVERTAP_PASSCODE"],
        "Content-Type": "application/json",
    }

    # Construct the groups object with proper property_type
    groups = {
        "Devices": {
            "property_type": "technographics",
            "name": "Device",
            # Optional: "top_n": 10,
            # Optional: "order": "desc"
        },
        "Operating System": {
            "property_type": "technographics",
            "name": "OS",
            # Optional: "top_n": 10,
            # Optional: "order": "desc"
        },
        "Browsers": {
            "property_type": "technographics",
            "name": "Browser",
            # Optional: "top_n": 10,
            # Optional: "order": "desc"
        },
        # Add more groups as needed
    }

    # Data payload as a dictionary
    data = {
        "event_name": event_name,
        "from": int(from_date_str),
        "to": int(to_date_str),
        "groups": groups,
    }
    # st.write(data)

    # Making the POST request to CleverTap
    response = requests.post(
        "https://api.clevertap.com/1/counts/top.json",
        headers=headers,
        json=data,  # Sends the dictionary as a JSON-formatted string
    )

    # Extract and print the response
    response_output = response.text

    # st.write("EVENT_NAME:", event_name)
    # st.write(response_output)

    # Extract and print the response
    json_obj = json.loads(response_output)
    req_id = json_obj["req_id"]

    response_f = requests.post(
        "https://api.clevertap.com/1/counts/top.json?req_id=" + req_id + "",
        headers=headers,
        data=data,
    )

    # st.write("EVENT_NAME: " + event_name)
    # st.write(response_f.text)

    json_obj = json.loads(response_f.text)
    # Extract relevant data for the bar chart
    flattened_data = {}

    for key, value in json_obj.items():
        if isinstance(value, dict) and "ENUM" in value:
            flattened_data[key] = value["ENUM"]
    # Create a bar chart in Streamlit
    st.bar_chart(flattened_data)
    # Convert data to DataFrame
    df = pd.DataFrame(flattened_data)

    # Save DataFrame to CSV
    csv_file_path = "output_technodata1_data.csv"
    df.to_csv(csv_file_path, index=False)

    # Provide a link to download the CSV
    st.markdown(f"Download the CSV file [here](sandbox:/path/to/{csv_file_path})")


def get_technodata_2(event_name, from_date, to_date):
    # Headers using environment variables
    headers = {
        "X-CleverTap-Account-Id": st.secrets["CLEVERTAP_ACCOUNT_ID"],
        "X-CleverTap-Passcode": st.secrets["CLEVERTAP_PASSCODE"],
        "Content-Type": "application/json",
    }

    # Construct the groups object with proper property_type
    groups = {
        "Mobile Devices": {
            "property_type": "app_fields",
            "name": "Model",
            # Optional: "top_n": 10,
            # Optional: "order": "desc"
        },
        "Mobile Makers": {
            "property_type": "app_fields",
            "name": "Make",
            # Optional: "top_n": 10,
            # Optional: "order": "desc"
        },
        # Add more groups as needed
    }

    # Data payload as a dictionary
    data = {
        "event_name": event_name,
        "from": int(from_date),
        "to": int(to_date),
        "groups": groups,
    }
    # st.write(data)

    # Making the POST request to CleverTap
    response = requests.post(
        "https://api.clevertap.com/1/counts/top.json",
        headers=headers,
        json=data,  # Sends the dictionary as a JSON-formatted string
    )

    # Extract and print the response
    response_output = response.text

    # st.write("EVENT_NAME:", event_name)
    # st.write(response_output)

    # Extract and print the response
    json_obj = json.loads(response_output)
    req_id = json_obj["req_id"]

    response_f = requests.post(
        "https://api.clevertap.com/1/counts/top.json?req_id=" + req_id + "",
        headers=headers,
        data=data,
    )

    # st.write("EVENT_NAME: " + event_name)
    # st.write(response_f.text)

    json_obj = json.loads(response_f.text)
    # Extract relevant data for the bar chart
    flattened_data = {}

    for category, values in json_obj.items():
        if category != "status" and "STR" in values:
            flattened_data[category] = values["STR"]

    # Create a bar chart in Streamlit
    st.bar_chart(flattened_data)

    # Convert data to DataFrame
    df = pd.DataFrame(flattened_data)

    # Save DataFrame to CSV
    csv_file_path = "output_technodata2_data.csv"
    df.to_csv(csv_file_path, index=False)

    # Provide a link to download the CSV
    st.markdown(f"Download the CSV file [here](sandbox:/path/to/{csv_file_path})")


# ===================================== Streamlit app    ===============================

# Streamlit app
st.title("CleverTap Event Analysis")

# Dropdown for selecting an event
selected_event = st.selectbox("Select an Event", event_options)

# Date range input for start date and end date
start_date = st.date_input("Select Start Date", datetime.date.today())
end_date = st.date_input(
    "Select End Date", datetime.date.today() + datetime.timedelta(days=7)
)

# Button to trigger CleverTap API and display results
if st.button("Get CleverTap Data"):
    with st.spinner("Fetching CleverTap Data..."):
        results = {}
        current_date = start_date

        while current_date <= end_date:
            formatted_date = current_date.strftime("%Y-%m-%d")
            result = get_clevertap_data(selected_event, current_date, current_date)
            results[formatted_date] = result
            current_date += datetime.timedelta(days=1)

    # Convert results to DataFrame for plotting
    df = pd.DataFrame(list(results.items()), columns=["Date", "CleverTap Data"])
    df["Date"] = pd.to_datetime(df["Date"])

    # Plotting line chart
    st.line_chart(df.set_index("Date"))

    # Display raw data
    st.write("Raw CleverTap Data:")
    st.write(df)

# Button to trigger Technodata API and display results
if st.button("Get Technodata"):
    with st.spinner("Fetching Technodata..."):
        # Convert dates to the format you want
        from_date_str = start_date.strftime("%Y%m%d")
        to_date_str = end_date.strftime("%Y%m%d")

        # Use from_date_str and to_date_str as needed in your function
        get_technodata(selected_event, from_date_str, to_date_str)
        get_technodata_2(selected_event, from_date_str, to_date_str)
