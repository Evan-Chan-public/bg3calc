from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '<placeholder>'  #for if i ever want flash to work
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class FormData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    strn = db.Column(db.Integer, nullable=False)
    dext = db.Column(db.Integer, nullable=False)
    cons = db.Column(db.Integer, nullable=False)
    intl = db.Column(db.Integer, nullable=False)
    wisd = db.Column(db.Integer, nullable=False)
    char = db.Column(db.Integer, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)
    pointbuy = db.Column(db.String(100))
    strmod = db.Column(db.Integer)
    dexmod = db.Column(db.Integer)
    conmod = db.Column(db.Integer)
    intmod = db.Column(db.Integer)
    wismod = db.Column(db.Integer)
    chamod = db.Column(db.Integer)

    def __repr__(self):
        return f'<FormData {self.name}>'

# Create database tables
with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Getting
        name = request.form.get('name')
        strn = int(request.form.get('strength'))
        dext = int(request.form.get('dexterity'))
        cons = int(request.form.get('constitution'))
        intl = int(request.form.get('intelligence'))
        wisd = int(request.form.get('wisdom'))
        char = int(request.form.get('charisma'))
        
        # Processing
        pointbuy = pb_valid(strn, dext, cons, intl, wisd, char)
        strmod = as_to_mod(strn)
        dexmod = as_to_mod(dext)
        conmod = as_to_mod(cons)
        intmod = as_to_mod(intl)
        wismod = as_to_mod(wisd)
        chamod = as_to_mod(char)
        
        # Add to DB
        new_entry = FormData(
            name=name,
            strn=strn,
            dext=dext,
            cons=cons,
            intl=intl,
            wisd=wisd,
            char=char,
            pointbuy = pointbuy,
            strmod=strmod,
            dexmod=dexmod,
            conmod=conmod,
            intmod=intmod,
            wismod=wismod,
            chamod=chamod,
        )
        
        try:
            db.session.add(new_entry)
            db.session.commit()
            flash('Data successfully submitted!', 'success')
            return redirect(url_for('result', id=new_entry.id))
        except Exception as e:
            db.session.rollback()
            print(f"Error: {e}")  # Log the exception
            flash('An error occurred. Please try again.', 'error')
            return redirect(url_for('index'))
            
    return render_template('index.html')

@app.route('/result/<int:id>')
def result(id):
    entry = FormData.query.get_or_404(id)
    return render_template('result.html', entry=entry)

# Data processing logic function
def as_to_mod(num):
    return (num - 10) / 2

def pb_valid(strn, dext, cons, intl, wisd, char):
    if((strn + dext + cons + intl + wisd + char) == 27):
        return "Fully spent!"
    elif((strn + dext + cons + intl + wisd + char) > 27):
        return "Over limit. Arrangement invalid."
    else:
        return "Under limit. Arrangement invalid."
    

if __name__ == '__main__':
    app.run(debug=True)