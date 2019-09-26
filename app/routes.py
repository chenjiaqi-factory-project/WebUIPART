from app import app
from flask import jsonify, render_template, request, flash, redirect, url_for, send_file, Response
from config import Config
from flask_login import logout_user
from func_pack import get_api_info, get_current_datetime, get_current_date, get_current_time, write_csv, get_api_info_first
import requests
from app.forms import ViewPanelSearchForm, SendCsvFileForm


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


@app.route('/downloading', methods=['GET'])
def data_download_view():
    form = SendCsvFileForm()
    return render_template('dataDownLoad.html', form=form, title='数据下载')


@app.route('/downloading', methods=['POST'])
def data_download_post():
    form = SendCsvFileForm()
    if form.validate_on_submit():
        # choose data type
        if form.gas_submit.data is True:
            get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/gas/document/all-documents'
            file_name = 'gasData.csv'
        elif form.elec_submit.data is True:
            get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/elec/document/all-documents'
            file_name = 'elecData.csv'
        else:
            get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/water/document/all-documents'
            file_name = 'waterData.csv'

        result = requests.get(get_doc_url)
        if result.status_code == 200:
            document_list = get_api_info(result)
            write_csv(document_list, Config.DATA_CSV_PATH)
            flash('数据下载成功!', 'success')
            return send_file(Config.DATA_CSV_SEND_PATH, mimetype='text/csv',
                             attachment_filename=file_name, as_attachment=True)


# -------------- Log Out --------------- #
@app.route('/logout', methods=['GET'])
def logout_func():
    logout_user()
    return redirect(url_for('auth.login_view'))



