from flask import Flask, render_template
from main import formFunction
app = Flask(__name__)


@app.route('/')
def runHomePage():
    return render_template('homePage.html')

@app.route('/refugeeform', methods = ['GET', 'POST'])
def runFormPage():
    return render_template('formPage.html')

@app.route('/results', methods = ['GET', 'POST'])
def runResultPage():
    return render_template('resultPage.html')

if __name__ == "__main__":
    app.run()