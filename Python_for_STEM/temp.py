import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import IsolationForest

# Generate synthetic network KPI data (latency in ms)
np.random.seed(42)
normal_data = 50 + 10 * np.random.randn(200)  # Normal latency values
anomalies = np.array([100, 110, 95])  # Abnormally high latency values
data = np.concatenate([normal_data, anomalies])
data = data.reshape(-1, 1)

# Create and fit the Isolation Forest model
iso_forest = IsolationForest(contamination=0.02, random_state=42)
predictions = iso_forest.fit_predict(data)

# Separate normal points and anomalies
normal_points = data[predictions == 1]
anomaly_points = data[predictions == -1]

# Visualize the results
plt.figure(figsize=(10, 5))
plt.scatter(range(len(normal_points)), normal_points, color='green', label='Normal')
plt.scatter(np.where(predictions == -1), anomaly_points, color='red', label='Anomalies')
plt.title('Anomaly Detection in Network Latency')
plt.xlabel('Data Point Index')
plt.ylabel('Latency (ms)')
plt.legend()
plt.show()
