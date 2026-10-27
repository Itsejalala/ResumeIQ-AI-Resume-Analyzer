import os
import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Try loading the semantic AI model.
# If it fails, the matcher will use TF-IDF instead.
try:
    from sentence_transformers import SentenceTransformer

    embedding_model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )

except Exception:
    embedding_model = None


# ============================================================
# LOAD JOB ROLES
# ============================================================

def load_job_roles():

    csv_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "data",
        "job_roles.csv"
    )

    if not os.path.exists(csv_path):
        raise FileNotFoundError(
            f"Job roles file not found: {csv_path}"
        )

    df = pd.read_csv(csv_path)

    required_columns = {
        "job_role",
        "required_skills",
        "description"
    }

    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(
            "job_roles.csv must contain the columns: "
            "job_role, required_skills, description. "
            f"Missing: {', '.join(sorted(missing_columns))}"
        )

    return df.fillna("")


# ============================================================
# NORMALIZE TEXT
# ============================================================

def normalize_text(text):

    if text is None:
        return ""

    return re.sub(
        r"\s+",
        " ",
        str(text)
    ).strip().lower()


# ============================================================
# CONVERT SKILLS TO A LIST
# ============================================================

def split_skills(skills):

    if isinstance(skills, (list, tuple, set)):

        return [
            str(skill).strip()
            for skill in skills
            if str(skill).strip()
        ]

    if not str(skills or "").strip():
        return []

    return [
        skill.strip()
        for skill in re.split(r"[,;|]", str(skills))
        if skill.strip()
    ]


# ============================================================
# GET REQUIRED SKILLS FOR A JOB ROLE
# ============================================================

def get_required_skills(job_role):

    df = load_job_roles()

    target_role = normalize_text(job_role)

    matching_role = df[
        df["job_role"].apply(normalize_text) == target_role
    ]

    if matching_role.empty:
        return []

    skills = matching_role.iloc[0]["required_skills"]

    return split_skills(skills)


# ============================================================
# CALCULATE TEXT SIMILARITY
# ============================================================

def calculate_similarity(text1, text2):

    text1 = str(text1 or "").strip()
    text2 = str(text2 or "").strip()

    if not text1 or not text2:
        return 0.0, "none"

    # --------------------------------------------------------
    # Semantic similarity using Sentence Transformers
    # --------------------------------------------------------

    if embedding_model is not None:

        try:

            embeddings = embedding_model.encode(
                [text1, text2]
            )

            similarity = cosine_similarity(
                [embeddings[0]],
                [embeddings[1]]
            )[0][0]

            similarity = max(
                0.0,
                min(1.0, float(similarity))
            )

            return similarity, "sentence-transformers"

        except Exception:
            pass

    # --------------------------------------------------------
    # TF-IDF fallback
    # --------------------------------------------------------

    try:

        vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english"
        )

        vectors = vectorizer.fit_transform(
            [text1, text2]
        )

        similarity = cosine_similarity(
            vectors[0],
            vectors[1]
        )[0][0]

        similarity = max(
            0.0,
            min(1.0, float(similarity))
        )

        return similarity, "tf-idf-fallback"

    except ValueError:

        return 0.0, "tf-idf-fallback"


# ============================================================
# CALCULATE MATCH SCORES FOR ALL JOB ROLES
# ============================================================

def calculate_match_scores(cleaned_text, resume_skills):

    # Load the expanded job-role database.
    job_roles = load_job_roles()

    resume_text = str(cleaned_text or "")

    # Normalize the extracted resume skills.
    resume_skills = split_skills(resume_skills)

    resume_skills_lookup = {
        normalize_text(skill)
        for skill in resume_skills
    }

    results = []

    # Process every job role.
    for _, row in job_roles.iterrows():

        job_role = str(row["job_role"]).strip()

        job_description = str(
            row["description"]
        ).strip()

        required_skills = split_skills(
            row["required_skills"]
        )

        # ----------------------------------------------------
        # SKILL MATCHING
        # ----------------------------------------------------

        matched_skills = [
            skill
            for skill in required_skills
            if normalize_text(skill) in resume_skills_lookup
        ]

        missing_skills = [
            skill
            for skill in required_skills
            if normalize_text(skill) not in resume_skills_lookup
        ]

        if required_skills:

            skill_score = (
                len(matched_skills)
                / len(required_skills)
            ) * 100

        else:

            skill_score = 0.0

        # ----------------------------------------------------
        # PREPARE ROLE TEXT
        # ----------------------------------------------------

        role_text = (
            f"{job_role}. "
            f"{job_description}. "
            f"Required skills: "
            f"{', '.join(required_skills)}"
        )

        # ----------------------------------------------------
        # SEMANTIC SIMILARITY
        # ----------------------------------------------------

        semantic_similarity, matching_method = (
            calculate_similarity(
                resume_text,
                role_text
            )
        )

        semantic_score = semantic_similarity * 100

        # ----------------------------------------------------
        # TF-IDF SIMILARITY
        # ----------------------------------------------------

        tfidf_similarity, _ = calculate_similarity(
            resume_text,
            role_text
        )

        tfidf_score = tfidf_similarity * 100

        # ----------------------------------------------------
        # FINAL MATCH SCORE
        # ----------------------------------------------------

        final_score = (
            (skill_score * 0.50)
            +
            (semantic_score * 0.35)
            +
            (tfidf_score * 0.15)
        )

        final_score = max(
            0.0,
            min(100.0, final_score)
        )

        # ----------------------------------------------------
        # SAVE RESULTS
        # ----------------------------------------------------

        results.append({

            "job_role": job_role,

            "match_score": round(
                final_score,
                2
            ),

            "skill_match_score": round(
                skill_score,
                2
            ),

            "semantic_score": round(
                semantic_score,
                2
            ),

            "tfidf_score": round(
                tfidf_score,
                2
            ),

            "matched_skills": matched_skills,

            "missing_skills": missing_skills,

            "required_skills": required_skills,

            "description": job_description,

            "matching_method": matching_method

        })

    # --------------------------------------------------------
    # SORT RESULTS BY MATCH SCORE
    # --------------------------------------------------------

    results_df = pd.DataFrame(results)

    if results_df.empty:
        return results_df

    results_df = results_df.sort_values(
        by="match_score",
        ascending=False
    ).reset_index(drop=True)

    return results_df