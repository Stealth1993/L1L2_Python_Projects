import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import matplotlib.pyplot as plt

# Generate synthetic traffic data (e.g., number of active connections)
np.random.seed(42)
time_steps = 100
traffic = np.sin(np.linspace(0, 20, time_steps)) * 50 + 200  # Synthetic sinusoidal traffic data
traffic = traffic + 5 * np.random.randn(time_steps)  # Adding noise

# Prepare the data for LSTM
def create_dataset(series, window_size):
    X, y = [], []
    for i in range(len(series) - window_size):
        X.append(series[i:i+window_size])
        y.append(series[i+window_size])
    return np.array(X), np.array(y)

window_size = 10
X, y = create_dataset(traffic, window_size)
X = X.reshape((X.shape[0], X.shape[1], 1))

# Build the LSTM model
model = Sequential([
    LSTM(50, activation='relu', input_shape=(window_size, 1)),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# Train the model
model.fit(X, y, epochs=100, verbose=0)

# Forecast future traffic
predicted = model.predict(X)
plt.figure(figsize=(10, 5))
plt.plot(traffic[window_size:], label='Actual Traffic')
plt.plot(predicted, label='Predicted Traffic', linestyle='--')
plt.title('Network Traffic Forecasting using LSTM')
plt.xlabel('Time Step')
plt.ylabel('Traffic (Number of Connections)')
plt.legend()
plt.show()