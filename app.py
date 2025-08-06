import streamlit as st
import numpy as np
import os
import shutil
import cv2
from signatureExtractor import extract_signature_regions, save_signatures
from utils.js_ocr import run_tesseract_js

st.set_page_config(page_title="Signature Extractor JS", layout="centered")
st.title("🖋️ Signature Extraction Tool with Tesseract.js")
st.markdown("Upload a document and extract signatures using browser-based OCR.")

if 'uploaded_file' not in st.session_state:
    st.session_state.uploaded_file = None

def clear_upload():
    st.session_state.uploaded_file = None
    if os.path.exists("temp_uploads"):
        shutil.rmtree("temp_uploads")
    if os.path.exists("extracted_signatures"):
        shutil.rmtree("extracted_signatures")

uploaded_file = st.file_uploader("Upload an Image (JPG/PNG)", type=["jpg", "jpeg", "png"], key="file_uploader")

if uploaded_file:
    st.session_state.uploaded_file = uploaded_file
    input_path = os.path.join("temp_uploads", uploaded_file.name)
    os.makedirs("temp_uploads", exist_ok=True)
    with open(input_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    st.image(input_path, caption="Uploaded Image", use_container_width=True)
    st.button("❌ Clear Upload", on_click=clear_upload)

    if st.button("🔍 Extract Signature"):
        with st.spinner("Running OCR and detecting signature regions..."):
            img = cv2.imread(input_path)
            boxes = extract_signature_regions(img)
            saved_count = save_signatures(img, boxes, "extracted_signatures", uploaded_file.name)

            ocr_text = run_tesseract_js(uploaded_file.getvalue())

        if saved_count > 0:
            st.success(f"✅ Extracted {saved_count} signature(s). Text: \n{ocr_text}")
            for file in os.listdir("extracted_signatures"):
                path = os.path.join("extracted_signatures", file)
                st.image(path, caption=file)
                with open(path, "rb") as f:
                    st.download_button(label=f"Download {file}", data=f, file_name=file, mime="image/png")
        else:
            st.warning("⚠️ No valid signature regions found.")

elif st.session_state.uploaded_file:
    st.session_state.uploaded_file = None
