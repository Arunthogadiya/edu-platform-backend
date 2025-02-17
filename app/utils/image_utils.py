import base64
from io import BytesIO
from PIL import Image

def convert_to_base64(image_data):
    """
    Convert PIL images or image data to Base64 encoded strings
    """
    if isinstance(image_data, Image.Image):
        pil_image = image_data
    else:
        pil_image = Image.open(BytesIO(image_data))
    
    buffered = BytesIO()
    pil_image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str
