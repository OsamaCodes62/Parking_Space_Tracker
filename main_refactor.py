import cv2
import pickle
import cvzone
import numpy as np
import tkinter as tk
from tkinter import filedialog
import os

# Constants
PARKING_POS_FILE = 'CarParkPos'
POLYGONS_FILE = 'polygons'
WIDTH, HEIGHT = 107, 48
VIDEO_FOLDER = 'videos'
IMG_FOLDER = 'img'

def load_positions(file_path):
    """Load parking positions from a file."""
    try:
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return []

def save_positions(file_path, positions):
    """Save parking positions to a file."""
    with open(file_path, 'wb') as f:
        pickle.dump(positions, f)

def select_video_file():
    """Open file dialog to select a video file."""
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(initialdir=VIDEO_FOLDER, filetypes=[("Video Files", "*.mp4;*.avi;*.mov")])
    return file_path if file_path else None

def get_corresponding_image(video_file):
    """Retrieve corresponding image for the selected video file."""
    base_name = os.path.splitext(os.path.basename(video_file))[0]
    img_path = os.path.join(IMG_FOLDER, f"{base_name}.png")
    return img_path if os.path.exists(img_path) else None

def setup_trackbars():
    """Setup trackbars for adaptive threshold tuning."""
    cv2.namedWindow("Threshold Adjustments")
    cv2.resizeWindow("Threshold Adjustments", 640, 240)
    cv2.createTrackbar("Block Size", "Threshold Adjustments", 25, 50, lambda x: None)
    cv2.createTrackbar("Constant", "Threshold Adjustments", 16, 50, lambda x: None)
    cv2.createTrackbar("Blur", "Threshold Adjustments", 5, 50, lambda x: None)

def get_trackbar_values():
    """Retrieve values from trackbars."""
    val1 = cv2.getTrackbarPos("Block Size", "Threshold Adjustments")
    val2 = cv2.getTrackbarPos("Constant", "Threshold Adjustments")
    val3 = cv2.getTrackbarPos("Blur", "Threshold Adjustments")
    return max(3, val1 if val1 % 2 == 1 else val1 + 1), val2, max(3, val3 if val3 % 2 == 1 else val3 + 1)

def process_frame(img, val1, val2, val3):
    """Apply image processing techniques to detect free spaces."""
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_thres = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                      cv2.THRESH_BINARY_INV, val1, val2)
    img_thres = cv2.medianBlur(img_thres, val3)
    kernel = np.ones((3, 3), np.uint8)
    return cv2.dilate(img_thres, kernel, iterations=1)

def check_spaces(img, img_thres, pos_list):
    """Check available parking spaces and display information."""
    spaces = 0
    for x, y in pos_list:
        img_crop = img_thres[y:y + HEIGHT, x:x + WIDTH]
        count = cv2.countNonZero(img_crop)
        color = (0, 200, 0) if count < 900 else (0, 0, 200)
        thickness = 5 if count < 900 else 2
        spaces += 1 if count < 900 else 0
        cv2.rectangle(img, (x, y), (x + WIDTH, y + HEIGHT), color, thickness)
        cv2.putText(img, str(count), (x, y + HEIGHT - 6), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)
    cvzone.putTextRect(img, f'Free: {spaces}/{len(pos_list)}', (50, 60), thickness=3, offset=20, colorR=(0, 200, 0))

def main():
    """Main function to process video frames and detect available parking spaces."""
    video_file = select_video_file()
    if not video_file:
        print("No video file selected. Exiting.")
        return
    cap = cv2.VideoCapture(video_file)
    pos_list = load_positions(POLYGONS_FILE) or load_positions(PARKING_POS_FILE)
    img_path = get_corresponding_image(video_file)
    setup_trackbars()
    
    while cap.isOpened():
        success, img = cap.read()
        if not success or cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        val1, val2, val3 = get_trackbar_values()
        img_thres = process_frame(img, val1, val2, val3)
        check_spaces(img, img_thres, pos_list)
        cv2.imshow("Parking Monitor", img)
        if img_path:
            img_static = cv2.imread(img_path)
            cv2.imshow("Reference Image", img_static)
        if cv2.waitKey(1) & 0xFF == 27:  # Exit on 'ESC'
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
