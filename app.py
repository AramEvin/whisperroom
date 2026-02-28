from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = '098f6bcd4621d373cade4e832627b4f6'

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0') 
