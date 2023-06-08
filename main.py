from pyzbar.pyzbar import decode
from PIL import Image

def read_barcode(file_path):
    # Open the image file
    img = Image.open(file_path)
    
    # Use pyzbar to find and decode the barcode in the image
    barcodes = decode(img)
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        barcode_type = barcode.type
        print(f"[INFO] Found {barcode_type} barcode: {barcode_data}")

# Usage
# list all png and jpg files in the current directory
import glob
for file_path in glob.glob("*.png") + glob.glob("*.jpg"):
    print(f"{file_path} - {read_barcode(file_path)}")