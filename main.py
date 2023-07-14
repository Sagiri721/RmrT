from PIL import Image, ImageDraw;
import pytesseract;
import numpy;
import cv2;
import uuid;
from manga_ocr import MangaOcr;

import interface;
import utils;
import nlp;

utils.load_settings();

mocr = MangaOcr();
pytesseract.pytesseract.tesseract_cmd = r'D:\\Program Files\\Tesseract-OCR\\tesseract.exe'
file = "kissxpeak.jpg";
outline_color = (204, 0, 0, 255);

def save_image_from_array(array, name=uuid.uuid4()):
    
    data = Image.fromarray(array).convert('RGB');
    data.save(f'output/{name}.png');

def apply_image_processing(img):

    # Apply 300PPI to image
    width, height = img.size;
    factor = min(1, float(1024.0 / width));

    size = int(factor * width), int(factor * height);
    im_resized = img.resize(size, Image.LANCZOS);

    # Turn image to array
    img = numpy.array(im_resized);
    norm_img = numpy.zeros((img.shape[0], img.shape[1]));

    # Remove noise
    img = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15);

    # Grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY);
    
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX);
    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1];
    img = cv2.GaussianBlur(img, (1, 1), 0);

    #save_image_from_array(img);

    return img;

def draw_boxes(image, boxes):
    
    # Number of boxes to draw
    n = len(boxes['level']);
    draw = ImageDraw.Draw(image);

    for i in range(n):

        # Parse the box to a tuple
        (x, y, w, h) = (
            boxes['left'][i],
            boxes['top'][i],
            boxes['width'][i],
            boxes['height'][i],
        );

        # Overlay box on image
        draw.rectangle(
            [(x, y), (x+w, y+h)],
            fill=None,
            outline='red',
            width=2
        );

    image.save(f'output/boxes.png');

def analize_section(x, y, w, h, gui):
    
    subimage = Image.open(f"files/{file}").crop( (x, y, w, h) );

    #img = apply_image_processing(img=subimage);
    #save_image_from_array(img, f"crop-{uuid.uuid4()}.png");

    #img = Image.fromarray(img).convert('RGB');

    data = mocr(subimage);
    gui.update_text(data);

    processed = nlp.nlp_sentence(data);