import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# Step 1: Load data
df = pd.read_csv('brkb.csv', parse_dates=['date'], index_col='date')

# Step 2: Define volatility function
def calc_vol(data, window):
    X = np.log(data['adjClose'] / data['adjClose'].shift(1))
    X.fillna(0, inplace=True)
    vol = X.rolling(window=window).std() * np.sqrt(252)
    return vol

# Step 3: Compute volatilities
vol_20 = calc_vol(df, 20)
vol_30 = calc_vol(df, 30)
vol_180 = calc_vol(df, 180)

# Step 4: Scale price
price_scaled = (df['adjClose'] - df['adjClose'].min()) / (df['adjClose'].max() - df['adjClose'].min())

# Step 5: Set up plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=price_scaled, mode='lines', name='BRK.B Price (Scaled)', line=dict(color='#FF6B6B', width=2)))
fig.add_trace(go.Scatter(x=df.index, y=vol_20, mode='lines', name='20-Day Vol', line=dict(color='#4ECDC4', width=2, dash='dash')))
fig.add_trace(go.Scatter(x=df.index, y=vol_30, mode='lines', name='30-Day Vol', line=dict(color='#4ECDC4', width=2, dash='dash')))
fig.add_trace(go.Scatter(x=df.index, y=vol_180, mode='lines', name='180-Day Vol', line=dict(color='#4ECDC4', width=2, dash='dash')))

# Step 6: Adjust layout
fig.update_layout(
    title='BRK.B Realized Volatility vs Price (2022-02-28 to 2024-10-31)',
    xaxis_title='Date',
    yaxis_title='Volatility / Scaled Price',
    plot_bgcolor='rgb(40, 40, 40)',
    paper_bgcolor='rgb(40, 40, 40)',
    font=dict(color='white'),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
    margin=dict(l=50, r=50, t=50, b=50),
    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', gridwidth=0.5),
    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', gridwidth=0.5)
)

# Step 7: Show plot
fig.show()