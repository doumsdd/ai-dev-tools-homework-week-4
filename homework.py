import pandas as pd
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# ============================================================
# Q1. Download the data and check number of columns
# ============================================================
print("=" * 60)
print("Q1: Downloading data and checking columns")
print("=" * 60)

url_jan = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-01.parquet"
url_feb = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-02.parquet"

df_jan = pd.read_parquet(url_jan)
df_feb = pd.read_parquet(url_feb)

print(f"January data shape: {df_jan.shape}")
print(f"Number of columns in January: {len(df_jan.columns)}")
print(f"Columns: {list(df_jan.columns)}")

# ============================================================
# Q2. Computing duration (in minutes)
# ============================================================
print("\n" + "=" * 60)
print("Q2: Computing duration")
print("=" * 60)

df_jan['duration'] = (df_jan['tpep_dropoff_datetime'] - df_jan['tpep_pickup_datetime']).dt.total_seconds() / 60

std_duration = df_jan['duration'].std()
print(f"Standard deviation of duration in January: {std_duration:.2f}")

# ============================================================
# Q3. Dropping outliers (keep 1-60 minutes inclusive)
# ============================================================
print("\n" + "=" * 60)
print("Q3: Dropping outliers")
print("=" * 60)

total_before = len(df_jan)
df_jan_filtered = df_jan[(df_jan['duration'] >= 1) & (df_jan['duration'] <= 60)]
total_after = len(df_jan_filtered)
fraction = total_after / total_before
print(f"Before: {total_before}, After: {total_after}")
print(f"Fraction remaining: {fraction:.4f} ({fraction*100:.2f}%)")

# ============================================================
# Q4. One-hot encoding
# ============================================================
print("\n" + "=" * 60)
print("Q4: One-hot encoding")
print("=" * 60)

# Convert location IDs to strings
features_train = df_jan_filtered[['PULocationID', 'DOLocationID']].copy()
features_train['PULocationID'] = features_train['PULocationID'].astype(str)
features_train['DOLocationID'] = features_train['DOLocationID'].astype(str)

# Turn into list of dicts
dicts_train = features_train.to_dict(orient='records')

# Fit DictVectorizer
dv = DictVectorizer()
dv.fit(dicts_train)
X_train = dv.fit_transform(dicts_train)

print(f"Dimensionality of feature matrix: {X_train.shape}")
print(f"Number of columns: {X_train.shape[1]}")

# ============================================================
# Q5. Training a model
# ============================================================
print("\n" + "=" * 60)
print("Q5: Training a model")
print("=" * 60)

y_train = df_jan_filtered['duration'].values

lr = LinearRegression()
lr.fit(X_train, y_train)

y_pred_train = lr.predict(X_train)
rmse_train = np.sqrt(mean_squared_error(y_train, y_pred_train))
print(f"RMSE on train: {rmse_train:.2f}")

# ============================================================
# Q6. Evaluating the model on validation (February 2023)
# ============================================================
print("\n" + "=" * 60)
print("Q6: Evaluating on validation")
print("=" * 60)

# Compute duration for February
df_feb['duration'] = (df_feb['tpep_dropoff_datetime'] - df_feb['tpep_pickup_datetime']).dt.total_seconds() / 60

# Filter outliers
df_feb_filtered = df_feb[(df_feb['duration'] >= 1) & (df_feb['duration'] <= 60)]

# Prepare features
features_val = df_feb_filtered[['PULocationID', 'DOLocationID']].copy()
features_val['PULocationID'] = features_val['PULocationID'].astype(str)
features_val['DOLocationID'] = features_val['DOLocationID'].astype(str)

dicts_val = features_val.to_dict(orient='records')
X_val = dv.transform(dicts_val)
y_val = df_feb_filtered['duration'].values

y_pred_val = lr.predict(X_val)
rmse_val = np.sqrt(mean_squared_error(y_val, y_pred_val))
print(f"RMSE on validation: {rmse_val:.2f}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Q1: Number of columns = {len(df_jan.columns)}")
print(f"Q2: Std of duration = {std_duration:.2f}")
print(f"Q3: Fraction remaining = {fraction*100:.2f}%")
print(f"Q4: Dimensionality = {X_train.shape[1]}")
print(f"Q5: RMSE on train = {rmse_train:.2f}")
print(f"Q6: RMSE on validation = {rmse_val:.2f}")
