from flask import Flask, render_template, redirect, request, send_from_directory
from socket import gethostname, gethostbyname
from pathlib import Path
from os import listdir

def secure_filename(rawFilename):
    if '.' in rawFilename:
        filedata = rawFilename.rsplit('.', 1)
        filedata[1] = '.' + filedata[1]
    else:
        filedata = [rawFilename, '']
    # using global allowed
    filename = ''
    for letter in filedata[0]:
        if letter in allowed:
            filename += letter
    if (filename + filedata[1]) in listdir(filesFolder):
        antiCopy = 0
        while (filename + str(antiCopy) + filedata[1]) in listdir(filesFolder):
            antiCopy += 1
        filename = filename + str(antiCopy) + filedata[1]
    else:
        filename = filename + filedata[1]
    return filename

def getFiles(folder):
    files = {'path': folder.relative_to(filesFolder).as_posix(), 'name': folder.name, 'files': []}
    for file in folder.iterdir():
        if file.is_dir():
            files['files'].append(getFiles(file))
        else:
            files['files'].append({'path': file.relative_to(filesFolder).as_posix(), 'name': file.name})
    return files

print('website: http://' + gethostbyname(gethostname()) + ':8080')
app = Flask(__name__, template_folder='web/HTML', static_folder='web/public')
rootFolder = Path(__file__).parent
filesFolder = rootFolder / 'shared'

if (rootFolder / 'allowed.txt').is_file():
    with open(rootFolder / 'allowed.txt', 'r') as f:
        allowed = f.read()
else:
    allowed = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890_-. '

if filesFolder.is_dir() == False:
    filesFolder.mkdir()

@app.route('/', methods=['GET'])
def web_root():
    return render_template('index.html')

@app.route('/upload', methods=['GET'])
def web_upload():
    uploaded = request.args.get('file_uploaded')
    return render_template('upload.html', uploaded=uploaded)

@app.route('/download', methods=['GET'])
def web_download():
    files = getFiles(filesFolder)
    return render_template('download.html', fileTree=files)

@app.route('/download/<path:filepath>', methods=['GET'])
def web_download_file(filepath):
    requestedFile = filesFolder / filepath
    if requestedFile.is_file() == False:
        return redirect('/download')
    return send_from_directory(requestedFile.parent, requestedFile.name, as_attachment=True)

@app.route('/upload', methods=['POST'])
def web_upload_post():
    if 'file' not in request.files:
        return redirect('/upload?file_uploaded=0')

    file = request.files['file']
    if not file:
        return redirect('/upload?file_uploaded=0')

    filename = secure_filename(file.filename)
    if filename == False:
        return redirect('/upload?file_uploaded=0')
    with open(filesFolder / filename, 'wb') as f:
        file.save(f)
    return redirect('/upload?file_uploaded=1')

app.run(host='0.0.0.0', port=8080)