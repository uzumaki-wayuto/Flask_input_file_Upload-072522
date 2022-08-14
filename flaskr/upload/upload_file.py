from flask import request, render_template, redirect, url_for, send_from_directory, flash, current_app as app
from . import send_file_bp
from werkzeug.utils import secure_filename
import os
from datetime import datetime

ALLOWED_EXTENSIONS = {'mp4', 'mp3', 'jpg', 'png', 'gif', 'txt', 'rtf', 'pdf'}

def allowed_file(filename):
    """ check whether file or not and is allowed file ext
    parameter : file name
    return boolean """
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        
@send_file_bp.route('/')
def index():
    """ Index """
    navs = [{ 'name':'Upload', 'url':'send_file.upload'}, {'name':'Download', 'url':'send_file.download_list'}] #dynamic navigation to nav.html
    return render_template('index.html',extensions = list(ALLOWED_EXTENSIONS), navs=navs) #extension to announce

@send_file_bp.route('/upload', methods=['GET', 'POST'])
def upload():
    """ where upload works """
    navs = [{ 'name':'Home', 'url':'send_file.index'}, {'name':'Download', 'url':'send_file.download_list'}]
    if request.method == 'POST':
        file = request.files['file']
        if 'file' not in request.files:
            flash('No file apart', 'danger') #categories are inserted directly into bootstrap class - alert-danger
            return redirect(url_for('send_file.index'))
        if file.filename == '':
            flash('No file selected', 'warning')
            return redirect(url_for('send_file.index'))
        if file and allowed_file(file.filename): 
            filename = secure_filename(file.filename)
            new_filename = f'{filename.split(".")[0]}_{str(datetime.now().strftime("%m%d%y%H%M%S"))}.{filename.rsplit(".", 1)[1]}' #add date time to file name , format -> filename_datetime.ext
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename)) 
            flash('Uploaded', 'success')
            """set sleeep for 15000, to see progress bar(bootstrap class) working in uploading progress"""
            x=0
            while True: #do while
                print(x)
                if x == 15000:
                    break
                    x+=1
            return redirect(url_for('send_file.download_list', filename=new_filename, navs=navs))
        flash('Invalid File Type ', 'warning')
        return redirect(url_for('.index'))
    return render_template('upload.html', navs=navs)

@send_file_bp.route('/list', methods=['GET'])
def download_list():
    """list the file to show"""
    navs = [{ 'name':'Home', 'url':'send_file.index'}, {'name':'Upload', 'url':'send_file.upload'}]
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    if not files:
        flash('No file available rn, upload something', 'warning')
    return render_template('download.html', files=files, navs=navs)

@send_file_bp.route('/download/<path:filename>', methods=['GET', 'POST'])
def download(filename):
    """ download file whether get or post request, click on filename -> get , on button -> post """
    #upload_dir = os.path.join(app.root_path, app.config['UPLOAD_FOLDER'])
    if request.method == 'POST':
        return send_from_directory('files', filename) #post
    return send_from_directory('files',filename) #same for get
