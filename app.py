from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import joblib

# ---------------- Flask Config ----------------
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Database Model ----------------
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    math = db.Column(db.Float, nullable=False)
    science = db.Column(db.Float, nullable=False)
    english = db.Column(db.Float, nullable=False)
    history = db.Column(db.Float, nullable=False)
    computer = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)   # auto-calculated
    performance = db.Column(db.String(50))

# ---------------- Load ML Model ----------------
model = joblib.load("student_model.pkl")

# ---------------- Routes ----------------
@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

# Add Student + Predict Performance
@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        math = float(request.form['math'])
        science = float(request.form['science'])
        english = float(request.form['english'])
        history = float(request.form['history'])
        computer = float(request.form['computer'])

        total = math + science + english + history + computer

        # ML model predicts based on total (and maybe age)
        prediction = model.predict([[age, total]])[0]
        new_student = Student(
            name=name, 
            age=age, 
            math=math,
            science=science,
            english=english,
            history=history,
            computer=computer,
            total=total,
            performance=prediction)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

# Update Student
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    student = Student.query.get_or_404(id)   # safer: returns 404 if not found

    if request.method == 'POST':
        student.name = request.form['name']
        student.age = int(request.form['age'])

        # Update subject marks
        student.math = float(request.form['math'])
        student.science = float(request.form['science'])
        student.english = float(request.form['english'])
        student.history = float(request.form['history'])
        student.computer = float(request.form['computer'])

        # Recalculate total
        student.total = (
            student.math + 
            student.science + 
            student.english + 
            student.history + 
            student.computer
        )

        # Predict new performance using ML model
        student.performance = model.predict(
            [[student.age, student.total]]
        )[0]

        # Save changes
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('update_student.html', student=student)

# Delete Student
@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)