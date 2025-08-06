import cv2
import numpy as np
import os

def extract_signature_regions(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (21, 21), 0)
    normalized = cv2.divide(gray, blur, scale=255)
    thresh = cv2.adaptiveThreshold(normalized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY_INV, 15, 10)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 4))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    bounding_boxes = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        if w * h > 100:  # simple filter
            bounding_boxes.append((x, y, w, h))
    return bounding_boxes

def save_signatures(img, boxes, output_folder, image_name):
    os.makedirs(output_folder, exist_ok=True)
    count = 0
    for x, y, w, h in boxes:
        pad = 10
        sig = img[max(0, y - pad):y + h + pad, max(0, x - pad):x + w + pad]
        output_path = os.path.join(output_folder, f"signature_{count}_{image_name}")
        cv2.imwrite(output_path, sig)
        count += 1
    return count
