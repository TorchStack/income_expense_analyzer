from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# import send_text
import extract_excel
from datetime import datetime
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

else:
    print('We in production')
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_NOTIFICATIONS'] = False

db = SQLAlchemy(app)


app.app_context().push()

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key= True)
    first_name = db.Column(db.String(200))
    last_name = db.Column(db.String(200))
    date_of_birth = db.Column(db.Date)

    def __init__(self, first_name, last_name, dob):
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = dob


with app.app_context():
    db.create_all()



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        date_of_birth = request.form['dob']
        f = request.files['excelfile']
        f.save(f.filename)
        print(first_name,last_name, date_of_birth)

        # Convert the date_of_birth string to a Python date object
        dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        if first_name == '' or last_name == '':
            return render_template('index.html', message='Please enter the required fields')
        if db.session.query(User).filter(User.first_name == first_name).count() == 0:
            data = User(first_name, last_name, dob)
            db.session.add(data)
            db.session.commit()
            data = extract_excel.read_excel_to_array(f.filename, 'Sheet1')
            return render_template('chart.html', data=data)
        
        
        data = extract_excel.read_excel_to_array(f.filename, 'Sheet1')
        return render_template('chart.html', data=data)

if __name__ == '__main__':
    app.run(host='localhost', port=3001)
