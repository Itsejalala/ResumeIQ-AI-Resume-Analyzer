import re


def analyze_resume(resume_text):

    text = resume_text.lower()


    sections = {
        "Education": [
            "education",
            "academic",
            "degree",
            "university",
            "college"
        ],

        "Experience": [
            "experience",
            "work experience",
            "internship",
            "employment"
        ],

        "Skills": [
            "skills",
            "technical skills",
            "technologies"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Certifications": [
            "certification",
            "certifications",
            "certificate"
        ],

        "GitHub": [
            "github.com",
            "github"
        ],

        "LinkedIn": [
            "linkedin.com",
            "linkedin"
        ]
    }


    results = {}


    for section, keywords in sections.items():

        found = False


        for keyword in keywords:

            pattern = r"\b" + re.escape(keyword) + r"\b"

            if re.search(pattern, text):

                found = True
                break


        results[section] = found


    # Calculate completeness
    total_sections = len(results)

    completed_sections = sum(results.values())


    completeness_score = (
        completed_sections / total_sections
    ) * 100


    return results, completeness_score