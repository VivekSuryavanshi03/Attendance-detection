import os
import face_recognition
import numpy as np
import csv
from datetime import datetime

ENROLLMENT_FOLDER = "enrollment_images"
ATTENDANCE_LOG_FOLDER = "attendance_logs"
TOLERANCE = 0.55
MODEL = "hog"

def load_known_faces():
    known_face_encodings = []
    known_face_names = []

    if not os.path.exists(ENROLLMENT_FOLDER):
        return known_face_encodings, known_face_names

    for person_name in os.listdir(ENROLLMENT_FOLDER):
        person_dir = os.path.join(ENROLLMENT_FOLDER, person_name)
        if os.path.isdir(person_dir):
            for filename in os.listdir(person_dir):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    try:
                        path = os.path.join(person_dir, filename)
                        image = face_recognition.load_image_file(path)
                        locations = face_recognition.face_locations(image, model=MODEL)
                        if locations:
                            encodings = face_recognition.face_encodings(image, known_face_locations=locations)
                            if encodings:
                                known_face_encodings.append(encodings[0])
                                known_face_names.append(person_name)
                    except Exception as e:
                        print(f"Error loading {filename} for {person_name}: {e}")
    return known_face_encodings, known_face_names

def get_today_log_filename():
    if not os.path.exists(ATTENDANCE_LOG_FOLDER):
        os.makedirs(ATTENDANCE_LOG_FOLDER)
    today = datetime.now().strftime("%Y-%m-%d")
    return os.path.join(ATTENDANCE_LOG_FOLDER, f"attendance_{today}.csv")

def mark_attendance(name):
    filename = get_today_log_filename()
    already_present = set()

    if os.path.exists(filename):
        with open(filename, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if row:
                    already_present.add(row[0])

    if name in already_present:
        return False

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if os.path.getsize(filename) == 0:
            writer.writerow(['Name', 'Timestamp'])
        writer.writerow([name, timestamp])
    return True
