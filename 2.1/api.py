from flask import Flask, request, jsonify
from kafka import KafkaProducer
import json
import os
from werkzeug.utils import secure_filename
import pandas as pd

app = Flask(__name__)


KAFKA_BROKER = 'localhost:9092'
SENSOR_TOPIC = 'sensor-data'
DOCUMENT_TOPIC = 'document-uploads'


UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda x: json.dumps(x).encode('utf-8')  
)

# API 1: Upload files
@app.route('/upload-document', methods=['POST'])
def upload_document():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp', 'pdf'}
    file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
    if file_extension not in allowed_extensions:
        return jsonify({"error": "Only image files are allowed"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    document_metadata = {
        "filename": filename,
        "filepath": file_path,
        "size": os.path.getsize(file_path),
        "type": file_extension,
        "status": "uploaded"
    }

    producer.send(DOCUMENT_TOPIC, value=document_metadata)
    return jsonify({"message": "Image uploaded successfully", "metadata": document_metadata})

### API 2: Stream sensor data
@app.route('/upload-sensor-csv', methods=['POST'])
def upload_sensor_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)

    df = pd.read_csv(file_path)

    for _, row in df.iterrows():
        message = row.to_dict()
        producer.send(SENSOR_TOPIC, value=message)

    return jsonify({"message": "CSV data uploaded and sent to Kafka", "file": filename})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
