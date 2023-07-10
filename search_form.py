from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange


# define form used to validate investment input
class InvestmentForm(FlaskForm):

    # field for investment quantity
    #   - validates that data is inputted, and is a decimal
    #   - validates only 2 decimal places are read
    #   - Accepts values withing the NumberRange()
    investment = DecimalField('Investment', validators=[DataRequired(),
                              NumberRange(min=0.01, max=99999999.99)],
                              places=2)

    # defines a submit button
    submit = SubmitField('Show Results')
