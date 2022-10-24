from flask import Flask, render_template

app = Flask(__name__)

print("Starting Flask server...")

@app.route('/')
def main():
   return render_template('index.html')

@app.route('/api', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('success', name=user))
    else:
        user = request.args.get('nm')
        return redirect(url_for('success', name=user))

if __name__ == '__main__':
 	
    app.run()