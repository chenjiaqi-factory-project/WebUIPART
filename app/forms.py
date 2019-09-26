from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField
from wtforms.validators import DataRequired
from static_data import GasInfoClass

# choice = [('地点A/1号锅炉', '地点A - 1号锅炉')]
gasInfoClass = GasInfoClass()
# waterInfoClass = WaterInfoClass()
# elecInfoClass = ElecInfoClass()


# Send CSV file form
class SendCsvFileForm(FlaskForm):
    gas_submit = SubmitField('下载燃气数据')
    water_submit = SubmitField('下载用水量数据')
    elec_submit = SubmitField('下载用电量数据')


# View Panel Form
class ViewPanelSearchForm(FlaskForm):
    boiler_room_and_no = SelectField('选择锅炉房及锅炉', choices=gasInfoClass.get_gas_field_list(), validators=[DataRequired()])
    submit = SubmitField('检索数据')
