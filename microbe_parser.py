import docx2txt
import re
from striprtf.striprtf import rtf_to_text
import streamlit as st  # to log what's working

def extract_microbe_info(file):
    filename = file.name.lower()
    content = ""

    # Read the file content
    if filename.endswith(".docx"):
        content = docx2txt.process(file)
    elif filename.endswith(".rtf"):
        raw_text = file.read().decode(errors="ignore")
        content = rtf_to_text(raw_text)
    else:
        st.warning(f"Unsupported file format: {file.name}")
        return None

    # Debug: show some of the file content
    st.write(f"📄 File content for {file.name} (first 300 chars):")
    st.text(content[:300])

    # Attempt to extract fields
    microbe_name = extract_field(content, "Microbe Name")
    microbe_type = extract_field(content, "Microbe Type")
    student_name = extract_field(content, "Student Name") or file.name.replace(".docx", "").replace(".rtf", "")

    if microbe_name and microbe_type:
        return {
            "name": microbe_name.strip(),
            "type": microbe_type.strip().lower(),
            "student": student_name.strip(),
        }

    st.warning(f"⚠️ Missing fields in file: {file.name}")
    return None

def extract_field(text, field):
    pattern = rf"{field}[:\s]+(.+?)(\r|\n|$)"
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else None
