from app import app
from flask import flash, render_template, redirect, url_for, request
from app.elec import bp
from func_pack import get_current_date, get_last_date, get_last_date_strftime, get_current_date_strftime,\
    get_api_info_first, get_api_info, get_current_datetime, get_current_time
from config import Config
from app.elec.forms import ElecDataRecordForm, ElecDataStatsForm, ElecInfoClass
import requests


# status-panel version 2
# elec stats panel
@bp.route('/elec-stats-panel', methods=['GET', 'POST'])
def elec_stats_panel():
    form = ElecDataStatsForm()
    # functional url
    basic_successive_url = 'http://' + Config.DB_OPS_URL + '/api/elec/calculating/consumption/successive/'
    basic_sum_url = 'http://' + Config.DB_OPS_URL + '/api/elec/calculating/consumption/inexact-date/'

    # post function
    if form.validate_on_submit():
        factory_no = str(form.factory_no.data).split('/')[0]
        sum_url = basic_sum_url + factory_no + '/' +\
                        str(form.start_date.data) + '/' + str(form.end_date.data)
        successive_url = basic_successive_url + factory_no + '/' +\
                         str(form.start_date.data) + '/' + str(form.end_date.data)
    # get function
    else:
        today_date = get_current_date()
        last_date = get_last_date()
        form.start_date.data = get_last_date_strftime()
        form.end_date.data = get_current_date_strftime()

        default_boiler_room_and_no = ElecInfoClass().get_elec_url_list()[0]
        sum_url = basic_sum_url + default_boiler_room_and_no + '/' + last_date + '/' + today_date
        successive_url = basic_successive_url + default_boiler_room_and_no + '/' + last_date + '/' + today_date
        flash('默认统计"今日与昨日"的用电消耗量。', 'info')
    # get relative gas data
    # get first with dict type
    consumption_sum_dict = get_api_info_first(requests.get(sum_url))
    # get all with list type
    consumption_successive_list = get_api_info(requests.get(successive_url))
    if consumption_sum_dict['elec_consumption_type'] == '错误' or\
            consumption_sum_dict['elec_consumption_type'] == '日期区间错误':
        flash('无相关数据!', 'danger')
    else:
        flash('数据统计成功!', 'success')
    # render templates
    return render_template('elec/elecStatsPanel.html', consumption_sum_dict=consumption_sum_dict,
                           consumption_successive_list=consumption_successive_list, form=form, title='用电量数据统计')


@bp.route('/elec-data-submit', methods=['GET'])
def elec_data_submit_view():
    form = ElecDataRecordForm()
    return render_template('elec/elecDataSubmit.html', form=form, title='用电量数据提交')


@bp.route('/elec-data-submit', methods=['POST'])
def elec_data_submit_post():
    form = ElecDataRecordForm()
    post_doc_url = 'http://' + Config.DB_OPS_URL + '/api/elec/document'
    doc_dict = dict(request.form)
    doc_dict['factory_no'] = form.factory_no.data
    doc_dict['datetime'] = get_current_datetime()
    doc_dict['date'] = get_current_date()
    doc_dict['time'] = get_current_time()
    if form.validate_on_submit():
        result = requests.post(post_doc_url, data=doc_dict)
        if result.status_code == 200:
            flash('数据提交成功', 'success')
            return redirect(url_for('elec.elec_data_submit_view'))
        else:
            flash('发生了错误, 数据未成功提交', 'danger')
            return redirect(url_for('elec.elec_data_submit_view'))

