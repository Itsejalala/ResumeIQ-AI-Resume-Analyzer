# ResumeIQ | AI Resume Analyzer

ResumeIQ is a Python-based web application that analyzes resumes and
matches candidates with relevant job roles. It extracts skills from
resume content, calculates job-match scores, and highlights missing
skills to help users identify areas for improvement.

**Live Demo:** [Try ResumeIQ](https://resumeiq-ai-resume-analyzer-mts5bd36ror4mcypiz2bz4.streamlit.app/)

## Features

- Resume parsing from PDF and DOCX files
- Automated skill extraction from resume content
- Resume matching against multiple job roles
- Job-match scores and skill comparison
- Identification of missing skills
- Learning recommendations for skill development

## Tech Stack

- **Language:** Python
- **Frontend:** Streamlit
- **Text Processing:** NLP
- **Similarity Matching:** TF-IDF and Sentence Transformers
- **Data Processing:** Pandas, Scikit-learn

## How It Works

1. The user uploads a resume.
2. The application extracts and cleans the text.
3. Relevant skills are identified from the resume.
4. The resume is compared with job requirements.
5. Matching scores, suitable job roles, and missing skills are displayed.

## Project Structure

```text
ResumeIQ/
├── app.py
├── resume_parser.py
├── resume_analyzer.py
├── text_cleaner.py
├── skill_extractor.py
├── job_matcher.py
├── jd_matcher.py
├── job_description_parser.py
├── llm_analyzer.py
├── roadmap_generator.py
├── requirements.txt
└── data/
    ├── job_roles.csv
    ├── skill_dictionary.csv
    └── learning_resources.csv