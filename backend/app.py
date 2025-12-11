# In backend/app.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS 
from compliance_engine import check_logo_position, calculate_risk_score, check_text_compliance
from utils import resize_and_compress
import os
import tempfile 
# from PIL import Image # Keeping PIL import clean to avoid dependency issues

# --- 1. Define the absolute paths robustly ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
STATIC_DIR = os.path.join(BASE_DIR, '..', 'static') 

# --- CRITICAL FIX: Use OS-agnostic temp folder. WORKS ON WINDOWS & RENDER (/tmp/) ---
# The tempfile module finds a path guaranteed to be writable on ANY OS.
INPUT_IMAGE_PATH = os.path.join(tempfile.gettempdir(), 'final_creative.png')
OUTPUT_IMAGE_PATH = os.path.join(tempfile.gettempdir(), 'optimized_final_creative.jpeg')


# --- 2. Initialize Flask and enable CORS ---
app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app) 
# Fix for Render: Ensures internal URLs are generated using the secure scheme
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
    
    # CRITICAL FIX: PLACEHOLDER IMAGE CREATION (If the file doesn't exist)
    # We must create a small placeholder file if it's missing, using a simple open/write
    # to avoid complex PIL crashes on initial deployment.
    if not os.path.exists(INPUT_IMAGE_PATH):
        try:
            # Create a minimal dummy file to ensure os.path.exists() passes
            with open(INPUT_IMAGE_PATH, 'w') as f:
                f.write('This is a dummy creative file for testing optimization.')
        except Exception as e:
            # If even creating a dummy file fails, something is wrong with the temp dir.
             return jsonify({'error': f'Cannot create temporary input file: {e}.'}), 500

    # Apply optimization and resizing (utils.py must be updated to use the correct path)
    # NOTE: The resize_and_compress function in utils.py MUST be updated to accept the output path
    output_path, status_msg = resize_and_compress(INPUT_IMAGE_PATH, OUTPUT_IMAGE_PATH, 'final_creative', output_format='jpeg') 
    
    if output_path:
        # NOTE: The client side (JavaScript) expects the final size and message
        return jsonify({
            'success': True,
            'message': status_msg,
            # Ensure the file size is calculated correctly from the output path
            'final_size_kb': os.path.getsize(output_path) / 1024 
        })
    else:
        return jsonify({'success': False, 'message': status_msg}), 500


# --- 4. NEW ROUTE: Serve the optimized file for download ---
@app.route('/downloads/<filename>')
def serve_optimized_file(filename):
    """Allows the user to download the file saved in the temporary folder."""
    # CRITICAL FIX: Serve file directly from the writable temp folder
    return send_from_directory(tempfile.gettempdir(), filename, as_attachment=True)


if __name__ == '__main__':
    # Run the server locally 
    # NOTE: os.makedirs() is deleted, resolving the read-only error on Render.
    app.run(debug=True, port=5000)
