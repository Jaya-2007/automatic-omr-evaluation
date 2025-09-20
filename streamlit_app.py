import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Automated OMR Evaluation", layout="wide")
st.title("📊 Automated OMR Evaluation System")

uploaded_file = st.file_uploader("Upload OMR sheet image", type=["jpg","jpeg","png"])
if uploaded_file:
    version = st.text_input("Sheet Version", "1")
    if st.button("Evaluate"):
        files = {"file": (uploaded_file.name, uploaded_file, "image/jpeg")}
        try:
            response = requests.post("http://localhost:8000/evaluate_omr/", files=files)
            if response.status_code == 200:
                st.success("✅ Evaluation Complete")
                result = response.json()
                
        
                total_score = result["total_score"]
                st.subheader("Total Score")
                st.progress(total_score / 100) 
                
                subject_scores = result["subject_scores"]
                st.subheader("Subject-wise Scores")
                df = pd.DataFrame(list(subject_scores.items()), columns=["Subject", "Score"])
                
        
                fig = px.bar(df, x="Subject", y="Score", color="Score", 
                             color_continuous_scale="Viridis", text="Score",
                             labels={"Score":"Marks"})
                fig.update_layout(yaxis=dict(range=[0,20]), title="Scores per Subject")
                st.plotly_chart(fig, use_container_width=True)
                
                
                st.subheader("Scores Table")
                st.table(df)
                
                st.success("✅ Evaluation complete. No raw JSON displayed.")
                
            else:
                st.error("❌ Error evaluating sheet")
        except Exception as e:
            st.error(f"Server Error: {e}")
