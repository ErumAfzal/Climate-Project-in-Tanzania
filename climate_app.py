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

# Configure Streamlit page
st.set_page_config(page_title="Tanzania Climate Change Analysis", layout="wide")
st.title("🌍 Climate Change Analysis - Tanzania (Africa Proxy)")

# Load Data
@st.cache_data
def load_data():
    url = 'https://raw.githubusercontent.com/datasets/global-temp/master/data/monthly.csv'
    response = requests.get(url)
    data = pd.read_csv(StringIO(response.text))
    return data

data = load_data()

# Check required columns
if 'Mean' in data.columns and 'Date' in data.columns or 'Year' in data.columns:
    if 'Year' in data.columns:
        data['Date'] = pd.to_datetime(data['Year'], errors='coerce')
    else:
        data['Date'] = pd.to_datetime(data['Date'], errors='coerce')

    data.rename(columns={'Mean': 'Temperature'}, inplace=True)
    data = data[['Date', 'Temperature']].dropna()
    data = data.set_index('Date').resample('MS').mean().reset_index()
    data['Year'] = data['Date'].dt.year
    data['Month'] = data['Date'].dt.month
    data['Season'] = data['Month'].apply(lambda x: 'Dry' if x in [6,7,8,9] else 'Wet')
else:
    st.error("Required columns not found in dataset.")
    st.stop()

# Show raw data
if st.checkbox("🔍 Show Raw Data"):
    st.write(data.head())

# Exploratory Data Analysis
st.subheader("📊 Temperature Trend Over Time")
fig1, ax1 = plt.subplots(figsize=(14, 6))
ax1.plot(data['Date'], data['Temperature'], label='Monthly Avg Temperature', color='orange')
ax1.set_title('Temperature Trend (Africa Region Proxy)')
ax1.set_xlabel('Date')
ax1.set_ylabel('Temperature (°C)')
ax1.grid(True)
ax1.legend()
st.pyplot(fig1)

# Seasonal Decomposition
st.subheader("🌀 Seasonal Decomposition")
data_indexed = data.set_index('Date').asfreq('MS')
decomp = seasonal_decompose(data_indexed['Temperature'], model='additive', period=12)
fig2 = decomp.plot()
st.pyplot(fig2)

# Correlation Heatmap
st.subheader("📈 Correlation Heatmap")
fig3, ax3 = plt.subplots()
corr = data[['Temperature', 'Year', 'Month']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax3)
st.pyplot(fig3)

# Machine Learning
st.subheader("🤖 Temperature Prediction Models")

features = data[['Year', 'Month']]
target = data['Temperature']
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
lr_preds = lr.predict(X_test)

# Random Forest
rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
rf_preds = rf.predict(X_test)

# Evaluation Metrics
st.markdown("**Model Evaluation Metrics**")
col1, col2, col3 = st.columns(3)
col1.metric("Linear Reg. RMSE", f"{np.sqrt(mean_squared_error(y_test, lr_preds)):.3f}")
col2.metric("RF RMSE", f"{np.sqrt(mean_squared_error(y_test, rf_preds)):.3f}")
col3.metric("RF R² Score", f"{r2_score(y_test, rf_preds):.3f}")

# Forecast Future Temps
st.subheader("🔮 Forecast Future Temperatures (2025–2030)")

future_years = pd.DataFrame({
    'Year': list(range(2025, 2031)) * 12,
    'Month': sorted(list(range(1, 13)) * 6)
})
future_preds = rf.predict(future_years)
future_dates = pd.date_range(start='2025-01', end='2030-12', freq='MS')

fig4, ax4 = plt.subplots(figsize=(14, 6))
ax4.plot(future_dates, future_preds, label='Predicted Temp (2025–2030)', color='green')
ax4.set_title('Forecasted Monthly Temperatures (Africa Region Proxy)')
ax4.set_xlabel('Year')
ax4.set_ylabel('Predicted Temperature (°C)')
ax4.grid(True)
ax4.legend()
st.pyplot(fig4)

# Footer
st.markdown("---")
st.caption("Data Source: [Berkeley Earth - Global Temperature Data](https://github.com/datasets/global-temp)")
