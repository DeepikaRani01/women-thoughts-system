import os
import base64
import uuid
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, User

camera_bp = Blueprint('camera', __name__)

# Try to import DeepFace, but don't crash if it's not installed yet
try:
    from deepface import DeepFace
    DEEPFACE_AVAILABLE = True
except ImportError:
    DEEPFACE_AVAILABLE = False

@camera_bp.route('/api/verify-gender', methods=['POST'])
def verify_gender():
    data = request.json
    image_data = data.get('image')

    if not image_data:
        return jsonify({'verified': False, 'message': 'No image data received'})

    # Mock success if DeepFace is not available (for demonstration)
    if not DEEPFACE_AVAILABLE:
        return jsonify({
            'verified': True, 
            'message': 'Verification bypassed (DeepFace not installed). Simulated: Female'
        })

    try:
        # Decode base64 image
        header, encoded = image_data.split(",", 1)
        data = base64.b64decode(encoded)
        
        # Save temp file
        temp_filename = f"temp_{uuid.uuid4()}.jpg"
        temp_path = os.path.join('static', 'images', temp_filename)
        
        with open(temp_path, "wb") as f:
            f.write(data)

        # Run Analysis
        objs = DeepFace.analyze(img_path=temp_path, actions=['gender'], enforce_detection=False)
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

        dominant_gender = objs[0]['dominant_gender']
        
        if dominant_gender == 'Woman':
            return jsonify({'verified': True, 'message': '✅ Verified as Female'})
        else:
            return jsonify({'verified': False, 'message': '❌ Could not verify as Female'})

    except Exception as e:
        print(f"Gender Verification Error: {e}")
        return jsonify({'verified': False, 'message': f"Error during verification: {str(e)}"})
