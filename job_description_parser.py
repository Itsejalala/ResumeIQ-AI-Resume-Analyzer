from resume_parser import extract_from_pdf, extract_from_docx


def extract_job_description(file):

    if file.name.endswith(".pdf"):

        text = extract_from_pdf(file)

    elif file.name.endswith(".docx"):

        text = extract_from_docx(file)

    else:

        text = ""

    return text