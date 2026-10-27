import os
import json
import re

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


# ============================================================
# LLM
# ============================================================

def get_llm():

    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv("GROQ_MODEL")

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing from the .env file."
        )

    if not model_name:
        raise ValueError(
            "GROQ_MODEL is missing from the .env file."
        )

    return ChatGroq(
        api_key=api_key,
        model=model_name,
        temperature=0.2
    )


# ============================================================
# SAFE JSON PARSER
# ============================================================

def parse_json_response(content):

    content = content.strip()

    content = content.replace(
        "```json",
        ""
    )

    content = content.replace(
        "```",
        ""
    )

    content = content.strip()

    try:
        return json.loads(content)

    except json.JSONDecodeError:

        match = re.search(
            r"\{.*\}",
            content,
            re.DOTALL
        )

        if match:

            try:

                return json.loads(
                    match.group()
                )

            except json.JSONDecodeError:
                pass

    return {}


# ============================================================
# GENERAL RESUME ANALYSIS
# ============================================================

def analyze_resume_with_llm(
    resume_text,
    job_role,
    missing_skills
):

    llm = get_llm()

    missing_text = ", ".join(
        missing_skills
    )

    prompt = f"""
You are an expert technical career advisor.

TARGET ROLE:
{job_role}

MISSING SKILLS:
{missing_text}

RESUME:
{resume_text}

Analyze ONLY career-related information.

Focus on:

- technical skills
- projects
- education
- experience
- achievements
- resume structure
- relevance to target role

Do not evaluate personal characteristics.

Return exactly:

STRENGTHS:
- point
- point
- point

WEAKNESSES:
- point
- point
- point

IMPROVEMENTS:
- point
- point
- point

PROJECT_SUGGESTION:
One practical project.

CAREER_ADVICE:
A short paragraph.
"""

    response = llm.invoke(
        prompt
    )

    return response.content


# ============================================================
# AI RESUME SCORE
# ============================================================

def calculate_ai_resume_score(
    resume_text,
    target_role,
    resume_skills
):

    llm = get_llm()

    skills_text = ", ".join(
        resume_skills
    )

    prompt = f"""
You are an expert ATS and technical resume evaluator.

TARGET ROLE:
{target_role}

DETECTED SKILLS:
{skills_text}

RESUME:
{resume_text}

Evaluate:

1. ATS compatibility
2. Technical skills
3. Project quality
4. Experience quality
5. Resume structure
6. Target-role relevance

Give each score from 0 to 100.

Then calculate an overall score.

Use only job-related information.

Return ONLY valid JSON:

{{
    "ats_score": 0,
    "skills_score": 0,
    "projects_score": 0,
    "experience_score": 0,
    "structure_score": 0,
    "relevance_score": 0,
    "overall_score": 0,
    "summary": ""
}}
"""

    response = llm.invoke(
        prompt
    )

    result = parse_json_response(
        response.content
    )

    if not result:

        return {
            "ats_score": 0,
            "skills_score": 0,
            "projects_score": 0,
            "experience_score": 0,
            "structure_score": 0,
            "relevance_score": 0,
            "overall_score": 0,
            "summary": "Unable to generate AI score."
        }

    return result


# ============================================================
# RESUME REWRITER
# ============================================================

def improve_resume_section(
    text,
    section,
    target_role
):

    llm = get_llm()

    prompt = f"""
You are an expert technical resume writer.

TARGET ROLE:
{target_role}

SECTION:
{section}

CURRENT CONTENT:
{text}

Rewrite this content to make it:

- ATS-friendly
- concise
- technically specific
- professional
- achievement-oriented
- relevant to the target role

Use strong action verbs.

Include metrics only if they already exist
in the original content.

Never invent:

- technologies
- achievements
- experience
- projects
- numbers
- certifications

Return ONLY the rewritten version.
"""

    response = llm.invoke(
        prompt
    )

    return response.content.strip()


# ============================================================
# JOB DESCRIPTION INTELLIGENCE
# ============================================================

