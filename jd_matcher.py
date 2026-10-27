from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from sentence_transformers import SentenceTransformer

from skill_extractor import extract_skills


# Load AI embedding model
embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def calculate_jd_match(
    resume_text,
    job_description
):

    # ========================================================
    # SKILLS
    # ========================================================

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )


    # ========================================================
    # TF-IDF
    # ========================================================

    documents = [
        resume_text,
        job_description
    ]


    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        documents
    )


    tfidf_similarity = cosine_similarity(
        vectors[0],
        vectors[1]
    )[0][0]


    tfidf_score = (
        tfidf_similarity * 100
    )


    # ========================================================
    # AI SEMANTIC SIMILARITY
    # ========================================================

    embeddings = embedding_model.encode(
        [
            resume_text,
            job_description
        ]
    )


    semantic_similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]


    semantic_score = (
        semantic_similarity * 100
    )


    # ========================================================
    # SKILL MATCH
    # ========================================================

    resume_skills_lower = [
        skill.lower()
        for skill in resume_skills
    ]


    matched_skills = []

    missing_skills = []


    for skill in job_skills:

        if skill.lower() in resume_skills_lower:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )


    if len(job_skills) > 0:

        skill_score = (
            len(matched_skills)
            /
            len(job_skills)
        ) * 100

    else:

        skill_score = 0


    # ========================================================
    # FINAL SCORE
    # ========================================================

    final_score = (

        (skill_score * 0.50)

        +

        (semantic_score * 0.35)

        +

        (tfidf_score * 0.15)

    )


    return {

        "tfidf_score": tfidf_score,

        "semantic_score": semantic_score,

        "skill_score": skill_score,

        "match_score": final_score,

        "resume_skills": resume_skills,

        "job_skills": job_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills

    }