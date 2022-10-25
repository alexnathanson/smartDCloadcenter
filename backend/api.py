from flask import Flask, render_template, request
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
CORS(app)

systemData = {"system":{"modules":0,"loadBranches":0,"branchState":{1:0,2:0,3:0},"branchStatus":{1:0,2:0,3:0}},
            "pv":{"current":0,"voltage":0,"power":0},
                    "load":{"current":0,"voltage":0,"power":0}
                    }

userInput = {"load":
            {"branch1":{"status":0},
            "branch2":{"status":0},
            "branch3":{"status":0}}}

print("Starting Flask server...")

@app.route('/')
def main():
   return render_template('index.html')

@app.route('/api', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        postJSON = request.get_json()
        #print(postJSON)
        global systemData
        systemData = postJSON
        #print(systemData)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
    elif request.method == 'GET':

        if "user" in request.args.get('data'):
            response = userInput
        elif "system" in request.args.get('data'):
            response = systemData

        return response

#this route is for all user inputs
@app.route('/input', methods=['POST'])
def input():
    if request.method == 'POST':
        postJSON = request.get_json()

        # parsePost = postJSON.split(":")

        print(postJSON)
        global userInput
        userInput['load']['branch' + str(postJSON['branch'])]['status'] = postJSON['status']
        print(userInput)
        return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 

if __name__ == '__main__':
 	
    app.run()