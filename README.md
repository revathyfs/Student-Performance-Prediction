# Student-Performance-Prediction

# Structure of the project

```
Student_Performance_Prediction/
│── app.py                  # Flask app with CRUD + ML prediction
│── student_model.pkl       # Saved ML model
│── students_train.csv      # CSV dataset (used for training)
│── student_model.ipynb     # Jupyter Notebook: EDA, training, model saving
│── env/                    # Python virtual environment
│── templates/
│   ├── base.html           # Common layout (navigation + CSS)
│   ├── index.html          # Display all students + CRUD buttons
│   ├── add_student.html    # Form to add a student
│   └── update_student.html # Form to update student
│── static/
│   └── style.css           # CSS styling
```
