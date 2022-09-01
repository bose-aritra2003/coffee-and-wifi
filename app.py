from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField, URLField
from wtforms.validators import InputRequired, URL
import csv

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'any-string-you-want-just-keep-it-secret'
Bootstrap(app)

coffee_ratings = ["☕️", "☕️☕️", "☕️☕️☕️", "☕️☕️☕️☕️", "☕️☕️☕️☕️☕️"]
wifi_strengths = ["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"]
power_sockets = ["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"]


class CafeForm(FlaskForm):
    cafe = StringField(
        "Cafe name",
        validators=[InputRequired()]
    )
    location = URLField(
        "Cafe Location on Google Maps (URL)",
        validators=[InputRequired(), URL()]
    )
    open = TimeField(
        "Opening Time",
        validators=[InputRequired()]
    )
    close = TimeField(
        "Closing Time",
        validators=[InputRequired()]
    )
    coffee_rating = SelectField(
        "Coffee Rating",
        choices=coffee_ratings,
        validators=[InputRequired()]
    )
    wifi_rating = SelectField(
        "Wifi Strength Rating",
        choices=wifi_strengths,
        validators=[InputRequired()]
    )
    power_rating = SelectField(
        "Power Socket Availability",
        choices=power_sockets,
        validators=[InputRequired()]
    )
    submit = SubmitField(
        'Submit'
    )


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    cafe_form = CafeForm()
    if cafe_form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as csv_file:
            csv_file.write(f"\n{cafe_form.cafe.data},"
                           f"{cafe_form.location.data},"
                           f"{cafe_form.open.data.strftime('%I:%M %p')},"
                           f"{cafe_form.close.data.strftime('%I:%M %p')},"
                           f"{cafe_form.coffee_rating.data},"
                           f"{cafe_form.wifi_rating.data},"
                           f"{cafe_form.power_rating.data}")
        return redirect(url_for('cafes'))
    return render_template('add.html', form=cafe_form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
