from app import app
from flask import jsonify, render_template, request, flash, redirect, url_for, send_file, Response
from config import Config
from func_pack import get_api_info, get_current_datetime, get_current_date, get_current_time, write_csv, get_api_info_first
from func_pack import get_last_date
from app.forms import DataRecordForm, SendCsvFileForm, DataStatsForm
import requests


# boiler panel view
@app.route('/', methods=['GET'])
@app.route('/boiler-panel', methods=['GET'])
def gas_panel_view():
    get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/gas/document/all-documents'
    result = requests.get(get_doc_url)
    if result.status_code == 200:
        document_list = get_api_info(result)
        document_list.reverse()
        return render_template('gasPanel.html', documents=document_list, title='燃气监测')
    else:
        document_list = [{'Error': 'Server Down.'}]
        return render_template('gasPanel.html', documents=document_list, title='燃气监测')


# stats panel
# @app.route('/stats-panel', methods=['GET', 'POST'])
# def stats_panel():
#     form = DataStatsForm()
#     # functional url
#     date_url = 'http://' + Config.DB_OPS_URL + '/api/gas/document/date/fuzzy/'
#
#     # post function
#     if form.validate_on_submit():
#         start_date_url = date_url + str(form.start_date.data)
#         end_date_url = date_url + str(form.end_date.data)
#     # get function
#     else:
#         today_date = get_current_date()
#         last_date = get_last_date()
#         start_date_url = date_url + last_date
#         end_date_url = date_url + today_date
#
#     # get relative gas data
#     start_gas_data = requests.get(start_date_url)
#     end_gas_data = requests.get(end_date_url)
#     # if both return correct answer
#     if start_gas_data.status_code == 200 and end_gas_data.status_code == 200:
#         start_gas_doc = get_api_info_first(start_gas_data)
#         end_gas_doc = get_api_info_first(end_gas_data)
#
#         # if there is no date
#         if 'error' in start_gas_doc:
#             flash('您输入的起始日期没有对应数据! 请重新输入日期。', 'error')
#             return render_template('statsPanel.html', form=form,
#                                    start_gas_doc=start_gas_doc, end_gas_doc=end_gas_doc,
#                                    gas_consumption='无法统计')
#         elif 'error' in end_gas_doc:
#             flash('您输入的终止日期没有对应数据! 请重新输入日期。', 'error')
#             return render_template('statsPanel.html', form=form,
#                                    start_gas_doc=start_gas_doc, end_gas_doc=end_gas_doc,
#                                    gas_consumption='无法统计')
#
#         # 正常情况
#         gas_consumption = round(abs(float(start_gas_doc['gas_indicator']) - float(end_gas_doc['gas_indicator'])), 3)
#         flash('数据统计成功!', 'info')
#         return render_template('statsPanel.html', form=form,
#                                start_gas_doc=start_gas_doc, end_gas_doc=end_gas_doc, gas_consumption=gas_consumption)


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
        sum_url = basic_sum_url + str(form.boiler_room.data) + '/' + str(form.boiler_no.data) + '/' +\
                        str(form.start_date.data) + '/' + str(form.end_date.data)
        successive_url = basic_successive_url + str(form.boiler_room.data) + '/' + str(form.boiler_no.data) + '/' +\
                         str(form.start_date.data) + '/' + str(form.end_date.data)
    # get function
    else:
        today_date = get_current_date()
        last_date = get_last_date()
        # ToDo: 修改默认 URL
        sum_url = basic_sum_url + '地点A' + '/' + '1号锅炉' + '/' + last_date + '/' + today_date
        successive_url = basic_successive_url + '地点A' + '/' + '1号锅炉' + '/' + last_date + '/' + today_date
    # get relative gas data
    # get first with dict type
    consumption_sum_dict = get_api_info_first(requests.get(sum_url))
    # get all with list type
    consumption_successive_list = get_api_info(requests.get(successive_url))
    # render templates
    return render_template('statsPanel.html', consumption_sum_dict=consumption_sum_dict,
                           consumption_successive_list=consumption_successive_list, form=form)


@app.route('/data-submit', methods=['GET'])
def data_submit_view():
    form = DataRecordForm()
    return render_template('dataSubmit.html', form=form, title='数据提交')


@app.route('/data-submit', methods=['POST'])
def data_submit_post():
    form = DataRecordForm()
    post_doc_url = 'http://' + Config.DB_OPS_URL + '/api/document'
    doc_dict = dict(request.form)
    doc_dict['datetime'] = get_current_datetime()
    doc_dict['date'] = get_current_date()
    doc_dict['time'] = get_current_time()
    if form.validate_on_submit():
        result = requests.post(post_doc_url, data=doc_dict)
        if result.status_code == 200:
            flash('数据提交成功')
            return redirect(url_for('data_submit_view'))
        else:
            flash('发生了错误, 数据未成功提交')
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
            return send_file(Config.DATA_CSV_SEND_PATH, mimetype='text/csv',
                             attachment_filename='data.csv', as_attachment=True)





