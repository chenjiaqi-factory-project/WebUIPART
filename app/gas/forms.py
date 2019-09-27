from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from static_data import GasInfoClass


gasInfoClass = GasInfoClass()


# Gas Data Record form
class GasDataRecordForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=gasInfoClass.get_gas_field_list(), validators=[DataRequired()])
    gas_indicator = StringField('燃气表读数', validators=[DataRequired()])
    submit = SubmitField('提交')


# Data stats form
class GasDataStatsForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=gasInfoClass.get_gas_field_list(), validators=[DataRequired()])
    start_date = DateField('起始日期', validators=[DataRequired()])
    end_date = DateField('终止日期', validators=[DataRequired()])
    # Select fields keep a choices property which is a sequence of (value, label) pairs.
    # stats_type = SelectField('统计类型', choices=[('gas', '燃气统计')], validators=[DataRequired()])
    submit = SubmitField('开始统计')

