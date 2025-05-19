
import pandas as pd
import fitz  # PyMuPDF
import docx
import io

def score_responses(responses):
    total_score = sum(responses.values())
    return {"total_score": total_score, "responses": responses}

def generate_use_case_report(scores, uploaded_data):
    base_cases = [
        {"Title": "Contract Analytics", "Description": "AI to analyze contract terms and flag risks", "Score": 85},
        {"Title": "Spend Categorization", "Description": "Automated mapping of spend data to categories", "Score": 90},
        {"Title": "Policy Compliance Monitoring", "Description": "AI to flag non-compliance in procurement actions", "Score": 80}
    ]
    df = pd.DataFrame(base_cases)
    df["Adjusted Score"] = df["Score"] + scores["total_score"] * 0.5
    return df.sort_values("Adjusted Score", ascending=False)

def analyze_uploaded_files(files):
    content = ""
    for file in files:
        if file.name.endswith(".pdf"):
            content += extract_text_from_pdf(file)
        elif file.name.endswith(".docx"):
            content += extract_text_from_docx(file)
        elif file.name.endswith(".txt"):
            content += str(file.read(), 'utf-8')
        elif file.name.endswith((".csv", ".xlsx")):
            try:
                df = pd.read_csv(file) if file.name.endswith(".csv") else pd.read_excel(file)
                content += df.to_string()
            except Exception:
                pass
    return content

def extract_text_from_pdf(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(file):
    doc = docx.Document(io.BytesIO(file.read()))
    return "\n".join([para.text for para in doc.paragraphs])
