import streamlit as st
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

st.set_page_config(page_title="Tanzania Climate Analysis", layout="wide")
st.title("🌍 Climate Change Analysis - Tanzania")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ErumAfzal/Climate-Project-in-Tanzania/main/chart.csv"
    df = pd.read_csv(url)
    
    # Ensure column names match expected
    df = df.rename(columns={'AverageTemperature': 'Temperature'})

    # Drop rows with missing values
    df = df.dropna(subset=['Year', 'Temperature'])
    df['Year'] = df['Year'].astype(int)
    
    # Since we have only yearly data, create a dummy 'Month' column for modeling
    df['Month'] = 6  # Assuming mid-year average

    return df

df = load_data()

if not df.empty:
    # Sidebar Inputs
    st.sidebar.header("User Input")
    year = st.sidebar.slider('Select Year', int(df['Year'].min()), int(df['Year'].max()), int(df['Year'].min()))

    # Use dummy month
    month = 6

    # Train model
    features = df[['Year', 'Month']]
    target = df['Temperature']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    prediction = model.predict([[year, month]])[0]

    # Display result
    st.subheader("📈 Forecasted Temperature")
    st.write(f"Predicted Avg Temperature for **{year}**: 🌡️ **{prediction:.2f} °C**")

    # Show historical trend
    if st.checkbox("📊 Show Historical Temperature Trends"):
        avg_annual = df.groupby('Year')['Temperature'].mean().reset_index()
        st.line_chart(avg_annual.set_index('Year'))

    # Footer
    st.markdown("---")
    st.caption("Data Source: [World Bank Climate Portal](https://github.com/ErumAfzal/Climate-Project-in-Tanzania)")
else:
    st.warning("No data available to display.")
