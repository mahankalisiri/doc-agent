import streamlit as st
from scraper import get_page_content  # your scraper.py function
from analyzer import analyze_document  # your analysis function
from reviser import revise_document    # your revision function

st.set_page_config(page_title="Doc Agent", layout="wide")

st.title("📘 AI-Powered Documentation Improvement Agent")
st.markdown("Analyze and enhance documentation using AI-powered analysis and revision.")

url = st.text_input(
    "🔗 Enter the documentation URL to analyze",
    placeholder="https://example.com/docs/article..."
)

def is_valid_url(url: str) -> bool:
    # Basic validation to check if URL starts with http or https
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

        st.success("✅ Analysis complete!")

        st.subheader("🧠 Document Analysis")

        for key in ["readability", "structure", "completeness", "style_guidelines"]:
            section = analysis.get(key, {})
            st.markdown(f"### {key.replace('_', ' ').title()}")
            st.markdown(f"**Score:** `{section.get('score', 'N/A')}`")

            st.markdown("**Issues Found:**")
            if section.get("issues"):
                for issue in section["issues"]:
                    st.write(f"- {issue}")
            else:
                st.write("_No issues found._")

            st.markdown("**Improvement Suggestions:**")
            if section.get("suggestions"):
                for suggestion in section["suggestions"]:
                    st.success(f"✅ {suggestion}")
            else:
                st.write("_No suggestions available._")

        if st.button("🪄 Generate Revised Version"):
            with st.spinner("Applying suggestions..."):
                revised = revise_document(raw_text, analysis)

            st.subheader("📄 Revised Documentation")
            st.text_area("Revised Content", revised, height=500)
            st.download_button("📥 Download Revised Text", revised, file_name="revised.txt")
