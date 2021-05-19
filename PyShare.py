from flask import Flask, render_template, redirect, request, send_from_directory
from socket import gethostname, gethostbyname
from pathlib import Path
from os import listdir, chdir
from sys import argv

chdir(Path(__file__).parent)

def secure_filename(rawFilename):
    validatedFilename = ''
    for letter in rawFilename:
        # using global allowed
        if letter in allowed:
            validatedFilename += letter
    if validatedFilename in listdir(filesFolder):
        filedata = validatedFilename.rsplit('.', 1)
        if len(filedata) == 1:
            filedata = [filedata, '']
        antiCopy = 0
        while (filedata[0] + str(antiCopy) + filedata[1]) in listdir(filesFolder):
            antiCopy += 1
        filename = filedata[0] + str(antiCopy) + filedata[1]
    else:
        filename = validatedFilename
    return filename

def getFiles(folder):
    files = {'path': folder.relative_to(filesFolder).as_posix(), 'name': folder.name, 'files': []}
    for file in folder.iterdir():
        if file.is_dir():
            files['files'].append(getFiles(file))
        else:
            files['files'].append({'path': file.relative_to(filesFolder).as_posix(), 'name': file.name})
    return files

app = Flask(str(Path().absolute()), template_folder='web/HTML', static_folder='web/public')
filesFolder = Path('shared')
allowedFile = Path('allowed.txt')

if allowedFile.is_file():
    with open(allowedFile, 'r') as f:
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
    if str(requestedFile.relative_to(filesFolder))[:2] == '..':
        return redirect('/download')
    if requestedFile.is_file() == False:
        return redirect('/download')
    print(requestedFile, requestedFile.parent, requestedFile.name)
    return send_from_directory(requestedFile.parent, requestedFile.name, as_attachment=True)

@app.route('/upload', methods=['POST'])
def web_upload_post():
    if 'file' not in request.files:
        return '{"success":false, "message":"file not found"}'

    file = request.files['file']
    if not file:
        return '{"success":false, "message":"file not found"}'

    filename = secure_filename(file.filename)
    with open(filesFolder / filename, 'wb') as f:
        file.save(f)
    return '{"success":true, "message":"file uploaded"}'

port = 8080

for i in range(len(argv)):
    if argv[i] == '-p' or argv[i] == '--port':
        try:
            port = int(argv[i+1])
        except Exception:
            pass

print('website: http://' + gethostbyname(gethostname()) + ':' + str(port))
app.run(host='0.0.0.0', port=port)