def extract_jd_information(
    job_description
):

    llm = get_llm()

    prompt = f"""
You are an expert technical recruiter.

Analyze this job description:

{job_description}

Extract the following:

- technical skills
- programming languages
- frameworks
- databases
- cloud technologies
- AI/ML technologies
- tools
- experience requirements
- education requirements

Return ONLY valid JSON.

Format:

{{
    "technical_skills": [],
    "programming_languages": [],
    "frameworks": [],
    "databases": [],
    "cloud": [],
    "ai_ml": [],
    "tools": [],
    "experience_requirements": [],
    "education_requirements": []
}}
"""

    response = llm.invoke(
        prompt
    )

    result = parse_json_response(
        response.content
    )

    if not result:

        return {
            "technical_skills": [],
            "programming_languages": [],
            "frameworks": [],
            "databases": [],
            "cloud": [],
            "ai_ml": [],
            "tools": [],
            "experience_requirements": [],
            "education_requirements": []
        }

    return result


# ============================================================
# AI ROADMAP
# ============================================================

def generate_ai_roadmap(
    current_skills,
    missing_skills,
    target_role
):

    llm = get_llm()

    current = ", ".join(
        current_skills
    )

    missing = ", ".join(
        missing_skills
    )

    prompt = f"""
You are an AI career roadmap planner.

TARGET ROLE:
{target_role}

CURRENT SKILLS:
{current}

MISSING SKILLS:
{missing}

Create a realistic 6-week roadmap.

Progress from fundamentals to practical implementation.

For every week provide:

- week
- skill
- topic
- what_to_learn
- practice_task
- mini_project

Return ONLY valid JSON:

{{
    "roadmap": [
        {{
            "week": 1,
            "skill": "",
            "topic": "",
            "what_to_learn": "",
            "practice_task": "",
            "mini_project": ""
        }}
    ]
}}
"""

    response = llm.invoke(
        prompt
    )

    result = parse_json_response(
        response.content
    )

    if not result:

        return {
            "roadmap": []
        }

    return result


# ============================================================
# PROJECT RECOMMENDATIONS
# ============================================================

def recommend_projects(
    current_skills,
    missing_skills,
    target_role
):

    llm = get_llm()

    current = ", ".join(
        current_skills
    )

    missing = ", ".join(
        missing_skills
    )

    prompt = f"""
You are an AI project mentor.

TARGET ROLE:
{target_role}

CURRENT SKILLS:
{current}

MISSING SKILLS:
{missing}

Recommend exactly 3 portfolio projects.

Each project must:

- address skill gaps
- be realistic for a student
- demonstrate practical AI/software engineering
- be GitHub-worthy
- be relevant to the target role

Return ONLY valid JSON:

{{
    "projects": [
        {{
            "title": "",
            "difficulty": "",
            "technologies": [],
            "description": "",
            "skills_gained": []
        }}
    ]
}}
"""

    response = llm.invoke(
        prompt
    )

    result = parse_json_response(
        response.content
    )

    if not result:

        return {
            "projects": []
        }

    return result


# ============================================================
# RESUME VS JD AI ANALYSIS
# ============================================================

def analyze_resume_vs_jd(
    resume_text,
    job_description
):

    llm = get_llm()

    prompt = f"""
You are an expert technical recruiter.

Compare this resume with the job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Analyze:

- strongest matches
- important missing requirements
- relevant experience
- relevant projects
- resume weaknesses for this job
- practical recommendations

Return ONLY valid JSON:

{{
    "strong_matches": [],
    "missing_requirements": [],
    "relevant_experience": [],
    "relevant_projects": [],
    "resume_weaknesses": [],
    "recommendations": []
}}
"""

    response = llm.invoke(
        prompt
    )

    result = parse_json_response(
        response.content
    )

    if not result:

        return {
            "strong_matches": [],
            "missing_requirements": [],
            "relevant_experience": [],
            "relevant_projects": [],
            "resume_weaknesses": [],
            "recommendations": []
        }

    return result