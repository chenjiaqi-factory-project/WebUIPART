from app import app
from flask import jsonify, render_template
from config import Config
from func_pack import get_api_info
import requests


@app.route('/')
@app.route('/panel')
def usage():
    get_doc_url = 'http://' + Config.DB_OPS_URL + '/api/document/all-documents'
    result = requests.get(get_doc_url)
    if result.status_code == 200:
        document_list = get_api_info(result)
        return render_template('frontPage.html', documents=document_list)
    else:
        document_list = [{'Error': 'Server Down.'}]
        return render_template('frontPage.html', documents=document_list)

