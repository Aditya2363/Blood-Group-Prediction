import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import joblib

# Sample Data (Replace with actual dataset)
data = {
    'GeneA': [1, 2, 1, 2, 1, 2, 3, 3],
    'GeneB': [2, 1, 2, 1, 3, 3, 1, 2],
    'Antigen': [1, 2, 1, 2, 3, 3, 4, 4],
    'BloodGroup': ['A', 'B', 'A', 'B', 'AB', 'AB', 'O', 'O']
}

df = pd.DataFrame(data)

# Convert categorical labels to numerical values
df['BloodGroup'] = df['BloodGroup'].astype('category').cat.codes

# Split dataset
X = df.drop(columns=['BloodGroup'])
y = df['BloodGroup']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train Model
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# Save Model
joblib.dump(model, 'blood_group_model.pkl')

print("Model trained and saved successfully!")
