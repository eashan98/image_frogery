from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('page1.html')

@app.route('/history')
def history():
    return render_template('history.html')

if __name__ == '__main__':
    app.run(debug=True)
