from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["DEBUG"] = True

list_of_exercises = []
@app.route('/', methods=['GET'])
def index():
    return render_template('home.html')
@app.route('/workout-page', methods=['GET'])
def workout():
    return render_template('workout.html')
@app.route('/exercise-page', methods=['GET'])
def exercise():
    return render_template('exercise.html')
@app.route('/progress-page', methods=['GET'])
def progress():
    return render_template('progress.html')
@app.route('/about-page', methods=['GET'])
def about():
    return render_template('about.html')
@app.route('/store-input', methods=['POST'])
def store_input():
    exercise_name = request.form.get("exercise")
    rep_choice = request.form.get("rep_choice")
    
    if rep_choice == "1":
        raw_weight = request.form.get("weight_one")
    elif rep_choice == "3":
        raw_weight = request.form.get("weight_three")
    else:
        raw_weight = None
    
    rep_amount = int(rep_choice) if rep_choice else 0
    weight = int(raw_weight) if (raw_weight and raw_weight.isdigit()) else 0
    
    exercise = [exercise_name,rep_amount,weight]
    
    list_of_exercises.append(exercise)
    
    exercise.clear
    return render_template('exercise.html', items_list=list_of_exercises)
    
    



if __name__ == "__main__":
    app.run(debug=True)

            
            