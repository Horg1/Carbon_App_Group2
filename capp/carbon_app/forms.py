from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, FloatField
from wtforms.validators import InputRequired, NumberRange

class BoatForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired(), NumberRange(min=0.001, message='Must be greater than 0')])
    seafood_kg = FloatField('Cargo Weight (kg)', [InputRequired(), NumberRange(min=0.001, message='Must be greater than 0')])
    fuel_type = SelectField('Type of Fuel', [InputRequired()],
                            choices=[('Diesel', 'Diesel / HFO'), ('LNG', 'LNG'), ('Electric', 'Electric / Zero Emission')])
    submit = SubmitField('Submit')

class PlaneForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired(), NumberRange(min=0.001, message='Must be greater than 0')])
    seafood_kg = FloatField('Cargo Weight (kg)', [InputRequired(), NumberRange(min=0.001, message='Must be greater than 0')])
    fuel_type = SelectField('Type of Fuel', [InputRequired()],
                            choices=[('Jet Fuel', 'Jet Fuel (Kerosene)'), ('SAF', 'SAF (Sustainable Aviation Fuel)')])
    submit = SubmitField('Submit')

class TruckForm(FlaskForm):
    kms = FloatField('Kilometers', [InputRequired(), NumberRange(min=0.001, message='Must be greater than 0')])
    seafood_kg = FloatField('Cargo Weight (kg)', [InputRequired(), NumberRange(min=0.001, message='Must be greater than 0')])
    fuel_type = SelectField('Type of Fuel', [InputRequired()],
                            choices=[('Diesel', 'Diesel'), ('LNG', 'LNG'), ('HVO', 'HVO (Biodiesel)'), ('Electric', 'Electric')])
    submit = SubmitField('Submit')
