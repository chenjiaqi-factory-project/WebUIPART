from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from static_data import GasInfoClass, WaterInfoClass, ElecInfoClass

# choice = [('地点A/1号锅炉', '地点A - 1号锅炉')]
gasInfoClass = GasInfoClass()
waterInfoClass = WaterInfoClass()
elecInfoClass = ElecInfoClass()


# Gas Data Record form
class GasDataRecordForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=gasInfoClass.get_gas_field_list(), validators=[DataRequired()])
    gas_indicator = StringField('燃气表读数', validators=[DataRequired()])
    employee_no = StringField('员工编号', validators=[DataRequired()])
    submit = SubmitField('提交')


# Water Data Record form
class WaterDataRecordForm(FlaskForm):
    factory_no = SelectField('选择水表地点', choices=waterInfoClass.get_water_field_list(), validators=[DataRequired()])
    water_indicator = StringField('用水量', validators=[DataRequired()])
    employee_no = StringField('员工编号', validators=[DataRequired()])
    submit = SubmitField('提交')


# Send CSV file form
class SendCsvFileForm(FlaskForm):
    submit = SubmitField('下载数据')


# View Panel Form
class ViewPanelSearchForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=gasInfoClass.get_gas_field_list(), validators=[DataRequired()])
    submit = SubmitField('检索数据')


# Data stats form
class GasDataStatsForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=gasInfoClass.get_gas_field_list(), validators=[DataRequired()])
    start_date = DateField('起始日期', validators=[DataRequired()])
    end_date = DateField('终止日期', validators=[DataRequired()])
    # Select fields keep a choices property which is a sequence of (value, label) pairs.
    # stats_type = SelectField('统计类型', choices=[('gas', '燃气统计')], validators=[DataRequired()])
    submit = SubmitField('开始统计')


# Data stats form
class WaterDataStatsForm(FlaskForm):
    factory_no = SelectField('选择水表地点', choices=waterInfoClass.get_water_field_list(), validators=[DataRequired()])
    start_date = DateField('起始日期', validators=[DataRequired()])
    end_date = DateField('终止日期', validators=[DataRequired()])
    # Select fields keep a choices property which is a sequence of (value, label) pairs.
    # stats_type = SelectField('统计类型', choices=[('gas', '燃气统计')], validators=[DataRequired()])
    submit = SubmitField('开始统计')
