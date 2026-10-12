from flask import Flask, request, jsonify, render_template
from datetime import datetime, timedelta

app = Flask(__name__)
app.config["DEBUG"] = True

list_of_exercises = []
@app.route('/', methods=['GET'])
def index():
    return render_template('dashboard.html')
@app.route('/outs-page', methods=['GET'])
def workout():
    return render_template('out.html')
@app.route('/statistics-page', methods=['GET'])
def exercise():
    return render_template('statistics.html')



if __name__ == "__main__":
    app.run(debug=True)
