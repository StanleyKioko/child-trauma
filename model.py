import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix

# Load the data
df = pd.read_excel(r"C:\Users\HP\Desktop\Fourth Year project\Code Deploymet\Childtraumadata.xlsx")

# Trim whitespace from column names
df.columns = df.columns.str.strip()

# Display the first few rows
print(df.head())

# Check for missing values
print(df.isna().sum())

# Fill missing values
df.fillna(method='ffill', inplace=True)
df.fillna(method='bfill', inplace=True)

# Verify no missing values remain
print(df.isna().sum())

# Display dataframe info
print(df.shape)
print(df.columns)
print(df.head())
print(df.info())
print(df.describe())
print(df.dtypes)

# Drop columns with all values missing (ensure they exist)
columns_to_drop = ['recovery_time', 'duration_of_symptoms', 'quality_of_life', 'cognitive_functioning']
existing_columns_to_drop = [col for col in columns_to_drop if col in df.columns]
df = df.drop(columns=existing_columns_to_drop)

# Feature selection
# Ensure 'trauma_stage' exists in the DataFrame
if 'trauma_stage' not in df.columns:
    raise KeyError("'trauma_stage' column not found in the DataFrame")
    
X = df.drop(columns=['trauma_stage'])
y = df['trauma_stage']

# Convert categorical variables to numeric
X = pd.get_dummies(X, drop_first=True)

# Feature selection using chi-squared test
selector = SelectKBest(score_func=chi2, k=10)
X_new = selector.fit_transform(X, y)

# Get selected feature names
selected_features = X.columns[selector.get_support()]
print("Selected Features:", selected_features)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X[selected_features], y, test_size=0.2, random_state=42)

# Standardize the features (if necessary)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

print("Data preparation complete.")

# Initialize and train the model
model = RandomForestClassifier(random_state=42)
model.fit(X_train_scaled, y_train)

# Make predictions
y_pred = model.predict(X_test_scaled)

# Evaluate the model
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Save the trained model to a file
joblib.dump(model, 'random_forest_model.pkl')
