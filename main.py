import os
from pdf2image import convert_from_path
from PIL import Image, ImageDraw, ImageFont
import pytesseract
from googletrans import Translator, LANGUAGES


def pdf_to_images(pdf_path):
    # Convert PDF to a list of images
    images = convert_from_path(pdf_path)
    paths = []

    # Loop through the images list and save each page as an image
    for i, image in enumerate(images):
        image_path = f'page_{i+1}.png'
        image.save(image_path, 'PNG')
        paths.append(image_path)

    return paths


def translate_image_text(image_path, orig_lang='rus', target_lang='en'):
    # Open the image
    img = Image.open(image_path)

    # Use pytesseract to extract text
    extracted_text = pytesseract.image_to_string(img, lang=orig_lang)

    # Translate the extracted text
    translated_text = translator.translate(extracted_text, dest=target_lang)

    return translated_text.text


def extract_text_positions(image_path):
    # Open the image
    img = Image.open(image_path)
    
    # Use pytesseract to extract details
    # include_boxes_flag=True returns a list of boxes along with the detected text
    # Each box contains the text, and its position as (left, top, right, bottom)
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    n_boxes = len(data['text'])
    for i in range(n_boxes):
        if int(data['conf'][i]) > 60:  # Confidence threshold to filter weak detections
            (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            text = data['text'][i]
            print(f"Text: {text}, Position: (x: {x}, y: {y}, w: {w}, h: {h})")


# def translate_and_overlay_text(image_path, target_lang='en'):
#     # Load the image
#     img = Image.open(image_path)
#     draw = ImageDraw.Draw(img)
    
#     # For simplicity, using default font, adjust size as needed
#     try:
#         # Try to use a nicer font if available
#         font = ImageFont.truetype("arial.ttf", 15)
#     except IOError:
#         # Fallback to default PIL font
#         font = ImageFont.load_default()
    
#     # Extract text and positions
#     data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
#     # Iterate through each text item
#     for i in range(len(data['text'])):
#         if int(data['conf'][i]) > 60:  # Filter out uncertain OCR
#             text = data['text'][i]
#             # Translate the text
#             translated_text = translator.translate(text, dest=target_lang).text
            
#             # Get the position
#             (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
            
#             # Draw a white rectangle to cover the original text
#             draw.rectangle([x, y, x + w, y + h], fill="white")
            
#             # Draw the translated text
#             draw.text((x, y), translated_text, fill="black", font=font)
    
#     # Save or display the image
#     img.show()  # Or use img.save('translated_image.jpg')



def translate_and_overlay_text(image_path, target_lang='en'):
    # Load the image
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # For simplicity, using default font, adjust size as needed
    try:
        # Try to use a nicer font if available
        font = ImageFont.truetype("arial.ttf", 15)
    except IOError:
        # Fallback to default PIL font
        font = ImageFont.load_default()
    
    # Extract text and positions
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
    
    for i in range(len(data['text'])):
        if int(data['conf'][i]) > 60:  # Filter out uncertain OCR
            text = data['text'][i]
            if text.strip() != '':  # Ensure text is not empty
                # Translate the text
                result = translator.translate(text, dest=target_lang)
                translated_text = result.text
                
                # Get the position
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                
                # Draw a white rectangle to cover the original text
                draw.rectangle([x, y, x + w, y + h], fill="white")
                
                # Draw the translated text
                draw.text((x, y), translated_text, fill="black", font=font)
    
    # Save or display the image
    img.show()  # Or img.save('translated_image.jpg')


if __name__ == "__main__":
    # Specify the path to your PDF file
    pdf_path = os.path.join(os.path.dirname(__file__), 'examples/shengen_visa_form.pdf')
    paths = pdf_to_images(pdf_path)

    # Initialize the Translator
    translator = Translator()
    orig_lang = 'rus'
    target_lang = 'en'

    
    # 1.
    # # Example usage
    # translated_text = translate_image_text(paths[0], orig_lang, target_lang)
    # print("Translated Text:", translated_text)

    # 2.
    # # Example usage
    # extract_text_positions(paths[0])


    # 3.    
    # Specify the image path and target language
    image_path = paths[0]
    translate_and_overlay_text(paths[0], target_lang)
