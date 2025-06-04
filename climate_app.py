import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

st.set_page_config(page_title="Tanzania Climate Analysis", layout="wide")
st.title(" Climate Change Analysis - Tanzania")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ErumAfzal/Climate-Project-in-Tanzania/main/chart.csv"
    df = pd.read_csv(url)

    # Display column names for debugging
    st.write("Available columns:", df.columns.tolist())

    # Rename for clarity
    df.rename(columns={
        'Average Mean Surface Air Temperature': 'Temperature',
        'Category': 'MonthName'
    }, inplace=True)

    # Convert MonthName to month number
    month_map = {
        'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
        'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
        'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12
    }
    df['Month'] = df['MonthName'].map(month_map)
    df['Year'] = 2025  # Assign a default or dummy year

    # Ensure temperature is numeric
    df['Temperature'] = pd.to_numeric(df['Temperature'], errors='coerce')
    df.dropna(subset=['Temperature'], inplace=True)

    return df

df = load_data()

if not df.empty:
    # Sidebar Inputs
    st.sidebar.header("User Input")
    month = st.sidebar.slider('Select Month', 1, 12, 1)
    year = 2025  # fixed dummy year

    # Train model
    features = df[['Year', 'Month']]
    target = df['Temperature']

    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    prediction = model.predict([[year, month]])[0]

    # Display result
    st.subheader("📈 Forecasted Temperature")
    st.write(f"Predicted Avg Temperature for **{year}-{month:02d}**: 🌡️ **{prediction:.2f} °C**")

    # Historical Trend Chart
    if st.checkbox("📊 Show Temperature Trend by Month"):
        st.line_chart(df[['Month', 'Temperature']].set_index('Month').sort_index())

    # Footer
    st.markdown("---")
    st.caption("Data Source: [World Bank Climate Portal](https://github.com/ErumAfzal/Climate-Project-in-Tanzania)")
else:
    st.warning("No data available to display.")
