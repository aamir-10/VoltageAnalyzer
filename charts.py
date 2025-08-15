import pandas as pd
import plotly.graph_objects as go
import numpy as np
from scipy.signal import find_peaks
def generate_charts():
    df = pd.read_csv("Sample_Data.csv")
    df['Timestamp'] = pd.to_datetime(df['Timestamp'])
    df = df.sort_values('Timestamp')

    charts = []

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=df['Timestamp'], y=df['Values'], mode='lines', name='Original Voltage'))
    df['MA_1000'] = df['Values'].rolling(1000).mean()
    df['MA_5000'] = df['Values'].rolling(5000).mean()
    fig1.add_trace(go.Scatter(x=df['Timestamp'], y=df['MA_1000'], name='1000-point MA', line=dict(color='red')))
    fig1.add_trace(go.Scatter(x=df['Timestamp'], y=df['MA_5000'], name='5000-point MA', line=dict(color='green')))
    fig1.update_xaxes(tickformat="%d-%m-%Y %H:%M:%S", ticklabelmode="instant",nticks=60, tickangle=90)
    charts.append((fig1,"Voltage Over Time"))

    df['MA_5'] = df['Values'].rolling(5).mean()
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df['Timestamp'], y=df['Values'], name='Original Values', line=dict(color='purple')))
    fig2.add_trace(go.Scatter(x=df['Timestamp'], y=df['MA_5'], name='5-Day MA', line=dict(color='orange')))
    fig2.update_xaxes(tickformat="%d-%m-%Y %H:%M:%S", ticklabelmode="instant",nticks=60, tickangle=90)
    charts.append((fig2, "5-Day Moving Average"))

    peaks, _ = find_peaks(df['Values'])
    lows, _ = find_peaks(-df['Values'])
    peak_tbl = df.iloc[peaks][['Timestamp', 'Values']].reset_index(drop=True)
    low_tbl = df.iloc[lows][['Timestamp', 'Values']].reset_index(drop=True)

    fig3 = go.Figure()
    fig3.add_trace(go.Scatter(x=df['Timestamp'], y=df['Values'], mode='lines', name='Original Values'))
    fig3.add_trace(go.Scatter(x=peak_tbl['Timestamp'], y=peak_tbl['Values'], mode='markers', name='Peaks', marker=dict(color='red', size=4)))
    fig3.add_trace(go.Scatter(x=low_tbl['Timestamp'], y=low_tbl['Values'], mode='markers', name='Lows', marker=dict(color='blue', size=4)))
    fig3.update_xaxes(tickformat="%d-%m-%Y %H:%M:%S", ticklabelmode="instant",nticks=60, tickangle=90)
    charts.append((fig3, "Peaks and Lows"))

    df['diff'] = df['Values'].diff()
    df['diff_change'] = df['diff'].diff()
    downward_acc = df[(df['diff'] < 0) & (df['diff_change'] < 0)]

    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(x=df['Timestamp'], y=df['Values'], mode='lines', name='Original Values'))
    fig4.add_trace(go.Scatter(x=downward_acc['Timestamp'], y=downward_acc['Values'], mode='markers',
                              name='Downward Acceleration', marker=dict(color='black', size=5, symbol='triangle-down')))
    fig4.update_xaxes(tickformat="%d-%m-%Y %H:%M:%S", ticklabelmode="instant",nticks=60, tickangle=90)
    charts.append((fig4, "Downward Acceleration"))

    return charts

