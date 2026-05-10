import cv2
from pyzbar.pyzbar import decode

def initialize_camera(camera_index=1):
    cap = cv2.VideoCapture(camera_index)
    if not cap.isOpened():
        print("Error: Could not access the camera.")
        return None
    return cap

def scan_for_barcode(cap):
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        return None

    barcodes = decode(frame)

    barcode_data = None
    for barcode in barcodes:
        barcode_data = barcode.data.decode("utf-8")
        try:
            barcode_int = int(barcode_data)
            return barcode_int
        except ValueError:
            return barcode_data

    return None

def close_camera(cap):
    cap.release()
    
def scanBarcode() -> int:
    cap = None
    try:
        cap = initialize_camera()
        if cap is None:
            print("Exiting program due to camera initialization failure.")
            exit()

        while True:
            result = scan_for_barcode(cap)
            if result is not None:
                close_camera(cap)
                return result  

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if cap:
            close_camera(cap)
