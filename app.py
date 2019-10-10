import io
import os
import qrcode
import urllib.request
from flask import *
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	

@app.route('/', methods = ['GET', 'POST'])
def upload_form():
    
    if request.method == 'GET':
	    return render_template('upload.html')

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)

    file = request.files['file']

    if file.filename == '':
        flash('No file selected for uploading')
        return redirect(request.url)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # qr = qrcode.make(url_for(return_file, filename=filename))
        flash('File successfully uploaded')
        qr = qrcode.make(str(request.base_url) + '/download/' + filename) 
        qr.save(f'./static/qrcodes/qr_code.png', quality=70)   
        return redirect(url_for('display_qr'))
    else:
        flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
        return redirect(request.url)
		

@app.route('/download/<filename>', methods=['GET'])
def return_file(filename):
    return send_from_directory(directory='./uploads', filename=filename, as_attachment=True)


@app.route('/download/display_qr', methods = ['GET'])
def display_qr():
    return render_template('qr_display.html')


if __name__ == "__main__":
    app.run()