import streamlit as st
import requests
from datetime import date

# Streamlit UI elements for input
st.title("Receipt Scan Forecaster")

# Input: Select a start date
start_date = st.date_input("Select a start date:", min_value=date(2022, 1, 1), max_value=date(2022, 12, 31), value=date(2022, 1, 1))

# Input: Select an end date
end_date = st.date_input("Select an end date:", min_value=date(2022, 1, 1), max_value=date(2022, 12, 31), value=date(2022, 1, 1))

if st.button("Calculate"):
    # Convert date objects to ISO formatted strings
    start_date_str = start_date.isoformat()
    end_date_str = end_date.isoformat()

    # Send requests to FastAPI with port 8080
    api_url = "http://localhost:8080/predict/"
    request_payload_start = {"date": start_date_str}
    request_payload_end = {"date": end_date_str}

    response_start = requests.post(api_url, json=request_payload_start)
    response_end = requests.post(api_url, json=request_payload_end)

    if response_start.status_code == 200 and response_end.status_code == 200:
        result_start = response_start.json()
        result_end = response_end.json()

        # Extract predicted values
        predicted_value_start = result_start['predicted_value']
        predicted_value_end = result_end['predicted_value']

        # Calculate the total receipts scanned during the period
        total_predicted_value = int((predicted_value_start + predicted_value_end) * (end_date-start_date).days)

        st.write(f"Projection of total Receipt scans over this period is: {total_predicted_value}")
    else:
        st.write("Error calculating date difference. Please try again.")
