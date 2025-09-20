import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="OMR Evaluation Dashboard",
    page_icon=":memo:",
    layout="wide",
)

# Custom CSS for colors
st.markdown(
    """
    <style>
    .main {background-color: #f0f8ff;}
    .stButton>button {background-color: #00bfff; color: white;}
    .stFileUploader>div {background-color: #e6f2ff;}
    .stSelectbox>div>div {background-color: #e6f2ff;}
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.markdown("<h1 style='text-align: center; color: #1e90ff;'>Automated OMR Evaluation & Scoring System</h1>", unsafe_allow_html=True)
st.markdown("---")

# Upload OMR sheet
uploaded_file = st.file_uploader("Upload OMR Sheet Image", type=["png", "jpg", "jpeg"])
version = st.selectbox("Select Sheet Version", ["version1", "version2", "version3", "version4"])

if uploaded_file and version:
    st.info(f"Evaluating {uploaded_file.name} for {version}...")
    
    try:
        # Send file to FastAPI backend
        files = {"file": (uploaded_file.name, uploaded_file, "image/jpeg")}
        data = {"version": version}
        response = requests.post("http://127.0.0.1:8000/evaluate/", files=files, data=data)
        response.raise_for_status()
        result = response.json()
        
        # Display results in colorful columns
        st.success("Evaluation Complete! ✅")
        st.markdown("### Per-subject Scores")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        subjects = list(result["scores"].keys())
        scores = list(result["scores"].values())
        colors = ["#FF6347", "#FFD700", "#32CD32", "#1E90FF", "#FF69B4"]
        
        for i, col in enumerate([col1, col2, col3, col4, col5]):
            col.markdown(f"<h3 style='color:{colors[i]}; text-align:center'>{subjects[i]}</h3>", unsafe_allow_html=True)
            col.markdown(f"<h2 style='color:{colors[i]}; text-align:center'>{scores[i]}/20</h2>", unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown(f"<h2 style='text-align: center; color:#8A2BE2;'>Total Score: {result['total']}/100</h2>", unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Failed to evaluate OMR sheet: {e}")
