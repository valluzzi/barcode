from pyzbar.pyzbar import decode
import numpy as np
import cv2
import pytesseract

def deskew_image_cv(file_path):
    # Load the image
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    #ret, img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)
    # Invert the image
    img = cv2.bitwise_not(img)

    # Detect lines in the image using the Hough transform
    coords = np.column_stack(np.where(img > 0))
    angle = cv2.minAreaRect(coords)[-1]
    print(angle)
    # The `cv2.minAreaRect` function returns values in the range [-90, 0); as the rectangle rotates clockwise the angle tends to 0 
    # so it's necessary to add 90 degrees to the angle if it's found in the range [-90,-45)
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    # Rotate the image to deskew it
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    deskewed_img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    return deskewed_img

def read_barcode(file_path):
    # Open the image file
    
    img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    # Apply binary thresholding
    threshold = 100
    _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    
    # Use pyzbar to find and decode the barcode in the image
    barcodes = decode(img)
    
    text = pytesseract.image_to_string(img).strip()
    print(f"[INFO] Text: <{text}>")
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        print(f"[INFO] Barcode {barcode.type}: {barcode_data}")

# Usage
# list all png and jpg files in the current directory
import glob
for file_path in glob.glob("*.png") + glob.glob("*.jpg"):
    print(f"{file_path} - {read_barcode(file_path)}")