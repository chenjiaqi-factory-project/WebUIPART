from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


# Reset password form
class DataRecordForm(FlaskForm):
    boiler_no = StringField('锅炉编号', validators=[DataRequired()])
    gas_consumption = StringField('燃气消耗量', validators=[DataRequired()])
    elec_consumption = StringField('电力消耗量', validators=[DataRequired()])
    water_consumption = StringField('水消耗量', validators=[DataRequired()])
    water_out_temperature = StringField('出水温度', validators=[DataRequired()])
    water_in_temperature = StringField('回水温度', validators=[DataRequired()])
    location = StringField('地点', validators=[DataRequired()])
    employee_no = StringField('员工编号', validators=[DataRequired()])
    submit = SubmitField('提交')

