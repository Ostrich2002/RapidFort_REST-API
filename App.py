from flask import Flask, request, jsonify, render_template , send_from_directory
from flask_pymongo import PyMongo
import os

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/files_db'
mongo = PyMongo(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    filename = os.path.basename(file.filename)
    mongo.db.files.insert_one({'filename': filename})

    file.save(os.path.join('uploads', filename))
    return jsonify({'message': 'File uploaded successfully'}), 200

# @app.route('/files', methods=['GET'])
# def get_files():
#     files = mongo.db.files.find({}, {'_id': 0})
#     file_list = [f for f in files]
#     return jsonify(file_list)

@app.route('/files', methods=['GET'])
def get_files():
    files = mongo.db.files.find({}, {'_id': 0})
    return render_template('files.html', files=files)

@app.route('/file/<filename>')
def view_file_content(filename):
    try:
        file_path = os.path.join('uploads', filename)
        if filename.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        else:
            # Handle binary files by providing a link to download them
            return send_from_directory('uploads', filename)
        
        return render_template('file_content.html', filename=filename, content=content)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404

#This endpoint provides a link to content of each file with filename on '/files' endpoint
@app.route('/file_content/<filename>')
def view_file_content_by_name(filename):
    try:
        file_path = os.path.join('uploads', filename)
        if filename.lower().endswith('.txt'):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
        else:
            # Handle binary files by providing a link to download them
            return send_from_directory('uploads', filename)
        
        return render_template('file_content.html', filename=filename, content=content)
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404
        

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
