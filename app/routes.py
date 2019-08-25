from app import app
from flask import jsonify, render_template, request, flash, redirect, url_for, send_file, Response
from config import Config
from func_pack import get_api_info, get_current_datetime, get_current_date, get_current_time, write_csv
from app.forms import DataRecordForm, SendCsvFileForm
import requests


@app.route('/', methods=['GET'])
@app.route('/panel', methods=['GET'])
def panel_view():
    get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/document/all-documents'
    result = requests.get(get_doc_url)
    if result.status_code == 200:
        document_list = get_api_info(result)
        document_list.reverse()
        return render_template('frontPage.html', documents=document_list, title='数据监测')
    else:
        document_list = [{'Error': 'Server Down.'}]
        return render_template('frontPage.html', documents=document_list, title='数据监测')


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





