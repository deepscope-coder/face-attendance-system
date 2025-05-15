from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.utils.face_recognition import FaceRecognizer
from app.models import Attendance
from app import db
from datetime import datetime
import base64
import numpy as np
import cv2

bp = Blueprint('main', __name__)
face_recognizer = FaceRecognizer()

@bp.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@bp.route('/recognize', methods=['POST'])
def recognize():
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({'status': 'error', 'message': 'No image data provided'}), 400
            
        image_data = data['image'].split(',')[1]
        image_bytes = base64.b64decode(image_data)
        image_array = np.frombuffer(image_bytes, dtype=np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
        
        faces = face_recognizer.app.get(frame)
        if not faces:
            return jsonify({
                'status': 'no_face',
                'message': 'No face detected in the image'
            }), 404
        
        emb = faces[0].embedding
        result = face_recognizer.recognize_face(emb)
        
        if result['status'] == 'success':
            # Save the captured image
            bbox = faces[0].bbox.astype(int)
            cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
            cv2.putText(frame, 
                       f"{result['name']} ({result['score']:.2f})", 
                       (bbox[0], bbox[1] - 10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imwrite('app/static/captured.jpg', frame)
            
            return jsonify(result)
        else:
            return jsonify(result), 404
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Recognition failed: {str(e)}'
        }), 500

@bp.route('/recognized/<class_id>/<name>', methods=['GET', 'POST'])
def recognized(class_id, name):
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'enter':
            # Check for existing unexited record
            last_record = Attendance.query.filter_by(
                class_id=class_id,
                person_name=name,
                exit_time=None
            ).order_by(Attendance.entry_time.desc()).first()
            
            if last_record:
                flash(f'{name} has already entered without exiting!', 'error')
            else:
                # Create new entry record
                attendance = Attendance(
                    class_id=class_id,
                    person_name=name,
                    action='enter',
                    entry_time=datetime.utcnow()
                )
                db.session.add(attendance)
                db.session.commit()
                flash(f'{name} entered successfully!', 'success')
        
        elif action == 'exit':
            # Find most recent entry without exit
            record = Attendance.query.filter_by(
                class_id=class_id,
                person_name=name,
                exit_time=None
            ).order_by(Attendance.entry_time.desc()).first()
            
            if record:
                record.exit_time = datetime.utcnow()
                record.duty_duration = record.exit_time - record.entry_time
                record.action = 'exit'
                db.session.commit()
                flash(f'{name} exited successfully! Duty duration: {record.duty_duration}', 'success')
            else:
                flash(f'{name} has no active entry to exit from!', 'error')
        
        return redirect(url_for('main.home'))
    
    # GET request - show recent records
    records = Attendance.query.filter_by(class_id=class_id)\
                            .order_by(Attendance.entry_time.desc())\
                            .limit(5).all()
    return render_template('recognized.html', 
                         class_id=class_id, 
                         name=name, 
                         records=records,
                         score=request.args.get('score', 0.0))

@bp.route('/not_recognized')
def not_recognized():
    score = request.args.get('score', 0.0)
    message = request.args.get('message', 'Sorry, we couldn\'t recognize you.')
    return render_template('not_recognized.html', score=score, message=message)