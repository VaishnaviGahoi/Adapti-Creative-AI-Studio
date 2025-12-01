from PIL import Image
import numpy as np

# --- 1. CONFIGURATION (Ambiguous Guideline Rules) ---
MIN_MARGIN_PX = 20  # Logo must be at least 20px from edges
IMAGE_W = 1080      # Standard creative width (for ratio checks)
IMAGE_H = 1080      # Standard creative height

def check_logo_position(logo_coords, logo_dims, creative_dims):
    """
    Checks if the logo's position violates margin and quadrant rules.

    Args:
        logo_coords (tuple): (x_top_left, y_top_left) position of the logo provided by the UI.
        logo_dims (tuple): (width, height) of the logo.
        creative_dims (tuple): (creative_width, creative_height) of the canvas.
    
    Returns:
        tuple: (is_compliant: bool, violation_message: str)
    """

    # Unpack dimensions
    img_w, img_h = creative_dims
    x_tl, y_tl = logo_coords
    logo_w, logo_h = logo_dims

    # Calculate bottom-right corner of the logo
    x_br = x_tl + logo_w
    y_br = y_tl + logo_h

    # --- Rule 1: Minimum Margin Check ---
    margin_right = img_w - x_br
    margin_bottom = img_h - y_br

    if margin_right < MIN_MARGIN_PX:
        violation = MIN_MARGIN_PX - margin_right
        return False, f"Logo is too close to the right edge (Violation: {violation}px)."
    
    if margin_bottom < MIN_MARGIN_PX:
        violation = MIN_MARGIN_PX - margin_bottom
        return False, f"Logo is too close to the bottom edge (Violation: {violation}px)."

    # --- Rule 2: Quadrant Check (Must be in Bottom-Right) ---
    if x_tl < (img_w / 2) or y_tl < (img_h / 2):
         return False, "Logo must be placed within the bottom-right half of the creative."

    # If all primary checks pass
    return True, "Positional compliance passed."


def calculate_risk_score(violations):
    """
    Aggregates violations into a single risk score.
    """
    if not violations:
        # High score if no violations found
        return 98, "No major violations detected." 
    else:
        # Score drops significantly if any primary violation occurs
        return 45, "Major compliance violation detected." 

# Placeholder for text check (demonstrates NLP component concept)
def check_text_compliance(text_input):
    prohibited_words = ["guaranteed", "miracle", "risk-free"]
    for word in prohibited_words:
        if word in text_input.lower():
            return False, f"Text violates tone/claim rules: '{word}' is prohibited."
    return True, None