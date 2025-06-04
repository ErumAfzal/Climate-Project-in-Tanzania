import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import StringIO
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from statsmodels.tsa.seasonal import seasonal_decompose

st.set_page_config(layout='wide')
st.title("🌍 Climate Change Forecast - Tanzania (Africa Proxy)")

@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv'
    response = requests.get(url)
    df = pd.read_csv(StringIO(response.text))
    return df

data = load_data()

# Confirm required columns
required_cols = ['Date', 'Mean']
if 'Source' in data.columns and 'Year' in data.columns:
    data['Date'] = pd.to_datetime(data['Year'].astype(str) + '-' + data['Month'].astype(str).str.zfill(2))
    data = data.rename(columns={'Mean': 'Temperature'})
else:
    st.error("Dataset does not contain required 'Year' and 'Month' columns.")
    st.stop()

# Filter and clean
data = data[['Date', 'Temperature']]
data.dropna(inplace=True)
data = data.set_index('Date').resample('MS').mean().reset_index()

# Feature Engineering
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month
data['Season'] = data['Month'].apply(lambda x: 'Dry' if x in [6, 7, 8, 9] else 'Wet')

# Tabs
tab1, tab2, tab3 = st.tabs(["📈 Trend & Decomposition", "📊 Correlation & ML", "🔮 Forecasting Future"])

with tab1:
    st.subheader("Monthly Average Temperature Over Time")
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(data['Date'], data['Temperature'], color='orange', label='Avg Temp')
    ax.set_title("Temperature Trend Over Time (Africa Proxy)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    st.pyplot(fig)

    st.subheader("Seasonal Decomposition")
    try:
        seasonal_data = data.set_index('Date').asfreq('MS')
        decomp = seasonal_decompose(seasonal_data['Temperature'], model='additive', period=12)
        fig2 = decomp.plot()
        fig2.set_size_inches(12, 8)
        st.pyplot(fig2)
    except Exception as e:
        st.error(f"Seasonal decomposition failed: {e}")

with tab2:
    st.subheader("Correlation Heatmap")
    corr = data[['Temperature', 'Year', 'Month']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    st.pyplot(fig)

    st.subheader("Train Machine Learning Models")
    features = data[['Year', 'Month']]
    target = data['Temperature']
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

    # Linear Regression
    lr = LinearRegression()
    lr.fit(X_train, y_train)
    lr_preds = lr.predict(X_test)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_preds))

    # Random Forest
    rf = RandomForestRegressor(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    rf_preds = rf.predict(X_test)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_preds))
    rf_r2 = r2_score(y_test, rf_preds)

    st.write(f"📉 **Linear Regression RMSE**: {lr_rmse:.4f}")
    st.write(f"🌲 **Random Forest RMSE**: {rf_rmse:.4f}")
    st.write(f"🌲 **Random Forest R² Score**: {rf_r2:.4f}")

with tab3:
    st.subheader("Forecasting Monthly Temperatures (2025-2030)")

    future_years = pd.DataFrame({
        'Year': list(range(2025, 2031)) * 12,
        'Month': sorted(list(range(1, 13)) * 6)
    })
    future_preds = rf.predict(future_years)
    future_dates = pd.date_range(start='2025-01', end='2030-12', freq='MS')

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(future_dates, future_preds, label='Forecasted Temperature', color='green')
    ax.set_title("Forecasted Monthly Temperatures (2025–2030)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Predicted Temp (°C)")
    ax.legend()
    st.pyplot(fig)
