# Flask API Usage Guide

## Prerequisites
Ensure Apache Kafka is running.

Create Kafka topics: `sensor-data` and `document-uploads`.

## Start Flask API
```sh
python api.py
```

## API Endpoints

### 1. Upload Image Document
**Endpoint:** `POST /upload-document`

- Accepts image files (`png`, `jpg`, `jpeg`, `gif`, `bmp`, `webp`, `pdf`).
- Saves them locally.
- Sends metadata to Kafka topic `document-uploads`.

#### Curl Command:
```sh
curl -X POST http://localhost:5000/upload-document -F "file=@path/to/image.jpg"
```

### 2. Upload Sensor Data (CSV)
**Endpoint:** `POST /upload-sensor-csv`

- Accepts CSV files with sensor data.
- Reads and streams each row to Kafka topic `sensor-data`.

#### Curl Command:
```sh
curl -X POST http://localhost:5000/upload-sensor-csv -F "file=@path/to/data.csv"
```
