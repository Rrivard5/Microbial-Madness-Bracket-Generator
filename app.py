import streamlit as st
st.write("🧪 App starting...")
from bracket import generate_bracket_image, create_matchups
from microbe_parser import extract_microbe_info
from utils import save_bracket_to_pdf
from io import BytesIO
from PIL import Image
import tempfile

st.set_page_config(page_title="Microbial Madness Bracket", layout="centered")
st.title("🦠 Microbial Madness Bracket Builder")
st.write("Upload student-designed microbe files and auto-generate a visual tournament bracket.")

# File uploader
uploaded_files = st.file_uploader("Upload 10-20 .docx or .rtf student files:", accept_multiple_files=True, type=["docx", "rtf"])

if uploaded_files:
    with st.spinner("Extracting microbe data..."):
        microbes = []
        for uploaded_file in uploaded_files:
            try:
                microbe = extract_microbe_info(uploaded_file)
                if microbe:
                    microbes.append(microbe)
            except Exception as e:
                st.warning(f"Could not process {uploaded_file.name}: {e}")

    if len(microbes) < 2:
        st.warning("Please upload at least two valid microbe files to build a bracket.")
    else:
        st.success(f"Successfully extracted {len(microbes)} microbe entries.")

        matchups = create_matchups(microbes)

        st.subheader("🔢 Bracket Matchups")
        for round_num, round_matches in enumerate(matchups, start=1):
            st.markdown(f"**Round {round_num}**")
            for m1, m2 in round_matches:
                st.write(f"{m1['name']} ({m1['type']}) vs {m2['name']} ({m2['type']})")

        st.subheader("🎨 Bracket Visualization")
        image = generate_bracket_image(matchups)
        st.image(image, caption="Tournament Bracket", use_column_width=True)

        # Download options
        st.subheader("📄 Download PDF")
        pdf_bytes = save_bracket_to_pdf(image)
        st.download_button(
            label="Download Bracket as PDF",
            data=pdf_bytes,
            file_name="microbial_madness_bracket.pdf",
            mime="application/pdf"
        )
