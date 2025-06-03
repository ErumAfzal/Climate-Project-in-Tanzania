# climate_app.py

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Streamlit Page Config
st.set_page_config(page_title="Climate Forecast for Tanzania", layout="centered")
st.title("🌍 Climate Change Forecast - Tanzania (Africa Proxy)")

# Load and preprocess the data
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv'
    data = pd.read_csv(url)

    # Ensure 'Date' column exists
    if 'Date' not in data.columns or 'Mean' not in data.columns:
        raise ValueError("Required columns 'Date' and 'Mean' not found in dataset")

    # Use only 'GCAG' source to avoid duplication
    data = data[data['Source'] == 'GCAG']

    # Convert date and rename Mean
    data['Date'] = pd.to_datetime(data['Date'])
    data.rename(columns={'Mean': 'Temperature'}, inplace=True)

    # Drop missing values
    data = data.dropna(subset=['Temperature'])

    # Extract Year and Month
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month

    return data[['Year', 'Month', 'Temperature']]

# Load data
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

# Predict
prediction = model.predict([[year, month]])[0]

# Display result
st.subheader("📈 Forecasted Temperature")
st.write(f"Predicted Avg Temperature for **{year}-{month:02d}**: 🌡️ **{prediction:.2f} °C**")

# Historical trends checkbox
if st.checkbox("📊 Show Historical Temperature Trends"):
    avg_annual = df.groupby('Year')['Temperature'].mean().reset_index()
    st.line_chart(avg_annual.set_index('Year'))

# Footer
st.markdown("---")
st.caption("Data Source: [Berkeley Earth Global Temperature Dataset](https://github.com/datasets/global-temp)")
