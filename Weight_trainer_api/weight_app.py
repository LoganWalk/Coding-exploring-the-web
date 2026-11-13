from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config["DEBUG"] = True
global list_of_exercises
global rep_amount
global weight
global reps
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
@app.route('/schedule-page', methods=['GET'])
def schedule():
    return render_template('schedule.html')
@app.route('/store-input', methods=['POST'])
def store_input():
    rep_amount = 0
    weight = 0
    exercise_name = request.form.get("exercise")
    rep_choice = request.form.get("rep_choice")
    typeOfExercise = request.form.get("type_of_workout")
    muscleTargeted = request.form.get("muscle")
    
    if muscleTargeted :
        muscleTargeted = muscleTargeted
    else:
        muscleTargeted = "None"
    
    if rep_choice == "1":
        raw_weight = request.form.get("weight_one")
    elif rep_choice == "3":
        raw_weight = request.form.get("weight_three")
    else:
        raw_weight = None
        
    if typeOfExercise == "bodyWeight":
        maxReps = request.form.get("max_reps")
        
        rep_amount = int(maxReps) if maxReps and maxReps.isdigit() else 0
    elif typeOfExercise == "Cardio":
        maxTime = request.form.get("max_time")
        rep_amount = int(maxTime) if maxTime and maxTime.isdigit() else 0
    elif typeOfExercise == "Bands":
        bandStrength = request.form.get("band_strength")
        weight = int(bandStrength) if bandStrength and bandStrength.isdigit() else 0

    elif rep_choice == "1" or rep_choice == "3":
        typeOfExercise = "freeWeight/Machine"
        rep_amount = int(rep_choice) if rep_choice else 0
        weight = int(raw_weight) if (raw_weight and raw_weight.isdigit()) else 0
    
    exercise = [exercise_name,rep_amount,weight,typeOfExercise,muscleTargeted]
    
    list_of_exercises.append(exercise)
    with open("exercises.json", "w") as file:
        json.dump(list_of_exercises, file, indent=4)
    
    exercise.clear
    return render_template('exercise.html', items_list=list_of_exercises)
@app.route('/workout-exercises', methods = ['POST'])
def workout_exercises():
    try:
        with open("exercises.json", "r") as file:
            saved_exercises = json.load(file)
    except FileNotFoundError:
        saved_exercises = []

    changed_weights_list = []
    
    for item in saved_exercises:
        exercise_name, rep_amount, current_weight, typeOfExercise, muscleTargeted = item
        if(typeOfExercise == "freeWeight/Machine"):
            if rep_amount == 1:
                workout_weight = round(((current_weight * 0.85)/5) * 5)
            elif rep_amount == 3:
                workout_weight = round(((current_weight * 0.9)/5) * 5)
            else:
                workout_weight = current_weight
            reps = 5
        elif(typeOfExercise == "bodyWeight"):
            reps = (int)(rep_amount * 0.6)
        elif(typeOfExercise == "Cardio"):
            reps = (int)(rep_amount * 0.7)
        elif(typeOfExercise == "Bands"):
            workout_weight = (int)(current_weight * 0.85)
            reps = 5
    changed_exercise = {
          "exercise_name": exercise_name,
          "target_reps":reps,
          "original_weight": current_weight,
          "workout_weight": workout_weight,
          "typeOfExercise": typeOfExercise,
          "muscleTargeted": muscleTargeted
      }
    changed_weights_list.append(changed_exercise)
    with open("exercises.json", "w") as file:
        json.dump(changed_weights_list, file, indent=4)
         
          
    return render_template('workout.html', items_list=changed_weights_list)
@app.route('/signin-page', methods = ['GET'])
def signin():
    return render_template('signin.html')
@app.route('/api/exercises', methods=['GET'])
def get_exercises():
    try:
        with open("exercises.json", "r") as file:
            saved_exercises = json.load(file)
    except FileNotFoundError:
        saved_exercises = []

    exercise_dicts = []
    for item in saved_exercises:
        name, rep_amount, weight, type_of_exercise, muscle = item
        exercise_dicts.append({
            "name": name,
            "type": type_of_exercise,
            "muscle": muscle
        })

    return jsonify(exercise_dicts)


@app.route('/api/workouts', methods=['POST'])
def save_workout():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data received"}), 400

    title = (data.get("title") or "").strip()
    supersets = data.get("supersets", [])

    if not title:
        return jsonify({"error": "Title required"}), 400
    if not supersets:
        return jsonify({"error": "Add at least one super set"}), 400

    try:
        with open("workouts.json", "r") as file:
            workouts = json.load(file)
    except FileNotFoundError:
        workouts = []

    workouts.append({"title": title, "supersets": supersets})

    with open("workouts.json", "w") as file:
        json.dump(workouts, file, indent=4)

    return jsonify({"message": "Saved"}), 201
    
    



if __name__ == "__main__":
    app.run(debug=True)


            
            