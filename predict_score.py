import joblib

#Load the model
model=joblib.load("student_score_model.pkl")
print("Model Loaded Successfully")

#Predict The Score
student_data =[8,7,2]
predicted_score = model.predict([student_data])

print(f"Predicted Score: {round(predicted_score[0], 2)}")
