import streamlit as st
import pandas as pd

st.set_page_config(page_title="Tanzania Climate Analysis", layout="wide")
st.title("🌍 Climate Change Analysis - Tanzania")

@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/ErumAfzal/Climate-Project-in-Tanzania/main/chart.csv"
    df = pd.read_csv(url)

    # Display available columns
    st.write("Available columns:", df.columns.tolist())

    # Rename columns for consistency
    df.rename(columns={'Average Mean Surface Air Temperature': 'Temperature'}, inplace=True)

    # Check for necessary columns
    required_columns = ['Year', 'Temperature']
    for col in required_columns:
        if col not in df.columns:
            st.error(f"Missing required column: {col}")
            return pd.DataFrame()

    # Drop rows with missing values
    df.dropna(subset=required_columns, inplace=True)

    # Convert 'Year' to integer
    df['Year'] = df['Year'].astype(int)

    # Add a dummy 'Month' column for modeling purposes
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

    from sklearn.ensemble import RandomForestRegressor
    from sklearn.model_selection import train_test_split

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
