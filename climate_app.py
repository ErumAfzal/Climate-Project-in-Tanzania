# climate_app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Climate Forecast for Tanzania", layout="centered")
st.title("🌍 Climate Change Forecast - Tanzania (Africa Proxy)")

@st.cache_data
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv'
    data = pd.read_csv(url)

    # Ensure 'Year' and 'Month' columns exist and create a proper datetime
    if 'Year' in data.columns and 'Month' in data.columns:
        data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' + data['Month'].astype(str).str.zfill(2))
    else:
        # If only 'Date' or something else is available, fall back or raise an error
        raise ValueError("Required columns 'Year' and 'Month' not found in dataset")

    data.rename(columns={'Mean': 'Temperature'}, inplace=True)
    data.dropna(subset=['Temperature'], inplace=True)

    data = data.set_index('Date').resample('MS').mean().reset_index()
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month

    return data[['Year', 'Month', 'Temperature']]


df = load_data()

# Train model
features = df[['Year', 'Month']]
target = df['Temperature']
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Sidebar Inputs
st.sidebar.header("User Input")
year = st.sidebar.slider('Select Year', 2025, 2035, 2025)
month = st.sidebar.slider('Select Month', 1, 12, 1)

prediction = model.predict([[year, month]])[0]

# Display result
st.subheader("📈 Forecasted Temperature")
st.write(f"Predicted Avg Temperature for **{year}-{month:02d}**: 🌡️ **{prediction:.2f} °C**")

# Show historical trend
if st.checkbox("📊 Show Historical Temperature Trends"):
    avg_annual = df.groupby('Year')['Temperature'].mean().reset_index()
    st.line_chart(avg_annual.set_index('Year'))

# Footer
st.markdown("---")
st.caption("Data Source: [Berkeley Earth Global Temperature Dataset](https://github.com/datasets/global-temp)")
