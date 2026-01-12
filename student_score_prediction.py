import csv

with open("student_scores.csv", mode = "r", newline = '') as f:
    reader = csv.DictReader(f)
    list_score = list(reader)

feauture = []
result = []
for record in list_score:
    study_hour = float(record["study_hours"].strip())
    sleeping_hours = float(record["sleep_hours"].strip())
    absences_day = int(record["absence_days"].strip())

    score = float(record["score"].strip())

    feauture.append([study_hour, sleeping_hours, absences_day])
    result.append(score)

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test =train_test_split(
    feauture,
    result,
    test_size = 0.2,
    random_state = 42
)

print(f"Train Size: {len(x_train)}, Test Size: {len(x_test)}")

#//////////////////////////////////////////////////////////////Model Training
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(x_train, y_train)

y_pred = model.predict(x_test) #Predict On Test Data 

for pred, actual in zip(y_test, y_pred):
    print(f"Predicted: {round(pred, 2)} Actual: {actual}")

score = model.score(x_test, y_test)
print(f"Model Score: {score}")

#//////////////////////////////////////////////////////////////Save The model
import joblib

joblib.dump(model, "student_score_model.pkl")
print("Model Saved Successfully")
