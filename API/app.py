import os
from dotenv import load_dotenv
import uuid
from datetime import datetime
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import json
import subprocess
from collections import OrderedDict
from DB.engine import Upload, User, session
from flask import Flask, request, jsonify
from DB.engine import Upload, User, session

load_dotenv()
app = Flask(__name__)
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
app.config['UPLOAD_FOLDER'] = os.path.join(MAIN_DIR, "uploads")


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

    email = request.form.get('email')
    user_id = None  # Initialize user_id as None

    if email:
        user = session.query(User).filter_by(email=email).first()
        if not user:
            # Create a new user if it doesn't exist
            user = User(email=email)
            session.add(user)
            session.commit()
        user_id = user.id  # Assign the user ID

    uid, filename = generate_unique_filename(file)
    try:
        upload = Upload(filename=filename, uid=uid, user_id=user_id)
        session.add(upload)
        session.commit()
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(save_path)
    except Exception as e:
        return jsonify({'message': e}), 500
    return jsonify({'message': 'File uploaded successfully',
                    'uuid': uid}), 200

@app.route('/get/<uuid>', methods=['GET'])
def get_file_status(uuid):
    """
    Handle the file status request endpoint.
    That endpoint will be called by the user script,
    and will return the status of the file with the given uuid.

    :param uuid: the unique identifier of the file
    :return: the status of the file
    """
    file = session.query(Upload).filter(Upload.uid == uuid).first()
    if not file:
        return jsonify({'status': 'not found'}), 404
    else:
        return jsonify({
            'status': file.status,
            'filename': file.filename,
            'upload_on': file.upload_time,
            'finish_on': file.finish_time,
            'explanation': None if file.status != 'done' else get_explanation(file.filename.split('.')[0])
        }), 200

    return jsonify({'status': 'not found'}), 404


def get_explanation(filename) -> object:
    """
    Retrieve the processed output explanation for the given UUID.
    This function retrieves the explanation from the corresponding JSON file.

    :param uuid: the unique identifier of the file
    :return: the processed output explanation if available, or None
    """
    print(filename)
    explanation_file_path = os.path.join(MAIN_DIR, os.environ.get('OUTPUT_FOLDER'), f"{filename}.json")
    print(explanation_file_path)
    if os.path.exists(explanation_file_path):
        with open(explanation_file_path, 'r') as json_file:
            explanation_data = json.load(json_file)
            return explanation_data
    return None


def generate_unique_filename(file) -> (str, str):
    """Generate a new unique file name.

    Args:
        file: The file to upload.

    Returns:
        A tuple containing the generated unique identifier (uid) and the new file name.
    """
    uid = str(uuid.uuid4())
    split_filename = os.path.splitext(secure_filename(file.filename))
    filename = secure_filename(split_filename[0])
    file_ext = split_filename[1]
    new_filename = f"{filename}_{uid}{file_ext}"
    return uid, new_filename


def run_file_monitoring_script():
    file_monitoring_script = os.path.join(os.path.dirname(__file__), "fileMonitoring.py")
    subprocess.Popen(["python3", file_monitoring_script])


if __name__ == '__main__':
    run_file_monitoring_script()
    app.run(debug=True)
