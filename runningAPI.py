from flask import Flask, render_template, request
from main import formFunction
app = Flask(__name__)

top3Loc = []
resultDict = {}

@app.route('/')
def runMainPage():
    return render_template('homePage.html')


@app.route('/home')
def runHomePage():
    return render_template('homePage.html')


@app.route('/refugeeform', methods=['GET', 'POST'])
def runFormPage():
    return render_template('formPage.html')


@app.route('/results', methods=['GET', 'POST'])
def runResultPage():
    if request.method == 'POST':

        # collect data from form

        nameOfPrincipalApplicant = request.form['name']
        countryOfOrigin = request.form['countryoforigin']
        countryOfResettlement = request.form['countryofresettlement']
        familySize = request.form['familysize']
        YNchildren = request.form['YNchildren']
        childAges = request.form.getlist('childAge')
        YNdisab = request.form['YNdisab']
        disabType = request.form.getlist('disab')
        YNeld = request.form['YNeld']
        religion = request.form['religion']
        firstLang = request.form['firstLang']
        secondLang = request.form['secondLang']

        # apply data into form function

        resultDict, top3Loc = formFunction(countryOfResettlement, familySize, YNchildren, childAges, YNdisab, disabType,
                                           YNeld, religion)

        locDict = {}

        i = 0
        for loc in top3Loc:
            locDict["loc" + str(i)] = loc
            i += 1

        return render_template('resultPage.html', countryOfResettlement=countryOfResettlement, name=nameOfPrincipalApplicant, loc0=locDict["loc0"], loc1=locDict["loc1"], loc2=locDict["loc2"])


@app.route('/about')
def runAboutPage():
    return render_template('aboutPage.html')


@app.route('/readmoreforcities')
def runreadMoreofCities():

    return render_template('readMoreofCities.html')


if __name__ == "__main__":
    app.run()
