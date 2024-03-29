from app import app
from flask import flash, render_template, redirect, url_for, request
from app.gas import bp
from flask_login import current_user, login_required
from func_pack import get_current_date, get_last_date, get_last_date_strftime, get_current_date_strftime,\
    get_api_info_first, get_api_info, get_current_datetime, get_current_time, get_account_info_by_account_id
from config import Config
from app.gas.forms import GasDataStatsForm, GasDataRecordForm, GasInfoClass
from app.forms import DeleteForm
import requests


# status-panel version 2
# elec stats panel
# status-panel version 2
# stats panel
@login_required
@bp.route('/gas-stats-panel', methods=['GET', 'POST'])
def gas_stats_panel():
    # auth process
    if current_user.is_authenticated is True:
        account = get_account_info_by_account_id(current_user.account_id)
    else:
        return redirect(url_for('auth.login_view'))
    # process end

    form = GasDataStatsForm()
    # functional url
    basic_successive_url = 'http://' + Config.DB_OPS_URL + '/api/gas/calculating/gas-consumption/successive/'
    basic_sum_url = 'http://' + Config.DB_OPS_URL + '/api/gas/calculating/gas-consumption/inexact-date/'

    # post function
    if form.validate_on_submit():
        boiler_room = str(form.boiler_room_and_no.data).split('/')[0]
        boiler_no = str(form.boiler_room_and_no.data).split('/')[1]
        sum_url = basic_sum_url + boiler_room + '/' + boiler_no + '/' +\
                        str(form.start_date.data) + '/' + str(form.end_date.data)
        successive_url = basic_successive_url + boiler_room + '/' + boiler_no + '/' +\
                         str(form.start_date.data) + '/' + str(form.end_date.data)
    # get function
    else:
        today_date = get_current_date()
        last_date = get_last_date()
        form.start_date.data = get_last_date_strftime()
        form.end_date.data = get_current_date_strftime()

        default_boiler_room_and_no = GasInfoClass().get_gas_url_list()[0]
        sum_url = basic_sum_url + default_boiler_room_and_no + '/' + last_date + '/' + today_date
        successive_url = basic_successive_url + default_boiler_room_and_no + '/' + last_date + '/' + today_date
        flash('默认统计"今日与昨日"的燃气消耗量。', 'info')
    # get relative gas data
    # get first with dict type
    consumption_sum_dict = get_api_info_first(requests.get(sum_url))
    # get all with list type
    consumption_successive_list = get_api_info(requests.get(successive_url))
    if consumption_sum_dict['gas_consumption_type'] == '错误' or\
            consumption_sum_dict['gas_consumption_type'] == '日期区间错误':
        flash('无相关数据!', 'danger')
    else:
        flash('数据统计成功!', 'success')
    # render templates
    return render_template('gas/statsPanel.html', consumption_sum_dict=consumption_sum_dict, account=account,
                           consumption_successive_list=consumption_successive_list, form=form, title='燃气数据统计')


@login_required
@bp.route('/gas-data-submit', methods=['GET'])
def gas_data_submit_view():
    # auth process
    if current_user.is_authenticated is True:
        account = get_account_info_by_account_id(current_user.account_id)
    else:
        return redirect(url_for('auth.login_view'))
    # process end
    form = GasDataRecordForm()
    return render_template('gas/gasDataSubmit.html', form=form, title='燃气数据提交', account=account)


@login_required
@bp.route('/gas-data-submit', methods=['POST'])
def data_submit_post():
    # auth process
    if current_user.is_authenticated is True:
        account = get_account_info_by_account_id(current_user.account_id)
    else:
        return redirect(url_for('auth.login_view'))
    # process end
    form = GasDataRecordForm()
    post_doc_url = 'http://' + Config.DB_OPS_URL + '/api/gas/document'
    doc_dict = dict(request.form)
    doc_dict['boiler_room'] = str(form.boiler_room_and_no.data).split('/')[0]
    doc_dict['boiler_no'] = str(form.boiler_room_and_no.data).split('/')[1]
    doc_dict['employee_no'] = current_user.account_id
    doc_dict['employee_name'] = account['account_nickname']
    doc_dict['datetime'] = get_current_datetime()
    doc_dict['date'] = get_current_date()
    doc_dict['time'] = get_current_time()
    if form.validate_on_submit():
        result = requests.post(post_doc_url, data=doc_dict)
        if result.status_code == 200:
            flash('数据提交成功', 'success')
            return redirect(url_for('gas.gas_data_submit_view'))
        else:
            flash('发生了错误, 数据未成功提交', 'danger')
            return redirect(url_for('gas.gas_data_submit_view'))


# delete view
@bp.route('/deleting/<string:record_id>', methods=['GET', 'POST'])
@login_required
def delete_confirm(record_id):
    # auth process
    if current_user.is_authenticated is True:
        account = get_account_info_by_account_id(current_user.account_id)
    else:
        return redirect(url_for('auth.login_view'))
    # process end
    form = DeleteForm()
    # Get record info
    record_url = 'http://' + Config.DB_OPS_URL + \
                 '/api/gas/document/rid/' + str(record_id)
    result = requests.get(record_url)
    # Functional Part
    if form.validate_on_submit():
        if result.status_code == 200:
            user_id = get_api_info(result)[0]['employee_no']

            # check user's authentication by account_id in url whether match current_user.account_id
            # Mention!! Type of current_user.account_id is not string!
            if str(current_user.account_id) != str(user_id):
                # back to detail viewing page
                flash('试图删除不属于自己的数据', 'danger')
                return redirect(
                    url_for('auth.home_view', account_id=current_user.account_id))

            # main function process below
            delete_url = 'http://' + Config.DB_OPS_URL + \
                         '/api/gas/document/' + str(record_id)
            requests.delete(delete_url)
            flash('数据删除成功', 'success')
            return redirect(url_for('auth.home_view', account_id=current_user.account_id))
    # View Part
    else:
        if result.status_code == 200:
            user_id = get_api_info(result)[0]['employee_no']

            # check user's authentication by account_id in url whether match current_user.account_id
            # Mention!! Type of current_user.account_id is not string!
            if str(current_user.account_id) != str(user_id):
                # back to detail viewing page
                return redirect(
                    url_for('auth.home_view', account_id=current_user.account_id))

            # main function process below
            competition = get_api_info(result)[0]
            return render_template('recordDelete.html', form=form, account=account)

