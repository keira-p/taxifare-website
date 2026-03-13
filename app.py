import datetime
import requests
import streamlit as st
import pandas as pd


'''
# @keira-p \\ TaxiFareModel :taxi:
'''

st.markdown('''
Tell us about your NYC ride and we'll predict your fare.
''')


# ==================================
# Get User Input
# ==================================
'''
#### When?
'''

# Date and time
#st.text_input(
    #label="Date and time of your ride:",
    #value="",
    #help="Use this format: YYYY-MM-DD hour:min:second",
    #icon= "⏰",
    ##placeholder="Example: 2026-03-13 09:44:00",
    #width="stretch")


event_time = st.datetime_input(
    ":alarm_clock: Date and time of your ride:",
    value=None
)

'''
#### Where?

**Tip**: Use [Google Maps](https://support.google.com/maps/answer/18539?hl=en-GB&co=GENIE.Platform%3DDesktop) to calculate your coordinates.
'''

# Pick up location
pickup_lat = st.text_input(
    label="Pick-up latitude:",
    value="40.73117398270109",
    placeholder="Example: 40.73117398270109",
    icon= "🏁",
    width="stretch")

pickup_long = st.text_input(
    label="Pick-up longitude:",
    value="-73.95354287650832",
    placeholder="Example: -73.95354287650832",
    icon= "🏁",
    width="stretch")

# Drop off location
dropoff_lat = st.text_input(
    label="Drop-off latitude:",
    value="40.78382299590267",
    placeholder="Example: 40.78382299590267",
    icon= "📍",
    width="stretch")

dropoff_long = st.text_input(
    label="Drop-off longitude:",
    value="-73.95909967625592",
    placeholder="Example: -73.95909967625592",
    icon= "📍",
    width="stretch")

'''
#### Who?
'''

# Passenger count
passengers = st.slider(":raising_hand_woman: How many passengers are in your ride?", 1, 10)


# ==================================
# Summary Details
# ==================================

'''
### Summary: Your ride details
'''
# date and time
if event_time:
    st.success(f"⏰ Ride scheduled for {event_time}")
else:
    st.warning("⚠️ No ride time selected")

# pick up
if pickup_lat and pickup_long:
    st.success(f"📍 Pick-up location: ({pickup_lat}, {pickup_long})")
else:
    st.warning("⚠️ Pick-up latitude and longitude required")

# drop off
if dropoff_lat and dropoff_long:
    st.success(f"📍 Drop-off location: ({dropoff_lat}, {dropoff_long})")
else:
    st.warning("⚠️ Drop-off latitude and longitude required")

# passengers
if passengers > 1:
    st.success(f"🙋‍♀️ {passengers} passengers")
else:
    st.success(f"🙋‍♀️ {passengers} passenger")

# map
if pickup_lat and pickup_long and dropoff_lat and dropoff_long:
    map_data = pd.DataFrame({
        "lat": [float(pickup_lat), float(dropoff_lat)],
        "lon": [float(pickup_long), float(dropoff_long)]
    })

    st.map(map_data)


# ==================================
# Call API to retrieve a prediction
# ==================================

url = "https://taxifare-248800634185.europe-west1.run.app/predict"

'''
### 💵 How much will it cost?
'''

if st.button("Predict my fare"):
    if event_time and pickup_lat and pickup_long and dropoff_lat and dropoff_long:
        try:
            params = {
                "pickup_datetime": event_time.strftime("%Y-%m-%d %H:%M:%S"),
                "pickup_longitude": float(pickup_long),
                "pickup_latitude": float(pickup_lat),
                "dropoff_longitude": float(dropoff_long),
                "dropoff_latitude": float(dropoff_lat),
                "passenger_count": passengers
            }

            response = requests.get(url, params=params)

            if response.status_code == 200:
                result = response.json()
                fare = result.get("fare", "No fare returned")
                st.success(f"💵 ${float(fare):.2f}")
            else:
                st.error(f"API request failed with status code {response.status_code}")
                st.write(response.text)

        except ValueError:
            st.error("Please enter valid numeric coordinates")
        except Exception as e:
            st.error(f"Something went wrong: {e}")
    else:
        st.warning("⚠️ Please complete all ride details before predicting")
