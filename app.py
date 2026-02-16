import streamlit as st
from docx import Document
from datetime import datetime
import os

TEMPLATE_FILE = "offer_template.docx"

def format_currency(num):
    return "{:,.0f}".format(num)

def replace_text_in_doc(doc, replacements):
    for paragraph in doc.paragraphs:
        for key, value in replacements.items():
            if key in paragraph.text:
                paragraph.text = paragraph.text.replace(key, value)

    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for key, value in replacements.items():
                    if key in cell.text:
                        cell.text = cell.text.replace(key, value)

st.title("Offer Letter Generator")

name = st.text_input("Candidate Name")
job_title = st.text_input("Job Title")
joining_deadline_date = st.date_input("Joining Deadline")
total_ctc = st.number_input("Total CTC", min_value=0)
performance_percent = st.number_input("Performance %", min_value=0.0)
probation = st.text_input("Probation Period", value="6 months")
notice = st.text_input("Notice Period", value="3 months")

if st.button("Generate Offer Letter"):

    performance_amount = total_ctc * performance_percent / 100
    fixed_ctc = total_ctc - performance_amount

    today = datetime.today().strftime("%d %B %Y")
    joining_deadline = joining_deadline_date.strftime("%d %B %Y")

    replacements = {
        "{{date}}": today,
        "{{name}}": name,
        "{{job_title}}": job_title,
        "{{joining_deadline}}": joining_deadline,
        "{{total_ctc}}": format_currency(total_ctc),
        "{{fixed_ctc}}": format_currency(fixed_ctc),
        "{{performance_percent}}": str(performance_percent),
        "{{performance_amount}}": format_currency(performance_amount),
        "{{probation}}": probation,
        "{{notice_period}}": notice,
    }

    doc = Document(TEMPLATE_FILE)
    replace_text_in_doc(doc, replacements)

    output_docx = f"./Offer_Letter_{name}-windmark.docx"
    doc.save(output_docx)

    st.success("Offer Letter Generated Successfully")

    with open(output_docx, "rb") as file:
        st.download_button("Download Word", file, file_name=os.path.basename(output_docx))