from app import app
from flask import jsonify, render_template, request, flash, redirect, url_for, send_file, Response
from config import Config
from func_pack import get_api_info, get_current_datetime, get_current_date, get_current_time, write_csv, get_api_info_first
from func_pack import get_last_date, get_current_date_strftime, get_last_date_strftime
from app.forms import DataRecordForm, SendCsvFileForm, DataStatsForm, ViewPanelSearchForm
from static_data import GasInfoClass
import requests


# boiler panel view
@app.route('/', methods=['GET'])
@app.route('/boiler-panel', methods=['GET'])
def gas_panel_view():
    form = ViewPanelSearchForm()
    get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/gas/document/all-documents'
    result = requests.get(get_doc_url)
    if result.status_code == 200:
        document_list = get_api_info(result)
        document_list.reverse()
    else:
        document_list = [{'Error': 'Server Down.'}]
    return render_template('gasPanel.html', documents=document_list, title='燃气监测', form=form)


@app.route('/', methods=['POST'])
@app.route('/boiler-panel', methods=['POST'])
def gas_panel_search():
    form = ViewPanelSearchForm()
    basic_doc_url = 'http://' + Config.DB_OPS_URL + '/api/gas/document/boiler-room-and-no/fuzzy/'
    if form.validate_on_submit():
        search_doc_url = basic_doc_url + str(form.boiler_room_and_no.data)
        gas_doc_list = get_api_info(requests.get(search_doc_url))
        flash('数据检索成功!', 'success')
        return render_template('gasPanel.html', documents=gas_doc_list, title='燃气监测', form=form)


# status-panel version 2
# stats panel
@app.route('/stats-panel', methods=['GET', 'POST'])
def stats_panel():
    form = DataStatsForm()
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
    return render_template('statsPanel.html', consumption_sum_dict=consumption_sum_dict,
                           consumption_successive_list=consumption_successive_list, form=form, title='数据统计')


@app.route('/data-submit', methods=['GET'])
def data_submit_view():
    form = DataRecordForm()
    return render_template('dataSubmit.html', form=form, title='数据提交')


@app.route('/data-submit', methods=['POST'])
def data_submit_post():
    form = DataRecordForm()
    post_doc_url = 'http://' + Config.DB_OPS_URL + '/api/gas/document'
    doc_dict = dict(request.form)
    doc_dict['boiler_room'] = str(form.boiler_room_and_no.data).split('/')[0]
    doc_dict['boiler_no'] = str(form.boiler_room_and_no.data).split('/')[1]
    doc_dict['datetime'] = get_current_datetime()
    doc_dict['date'] = get_current_date()
    doc_dict['time'] = get_current_time()
    if form.validate_on_submit():
        result = requests.post(post_doc_url, data=doc_dict)
        if result.status_code == 200:
            flash('数据提交成功', 'success')
            return redirect(url_for('data_submit_view'))
        else:
            flash('发生了错误, 数据未成功提交', 'danger')
            return redirect(url_for('data_submit_view'))


@app.route('/downloading', methods=['GET'])
def data_download_view():
    form = SendCsvFileForm()
    return render_template('dataDownLoad.html', form=form, title='数据下载')


@app.route('/downloading', methods=['POST'])
def data_download_post():
    form = SendCsvFileForm()
    if form.validate_on_submit():
        get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/document/all-documents'
        result = requests.get(get_doc_url)
        if result.status_code == 200:
            document_list = get_api_info(result)
            write_csv(document_list, Config.DATA_CSV_PATH)
            flash('数据下载成功!', 'success')
            return send_file(Config.DATA_CSV_SEND_PATH, mimetype='text/csv',
                             attachment_filename='data.csv', as_attachment=True)





