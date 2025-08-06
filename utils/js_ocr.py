from streamlit_js_eval import streamlit_js_eval
import streamlit as st
import base64

def run_tesseract_js(image_bytes):
    img_base64 = base64.b64encode(image_bytes).decode("utf-8")

    js_code = f"""
        async function runOCR() {{
            const {{ createWorker }} = await import('https://cdn.jsdelivr.net/npm/tesseract.js@5.0.3/dist/tesseract.min.js');

            const worker = await createWorker('eng');
            const img = document.getElementById("tesseractImage");
            const result = await worker.recognize(img);

            return result.data.text;
        }}
        runOCR()
    """

    st.markdown(f'<img id="tesseractImage" src="data:image/jpeg;base64,{img_base64}" style="display:none;">', unsafe_allow_html=True)
    result = streamlit_js_eval(js_expressions=js_code, key="ocr_output")
    return result
