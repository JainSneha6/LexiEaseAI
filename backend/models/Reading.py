import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import joblib

data = pd.read_csv('reading_passages.csv')

features = ['ReadingSpeedWPM', 'PronunciationErrors', 'Omissions', 'Insertions', 'Substitutions', 'Repetitions', 'Hesitations']
target = 'Fluency'

X = data[features]
y = data[target]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

joblib.dump(model, 'fluency_model.pkl')
print("Model training completed and saved as 'fluency_model.pkl'")