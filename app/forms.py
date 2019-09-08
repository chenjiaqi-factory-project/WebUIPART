from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired


# Data Record form
class DataRecordForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=[('地点A/1号锅炉', '地点A - 1号锅炉')], validators=[DataRequired()])
    gas_indicator = StringField('燃气表读数', validators=[DataRequired()])
    employee_no = StringField('员工编号', validators=[DataRequired()])
    submit = SubmitField('提交')


# Send CSV file form
class SendCsvFileForm(FlaskForm):
    submit = SubmitField('下载数据')


# View Panel Form
class ViewPanelSearchForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=[('地点A/1号锅炉', '地点A - 1号锅炉')], validators=[DataRequired()])
    submit = SubmitField('搜索数据')


# Data stats form
class DataStatsForm(FlaskForm):
    boiler_room = SelectField('选择锅炉房', choices=[('地点A', '地点A')], validators=[DataRequired()])
    boiler_no = SelectField('选择锅炉', choices=[('1号锅炉', '1号锅炉')], validators=[DataRequired()])
    start_date = DateField('起始日期', validators=[DataRequired()])
    end_date = DateField('终止日期', validators=[DataRequired()])
    # Select fields keep a choices property which is a sequence of (value, label) pairs.
    stats_type = SelectField('统计类型', choices=[('gas', '燃气统计')], validators=[DataRequired()])
    submit = SubmitField('开始统计')
