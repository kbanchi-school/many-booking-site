from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('hello.html')

@app.route('/kazunori')
def kazunori():
    return render_template('kazunori.html')

@app.route('/aoi')
def aoi():
    return render_template('aoi.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
