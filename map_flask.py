from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, url_for, flash, redirect, request, abort
import requests


app = Flask(__name__)
app.secret_key = "Secret Key"


@app.route('/')
def home():
    return render_template('map_design.html')


@app.route('/update_api', methods=['GET', 'POST'])
def update_api():
    if request.method == 'POST':
        user_address = request.form.get('user_address')
        if user_address != "":
            url = 'https://nominatim.openstreetmap.org/search/' + request.form.get('user_address') + '?format=json'
            response = requests.get(url).json()
            if not response:
                flash('Location not found, please try again', 'danger')
            else: 
                result_address = response[0]["display_name"]
                result_latitude = response[0]["lat"]
                result_longitude = response[0]["lon"]
                return render_template('map_design.html', result_address=result_address, result_latitude=result_latitude, result_longitude=result_longitude, user_address = request.form.get('user_address'))
        else: 
            flash('Please suggest some location', 'warning')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
