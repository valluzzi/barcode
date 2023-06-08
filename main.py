from pyzbar.pyzbar import decode
import numpy as np
import cv2
import pytesseract

def deskew_image_cv(file_path):
    # Load image
    img = cv2.imread(file_path, 0)
    
    # Thresholding the image
    (thresh, img_bin) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    
    # Invert the image
    img_bin = 255-img_bin

    # Define a rectangular structuring element
    sz = np.array(img.shape) // 40
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, tuple(sz))

    # Apply dilation on the threshold image
    dilation = cv2.dilate(img_bin, rect_kernel, iterations = 1)

    # Find contours
    contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Loop over each contour
    angles = []
    for cnt in contours:
        # Get the minimum area rectangle
        rect = cv2.minAreaRect(cnt)
        angles.append(rect[-1])

    # Compute the median angle and rotate
    median_angle = np.median(angles)
    if median_angle > 45:
        median_angle -= 90
    img_rotated = rotate_image(img, -median_angle)

    return img_rotated

def rotate_image(mat, angle):
    # angle in degrees
    height, width = mat.shape[:2]
    image_center = (width / 2, height / 2)

    rotation_mat = cv2.getRotationMatrix2D(image_center, angle, 1.)

    abs_cos = abs(rotation_mat[0,0])
    abs_sin = abs(rotation_mat[0,1])

    bound_w = int(height * abs_sin + width * abs_cos)
    bound_h = int(height * abs_cos + width * abs_sin)

    rotation_mat[0, 2] += bound_w/2 - image_center[0]
    rotation_mat[1, 2] += bound_h/2 - image_center[1]

    rotated_mat = cv2.warpAffine(mat, rotation_mat, (bound_w, bound_h))
    return rotated_mat

def read_barcode(file_path):
    # Open the image file
    
    # img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
    # # Apply binary thresholding
    # threshold = 100
    # _, img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    
    img = deskew_image_cv(file_path)

    
    # Use pyzbar to find and decode the barcode in the image
    barcodes = decode(img)
    
    text = pytesseract.image_to_string(img).strip()
    print(f"[INFO] Text: <{text}>")
    

    print(f"[INFO] Found {len(barcodes)} barcode(s)")
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        print(f"[INFO] Barcode {barcode.type}: {barcode_data}")
    print("===========================")
    cv2.imshow(file_path,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# Usage
# list all png and jpg files in the current directory
import glob
for file_path in glob.glob("*.png") + glob.glob("*.jpg"):
    print(f"{file_path} - {read_barcode(file_path)}")