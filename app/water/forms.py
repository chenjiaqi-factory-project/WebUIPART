from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from static_data import WaterInfoClass


waterInfoClass = WaterInfoClass()


# Water Data Record form
class WaterDataRecordForm(FlaskForm):
    factory_no = SelectField('选择水表地点', choices=waterInfoClass.get_water_field_list(), validators=[DataRequired()])
    water_indicator = StringField('用水量', validators=[DataRequired()])
    employee_no = StringField('员工编号', validators=[DataRequired()])
    submit = SubmitField('提交')


# Data stats form
class WaterDataStatsForm(FlaskForm):
    factory_no = SelectField('选择水表地点', choices=waterInfoClass.get_water_field_list(), validators=[DataRequired()])
    start_date = DateField('起始日期', validators=[DataRequired()])
    end_date = DateField('终止日期', validators=[DataRequired()])
    # Select fields keep a choices property which is a sequence of (value, label) pairs.
    # stats_type = SelectField('统计类型', choices=[('gas', '燃气统计')], validators=[DataRequired()])
    submit = SubmitField('开始统计')

