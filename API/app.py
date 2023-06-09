import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename

load_dotenv()
app = Flask(__name__)
# UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = os.environ.get('UPLOAD_FOLDER')


@app.route('/add', methods=['POST'])
def add_file():
    """
    Handle the file upload request endpoint.
    That endpoint will be called by the user script,
    and will save the file to the uploads' folder.

    :return: the unique file name for the uploaded file
    """
    if 'upload_file' not in request.files:
        return jsonify({'message': 'No file part'}), 400
    file = request.files['upload_file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    uuid, filename = generate_unique_filename(file)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(save_path)
    return jsonify({'message': 'File uploaded successfully',
                    'uuid': uuid}), 200


@app.route('/get/<uuid>', methods=['GET'])
def get_file_status(uuid):
    """
    Handle the file status request endpoint.
    That endpoint will be called by the user script,
    and will return the status of the file with the given uuid.

    :param uuid: the unique identifier of the file
    :return: the status of the file
    """
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        if uuid in file:
            if file.startswith("pending"):
                return jsonify({'message': 'File is pending'}), 200
            elif file.startswith("done"):
                return jsonify({'message': 'File is done'}), 200
        else:
            return jsonify({'message': 'File not found'}), 404
def generate_unique_filename(file) -> (str, str):
    """Generate a new unique file name.

    Args:
        file: The file to upload.

    Returns:
        A tuple containing the generated unique identifier (uid) and the new file name.
    """
    uid = str(uuid.uuid4())
    split_filename = os.path.splitext(secure_filename(file.filename))
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = secure_filename(split_filename[0])
    file_ext = split_filename[1]
    new_filename = f"pending_{filename}_{timestamp}_{uid}{file_ext}"
    return uid, new_filename


def create_folders_if_not_exists():
    if not os.path.exists(os.environ.get('UPLOAD_FOLDER')):
        os.mkdir(os.environ.get('UPLOAD_FOLDER'))
    if not os.path.exists(os.environ.get('OUTPUT_FOLDER')):
        os.mkdir(os.environ.get('OUTPUT_FOLDER'))


if __name__ == '__main__':
    create_folders_if_not_exists()
    app.run(debug=True)
