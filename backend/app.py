# In backend/app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
from compliance_engine import check_logo_position, calculate_risk_score, check_text_compliance
from utils import resize_and_compress, remove_background
import os

# --- 1. Define the absolute paths robustly ---
# Gets the absolute path to the current directory (backend/)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
# Gets the path to the static folder (one level up)
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static') 
# Gets the path to the temporary storage folder
TEMP_DIR = os.path.join(BASE_DIR, 'temp')


# --- 2. Initialize Flask and enable CORS ---
app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app) 
app.config['PREFERRED_URL_SCHEME'] = 'https'

# --- 3. Add the root route ('/') to serve index.html ---
@app.route('/')
def serve_index():
    """Serves the main index.html file from the static folder."""
    return send_from_directory(STATIC_DIR, 'index.html')


@app.route('/api/check-compliance', methods=['POST'])
def check_compliance():
    """
    API endpoint to check the current creative layout and provide real-time feedback.
    """
    data = request.json
    
    logo_coords = data.get('logo_coords')
    logo_dims = data.get('logo_dims')
    creative_text = data.get('headline_text', '')
    creative_dims = data.get('creative_dims', [1080, 1080])

    violations = []
    
    # 1. Positional Compliance Check (CV-based Guardrail)
    if logo_coords and logo_dims:
        compliant, msg = check_logo_position(logo_coords, logo_dims, creative_dims)
        if not compliant:
            violations.append(msg)

    # 2. Text Compliance Check (NLP Concept)
    compliant_text, text_msg = check_text_compliance(creative_text)
    if not compliant_text:
        violations.append(text_msg)
        
    # 3. Final Score Aggregation
    risk_score, summary_msg = calculate_risk_score(violations)

    return jsonify({
        'compliance_score': risk_score,
        'summary': summary_msg,
        'violations': violations
    })


@app.route('/api/generate-output', methods=['POST'])
def generate_output():
    """
    API endpoint to finalize the creative and apply mandatory optimization.
    """
    # Use TEMP_DIR for the path where the input image should be saved
    final_image_path = os.path.join(TEMP_DIR, 'final_creative.png')
    
    # NOTE: You must ensure final_creative.png exists in backend/temp/ for this test to pass!
    if not os.path.exists(final_image_path):
        return jsonify({'error': f'Final image not found at {final_image_path}.'}), 400

    # Apply optimization and resizing
    output_path, status_msg = resize_and_compress(final_image_path, output_format='jpeg')
    
    if output_path:
        return jsonify({
            'success': True,
            'download_link': f'/downloads/{output_path}',
            'message': status_msg
        })
    else:
        return jsonify({'success': False, 'message': status_msg}), 500


if __name__ == '__main__':
    # Ensure you create the temp directory
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Run the server
    app.run(debug=True, port=5000)
