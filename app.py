from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import base64
import csv
from datetime import datetime

app = Flask(__name__)

# Folder Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PHOTO_FOLDER = os.path.join(BASE_DIR, 'static', 'photos')
CSV_FILE = os.path.join(BASE_DIR, 'absensi_siswa.csv')

# Ensure photo folder exists
if not os.path.exists(PHOTO_FOLDER):
    os.makedirs(PHOTO_FOLDER)

# Initialize CSV if not exists
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["Nama Lengkap", "Kelas", "Waktu", "File Foto"])

init_csv()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit_absensi():
    try:
        data = request.json
        name = data.get('name')
        class_name = data.get('class')
        photo_data = data.get('photo')
        
        if not name or not class_name or not photo_data:
            return jsonify({"status": "error", "message": "Data tidak lengkap"}), 400

        # Decode photo
        header, encoded = photo_data.split(",", 1)
        photo_bytes = base64.b64decode(encoded)
        
        # Unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        photo_filename = f"{name.replace(' ', '_')}_{timestamp}.png"
        photo_path = os.path.join(PHOTO_FOLDER, photo_filename)
        
        with open(photo_path, "wb") as f:
            f.write(photo_bytes)
            
        # Save to CSV
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([name, class_name, waktu_sekarang, photo_filename])
        
        return jsonify({
            "status": "success", 
            "message": "Absensi berhasil disimpan",
            "data": {
                "name": name,
                "class": class_name,
                "time": waktu_sekarang,
                "photo": photo_filename
            }
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/view')
def view_absensi():
    rows = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    
    header = rows[0] if rows else []
    data = rows[1:][::-1] if len(rows) > 1 else []
    return render_template('view.html', header=header, data=data)

if __name__ == '__main__':
    # Use port from environment for deployment
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
