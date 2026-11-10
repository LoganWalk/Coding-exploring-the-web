from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta
 
app = Flask(__name__)
app.config["DEBUG"] = True
 
# variables (names no longer match any function name)
out_type = None
start_num = None
first_double_hit = None
second_double_hit = None
third_double_hit = None
first_straight_hit = None
second_straight_hit = None
third_straight_hit = None
left_over = None
out_path_one = []
out_path_two = []
out_path_three = []
 
 
@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')
 
 
@app.route('/outs-page', methods=['GET'])
def outs_page():
    return render_template('out.html')
 
 
@app.route('/statistics-page', methods=['GET'])
def statistics_page():
    return render_template('statistics.html')
 
 
@app.route("/out-type", methods=["POST"])
def select_out_type():
    global out_type
    chosen = request.form.get("out_type")
    if chosen == "straight":
        out_type = "straight"
    elif chosen == "double":
        out_type = "double"
    return render_template('out.html')
 
 
@app.route("/first-num", methods=["POST"])
def enter_start_num():
    global start_num
    start_num = request.form.get("start")
 
    if out_type == "straight":
        match start_num:
            case 180:
                return
            case 1:
                return
            case n if int(n) > 180:
                return
            case n if int(n) > start_num:
                return
    elif out_type == "double":
        match start_num:
            case 170:
                return
            case 2:
                return
            case 1: 
                return
            case n if int(n) > 170 :
                return
            case n if int(n) > start_num:
                return
            
 
    return render_template('out.html')
 
 
@app.route("/first-dart-double", methods=["POST"])
def first_dart_double():
    global first_double_hit, left_over
    first_double_hit = request.form.get("hitDouble1")
    left_over = int(start_num) - int(first_double_hit)
    match left_over:
        case 0:
            return
        case 1:
            return
        case 100:
            return
        case n if (int(n) > 100):
            return
        case n if int(n) > left_over:
            return
            
    return render_template('out.html')
 
 
@app.route("/second-dart-double", methods=["POST"])
def second_dart_double():
    global second_double_hit
    second_double_hit = request.form.get("hitDouble2")
    left_over = int(start_num) - int(first_double_hit) - int(second_double_hit)
    match left_over:
        case 0:
            return
        case 1:
            return
        case 50:
            return
        case n if (int(n) > 50):
            return
        case n if int(n) > left_over:
            return
    
    
    
    
    
    return render_template('out.html')
@app.route("/third-dart-double", methods=["POST"])
def third_dart_double():
    global third_double_hit
    third_double_hit = request.form.get("hitDouble3")
    left_over = int(start_num) - int(first_double_hit) - int(second_double_hit) - int(third_double_hit)
    if(left_over == 0):
        return
    elif(left_over <= 1):
        return
    else:
        return 
    return render_template('out.html')
 
 
@app.route("/first-dart-straight", methods=["POST"])
def first_dart_straight():
    global first_straight_hit
    first_straight_hit = request.form.get("hitStraight1")
    left_over = int(start_num) - int(first_straight_hit)
    match left_over:
        case 0:
            return
        case 1:
            return
        case 120:
            return
        case n if (int(n) > 120):
            return
        case n if int(n) > left_over:
            return

    return render_template('out.html')
 
 
@app.route("/second-dart-straight", methods=["POST"])
def second_dart_straight():
    global second_straight_hit
    second_straight_hit = request.form.get("hitStraight2")
    left_over = int(start_num) - int(first_straight_hit) - int(second_straight_hit)
    match left_over:
        case 0:
            return
        case 1:
            return
        case 60:
            return
        case n if (int(n) > 60):
            return
        case n if int(n) > left_over:
            return
    return render_template('out.html')
 
 
@app.route("/third-dart-straight", methods=["POST"])
def third_dart_straight():
    global third_straight_hit
    third_straight_hit = request.form.get("hitStraight3")
    left_over = int(start_num) - int(first_straight_hit) - int(second_straight_hit) - int(third_straight_hit)
    if(left_over == 0):
        return
    elif(left_over < 0):
        return
    else:
        return
    return render_template('out.html')
 
 
if __name__ == "__main__":
    app.run(debug=True)
