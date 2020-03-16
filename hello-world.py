from flask import Flask



app = Flask(__name__)
app.run(host='0.0.0.0', port=5000)
@app.route('/hello')
def helloIndex():
    return 'Hello World from Python Flask!'

    
app.run(host='0.0.0.0', port=5000)