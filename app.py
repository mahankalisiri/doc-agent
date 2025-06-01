import os
import time
import streamlit as st
from scraper import get_page_content
from analyzer import analyze_document
from reviser import revise_document


os.makedirs("output", exist_ok=True)

st.set_page_config(page_title="Doc Agent", layout="wide")

st.title("📘 AI-Powered Documentation Improvement Agent")
st.markdown("Analyze and enhance documentation using AI-powered analysis and revision.")

url = st.text_input(
    "🔗 Enter the documentation URL to analyze",
    placeholder="https://example.com/docs/article..."
)

def is_valid_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://")

if url:
    if not is_valid_url(url):
        st.error("❌ Please enter a valid URL starting with http:// or https://")
    else:
        with st.spinner("Scraping and analyzing content..."):
            try:
                raw_text = get_page_content(url)
                analysis = analyze_document(raw_text)
            except Exception as e:
                st.error(f"❌ Failed to fetch or analyze the URL: {e}")
                st.stop()

        st.success(" Analysis complete!")

        st.subheader("Document Analysis")


        timestamp = time.strftime("%Y%m%d_%H%M%S")
        analysis_filename = f"output/analysis_{timestamp}.txt"
        revised_filename = f"output/revised_{timestamp}.txt"

 
        full_analysis = []
        for key in ["readability", "structure", "completeness", "style_guidelines"]:
            section = analysis.get(key, {})
            full_analysis.append(f"### {key.replace('_', ' ').title()}")
            full_analysis.append(f"Score: {section.get('score', 'N/A')}\n")

            full_analysis.append("Issues Found:")
            if section.get("issues"):
                for issue in section["issues"]:
                    full_analysis.append(f"- {issue}")
            else:
                full_analysis.append("No issues found.")

            full_analysis.append("Improvement Suggestions:")
            if section.get("suggestions"):
                for suggestion in section["suggestions"]:
                    full_analysis.append(f" {suggestion}")
            else:
                full_analysis.append("No suggestions available.")
            full_analysis.append("\n")

        full_analysis_str = "\n".join(full_analysis)


        with open(analysis_filename, "w", encoding="utf-8") as f:
            f.write(full_analysis_str)

        st.info(f"Analysis saved to `{analysis_filename}`")

  
        st.text_area(" Full Analysis", full_analysis_str, height=400)

        if st.button("Generate Revised Version"):
            with st.spinner("Applying suggestions..."):
                revised = revise_document(raw_text, analysis)

            # Save revised doc to file
            with open(revised_filename, "w", encoding="utf-8") as f:
                f.write(revised)

            st.subheader(" Revised Documentation")
            st.text_area("Revised Content", revised, height=500)
            st.download_button(" Download Revised Text", revised, file_name=os.path.basename(revised_filename))
            st.success(f" Revised version saved to `{revised_filename}`")
