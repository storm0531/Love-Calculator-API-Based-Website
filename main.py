from flask import Flask ,render_template
from flask_wtf import FlaskForm
import requests
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

url = "https://love-calculator.p.rapidapi.com/getPercentage"
#set api_key as environment variable also get it from site itself
API_KEY = 'API key'
results_text = "undecided"
results_percentage = "X"

app = Flask(__name__)
#set you secrect key for crlf protection
app.config["SECRET_KEY"] = "SECRET KEYS"

class NameForm(FlaskForm):
    first_name = StringField("your name:",validators=[DataRequired()])
    sec_name = StringField("his/her name:",validators=[DataRequired()])
    submit = SubmitField("Submit")

@app.route("/",methods=["GET","POST"])
def request_home():
    global results_text, results_percentage

    form = NameForm()
    if form.validate_on_submit():
        querystring = {"fname": form.first_name.data, "sname": form.sec_name.data}
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": "love-calculator.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

        data = response.json()
        results_percentage = data["percentage"]
        results_text = data["result"]
        print(data)
    return render_template("index.html",form=form,results=results_text ,percentage = results_percentage)

if __name__ == "__main__":
    app.run(debug=True)