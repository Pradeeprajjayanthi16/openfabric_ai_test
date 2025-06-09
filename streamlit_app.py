import streamlit as st
import requests
import base64

st.set_page_config(page_title="AI 3D Generator", layout="centered")
st.title("🎨 AI-Powered Image & 3D Model Generator")

prompt = st.text_input("Describe your imagination:", "A glowing dragon standing on a cliff at sunset")

if st.button("Generate"):
    with st.spinner("Processing your imagination..."):
        # Call your local Openfabric backend
        response = requests.post("http://localhost:8888/execution", json={"request": {"prompt": prompt}})
        result = response.json()

        # Show response message
        st.success(result['response']['message'])

        # Try displaying the saved image and 3D model
        try:
            with open("generated_image.png", "rb") as f:
                st.image(f.read(), caption="🎨 Generated Image")
            with open("generated_model.glb", "rb") as f:
                btn = st.download_button("⬇ Download 3D Model", data=f, file_name="model.glb")
        except Exception as e:
            st.warning(f"Could not find files: {e}")