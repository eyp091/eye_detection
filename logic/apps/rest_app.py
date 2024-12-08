import sys
sys.path.append('C:/Users/escan/Desktop/python_folder_structure/logic')

from flask import Flask, render_template, redirect, url_for, jsonify
from utils.rest_area_finder import findNearesRestArea
import threading
import webbrowser

app = Flask(__name__, template_folder='../../ui')

def openBrowser():
    webbrowser.open("http://127.0.0.1:5000/")

@app.route('/rest_area')
def restAreas():
    places = findNearesRestArea()
    return render_template("rest_areas.html", places=places)

@app.route('/send_message')
def sendMessage():
    message = "SURUCU YORGUUUUNNNN!!!!"
    return jsonify({"status": "success", "message": message})

@app.route('/')
def index():
    return redirect(url_for('restAreas'))

if __name__ == "__main__":
    #threading.Timer(1, openBrowser).start()
    app.run(debug=True, host='0.0.0.0', port=5000)