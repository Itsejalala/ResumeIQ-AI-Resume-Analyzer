import re
import pandas as pd


def load_skill_dictionary():

    skills = pd.read_csv("data/skill_dictionary.csv")

    return skills


def extract_skills(text):

    skills_df = load_skill_dictionary()

    found_skills = []

    text = text.lower()


    # Skill aliases
    aliases = {
        "sklearn": "Scikit-learn",
        "scikit learn": "Scikit-learn",
        "scikit learn library": "Scikit-learn",
        "huggingface": "Hugging Face",
        "hugging-face": "Hugging Face",
        "js": "JavaScript",
        "nodejs": "Node.js",
        "reactjs": "React",
        "postgres": "PostgreSQL"
    }


    # Check aliases first
    for alias, actual_skill in aliases.items():

        pattern = r"\b" + re.escape(alias) + r"\b"

        if re.search(pattern, text):

            if actual_skill not in found_skills:

                found_skills.append(actual_skill)


    # Check skills from dictionary
    for skill in skills_df["skill"]:

        skill_lower = skill.lower()

        pattern = r"(?<!\w)" + re.escape(skill_lower) + r"(?!\w)"

        if re.search(pattern, text):

            if skill not in found_skills:

                found_skills.append(skill)


    return found_skills


def find_missing_skills(resume_skills, required_skills):

    resume_skills_lower = []

    for skill in resume_skills:

        resume_skills_lower.append(
            skill.lower()
        )


    missing_skills = []


    for skill in required_skills:

        if skill.lower() not in resume_skills_lower:

            missing_skills.append(skill)


    return missing_skills