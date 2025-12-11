# In backend/utils.py

from PIL import Image
import io
import os

def resize_and_compress(input_image_path, output_path_absolute, output_format="jpeg"):
# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Function signature corrected
    """
    Resizes the image and attempts to compress it below 500 KB using Pillow.
    
    Args:
        input_image_path (str): The absolute path to the creative input.
        output_path_absolute (str): The absolute, writable path (e.g., from tempfile.gettempdir()) for the final output.
        output_format (str): The desired output format (e.g., 'jpeg').
        
    Returns:
        tuple: (output_path: str, status_msg: str)
    """
    
    try:
        # NOTE: Make sure your app.py is passing a valid path here!
        img = Image.open(input_image_path)
    except Exception as e:
        return None, f"Image Load Error: {e}"

    # 1. Resize (Standardizing the output size to meet required formats)
    img = img.resize((1080, 1080))
    
    # 2. Compression Loop (Target: <500KB)
    quality = 95
    
    # --- CRITICAL FIX: The output path is now the absolute path passed from app.py ---
    output_path = output_path_absolute # Use the safe path provided by the caller
    # ---------------------------------------------------------------------------------

    while quality >= 30: # Stop if quality drops too low
        buffer = io.BytesIO()
        # Save as JPEG for better compression
        img.save(buffer, format='JPEG', quality=quality) 
        
        size_kb = buffer.tell() / 1024
        
        if size_kb <= 500:
            # Save the final optimized image to the safe, absolute path
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())
            
            return output_path, f"Optimization successful! Size: {size_kb:.2f} KB (Quality: {quality})"
        
        quality -= 5 # Reduce quality
    
    return None, f"Could not optimize image below 500 KB. Final size: {size_kb:.2f} KB"

# Placeholder for simple background removal logic (demonstrates CV/ML concept)
def remove_background(image_path):
    # This function is okay as it just prints and doesn't write to the file system.
    print(f"Applying AI segmentation to remove background from {image_path}...")
    return image_path.replace("original", "processed_no_bg")
