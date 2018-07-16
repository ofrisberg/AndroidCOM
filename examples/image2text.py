from PIL import Image
import pytesseract
import cv2
import os

"""

C:/Users/Olle/AppData/Local/Programs/Python/Python36-32/lib/site-packages/pytesseract/pytesseract.py

Inspiration
https://www.pyimagesearch.com/2017/07/10/using-tesseract-ocr-python/
https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
"""

#setup
pytesseract.tesseract_cmd = "C:\\Program Files (x86)\\Tesseract-OCR\\tesseract"

# load the example image and convert it to grayscale
url = "C:\\Users\\Olle\\Desktop\\python-projects\\AndroidCOM\\tmp\\tmp_androidcom_screen.png"
image = cv2.imread(url)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 3)
filename = str(os.getpid())+".png"
cv2.imwrite(filename, gray)

text = pytesseract.image_to_string(Image.open(filename))

#os.remove(filename)

print(text)