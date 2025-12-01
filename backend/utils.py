# In backend/utils.py

from PIL import Image
import io
import os

def resize_and_compress(input_image_path, output_format="jpeg"):
    """
    Resizes the image and attempts to compress it below 500 KB using Pillow.
    
    Args:
        input_image_path (str): The absolute path to the creative compiled by the UI.
        output_format (str): The desired output format (e.g., 'jpeg').
        
    Returns:
        tuple: (output_path: str, status_msg: str)
    """
    
    try:
        img = Image.open(input_image_path)
    except Exception as e:
        return None, f"Image Load Error: {e}"

    # 1. Resize (Standardizing the output size to meet required formats)
    # The creative is resized to 1080x1080 as a standard social media format.
    img = img.resize((1080, 1080))
    
    # 2. Compression Loop (Target: <500KB)
    quality = 95
    # Define a safe output path relative to the input directory
    base_name = os.path.basename(input_image_path).split('.')[0]
    
    # Use the same directory as the input for output (backend/temp/)
    output_dir = os.path.dirname(input_image_path)
    output_filename = f"optimized_{base_name}.{output_format}"
    output_path = os.path.join(output_dir, output_filename)

    while quality >= 30: # Stop if quality drops too low
        buffer = io.BytesIO()
        # Save as JPEG for better compression
        img.save(buffer, format='JPEG', quality=quality) 
        
        size_kb = buffer.tell() / 1024
        
        if size_kb <= 500:
            # Save the final optimized image
            with open(output_path, 'wb') as f:
                f.write(buffer.getvalue())
            
            return output_path, f"Optimization successful! Size: {size_kb:.2f} KB (Quality: {quality})"
        
        quality -= 5 # Reduce quality
    
    return None, f"Could not optimize image below 500 KB. Final size: {size_kb:.2f} KB"

# Placeholder for simple background removal logic (demonstrates CV/ML concept)
def remove_background(image_path):
    # In the prototype, this function would call a simple OpenCV or ML model.
    # For now, it just demonstrates the API call:
    print(f"Applying AI segmentation to remove background from {image_path}...")
    # Return path to processed image
    return image_path.replace("original", "processed_no_bg")