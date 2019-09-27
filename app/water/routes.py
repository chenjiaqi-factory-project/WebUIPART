from app import app
from flask import flash, render_template, redirect, url_for, request
from app.water import bp
from flask_login import current_user, login_required
from func_pack import get_current_date, get_last_date, get_last_date_strftime, get_current_date_strftime,\
    get_api_info_first, get_api_info, get_current_datetime, get_current_time, get_account_info_by_account_id
from config import Config
from app.water.forms import WaterInfoClass, WaterDataStatsForm, WaterDataRecordForm
import requests


# status-panel version 2
# water stats panel
@login_required
@bp.route('/water-stats-panel', methods=['GET', 'POST'])
def water_stats_panel():
    # auth process
    if current_user.is_authenticated is True:
        account = get_account_info_by_account_id(current_user.account_id)
    else:
        return redirect(url_for('auth.login_view'))
    # process end

    form = WaterDataStatsForm()
    # functional url
    basic_successive_url = 'http://' + Config.DB_OPS_URL + '/api/water/calculating/water-consumption/successive/'
    basic_sum_url = 'http://' + Config.DB_OPS_URL + '/api/water/calculating/water-consumption/inexact-date/'

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

        default_boiler_room_and_no = WaterInfoClass().get_water_url_list()[0]
        sum_url = basic_sum_url + default_boiler_room_and_no + '/' + last_date + '/' + today_date
        successive_url = basic_successive_url + default_boiler_room_and_no + '/' + last_date + '/' + today_date
        flash('默认统计"今日与昨日"的用水消耗量。', 'info')
    # get relative water data
    # get first with dict type
    consumption_sum_dict = get_api_info_first(requests.get(sum_url))
    # get all with list type
    consumption_successive_list = get_api_info(requests.get(successive_url))
    if consumption_sum_dict['water_consumption_type'] == '错误' or\
            consumption_sum_dict['water_consumption_type'] == '日期区间错误':
        flash('无相关数据!', 'danger')
    else:
        flash('数据统计成功!', 'success')
    # render templates
    return render_template('water/waterStatsPanel.html', consumption_sum_dict=consumption_sum_dict, account=account,
                           consumption_successive_list=consumption_successive_list, form=form, title='用水量数据统计')


@login_required
@bp.route('/water-data-submit', methods=['GET'])
def water_data_submit_view():
    # auth process
    if current_user.is_authenticated is True:
        account = get_account_info_by_account_id(current_user.account_id)
    else:
        return redirect(url_for('auth.login_view'))
    # process end
    form = WaterDataRecordForm()
    return render_template('water/waterDataSubmit.html', form=form, title='用水量数据提交', account=account)


@login_required
@bp.route('/water-data-submit', methods=['POST'])
def water_data_submit_post():
    form = WaterDataRecordForm()
    post_doc_url = 'http://' + Config.DB_OPS_URL + '/api/water/document'
    doc_dict = dict(request.form)
    doc_dict['factory_no'] = form.factory_no.data
    doc_dict['datetime'] = get_current_datetime()
    doc_dict['date'] = get_current_date()
    doc_dict['time'] = get_current_time()
    if form.validate_on_submit():
        result = requests.post(post_doc_url, data=doc_dict)
        if result.status_code == 200:
            flash('数据提交成功', 'success')
            return redirect(url_for('water.water_data_submit_view'))
        else:
            flash('发生了错误, 数据未成功提交', 'danger')
            return redirect(url_for('water.water_data_submit_view'))

