import io

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet


from resume_parser import (
    extract_from_pdf,
    extract_from_docx
)

from text_cleaner import clean_text

from skill_extractor import (
    extract_skills,
    find_missing_skills
)

from job_matcher import (
    calculate_match_scores,
    get_required_skills
)

from resume_analyzer import (
    analyze_resume
)

from jd_matcher import (
    calculate_jd_match
)

from roadmap_generator import (
    generate_roadmap
)

from llm_analyzer import (
    analyze_resume_with_llm,
    calculate_ai_resume_score,
    improve_resume_section,
    extract_jd_information,
    generate_ai_roadmap,
    recommend_projects,
    analyze_resume_vs_jd
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeIQ",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CSS
# ============================================================

st.html("""
<style>

@import url(
'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);

* {
    font-family: 'Inter', sans-serif;
}

.stApp {

    background:
        radial-gradient(
            circle at 5% 0%,
            rgba(99,102,241,.15),
            transparent 27%
        ),
        radial-gradient(
            circle at 95% 5%,
            rgba(168,85,247,.12),
            transparent 28%
        ),
        #070910;

    color:#f8fafc;
}

.block-container {

    max-width:1450px;

    padding-top:1.8rem;

    padding-bottom:5rem;
}


/* SIDEBAR */

section[data-testid="stSidebar"] {

    background:
        linear-gradient(
            180deg,
            #0a0d17,
            #070910
        );

    border-right:
        1px solid rgba(255,255,255,.07);
}

section[data-testid="stSidebar"] * {
    color:#dbe4f0;
}


/* HERO */

.hero-wrapper {

    position:relative;

    min-height:390px;

    border-radius:31px;

    overflow:hidden;

    margin-bottom:30px;

    background:
        linear-gradient(
            135deg,
            #101522,
            #15132a 52%,
            #0d111c
        );

    border:
        1px solid rgba(255,255,255,.08);

    box-shadow:
        0 35px 100px rgba(0,0,0,.30);
}

.hero-grid {

    position:absolute;

    inset:0;

    background-image:

        linear-gradient(
            rgba(255,255,255,.032) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,.032) 1px,
            transparent 1px
        );

    background-size:44px 44px;

    mask-image:
        linear-gradient(
            to bottom,
            black,
            transparent
        );
}

.hero-glow {

    position:absolute;

    width:620px;

    height:620px;

    right:-160px;

    top:-270px;

    border-radius:50%;

    background:
        radial-gradient(
            circle,
            rgba(124,58,237,.33),
            rgba(124,58,237,.08) 42%,
            transparent 70%
        );

    animation:
        heroGlow 7s ease-in-out infinite;
}

.hero-content {

    position:relative;

    z-index:5;

    padding:70px 66px;

    max-width:850px;
}

.hero-badge {

    display:inline-flex;

    padding:9px 16px;

    border-radius:50px;

    background:
        rgba(139,92,246,.13);

    border:
        1px solid rgba(167,139,250,.28);

    color:#d8ccff;

    font-size:11px;

    font-weight:750;

    letter-spacing:1.1px;
}

.hero-title {

    margin:22px 0 0 0;

    font-size:clamp(56px,7vw,88px);

    line-height:.95;

    font-weight:800;

    letter-spacing:-4px;

    background:
        linear-gradient(
            100deg,
            #ffffff,
            #d4c5ff 42%,
            #f4b5d5 72%,
            #ffffff
        );

    background-size:250% auto;

    -webkit-background-clip:text;

    -webkit-text-fill-color:transparent;

    animation:
        gradientShift 7s linear infinite;
}

.hero-description {

    margin-top:25px;

    color:#c2ccda;

    font-size:16px;

    line-height:1.75;

    max-width:730px;
}

.hero-mini-row {

    display:flex;

    gap:9px;

    margin-top:27px;

    flex-wrap:wrap;
}

.hero-mini {

    padding:8px 13px;

    border-radius:10px;

    background:
        rgba(255,255,255,.05);

    border:
        1px solid rgba(255,255,255,.075);

    color:#d5deeb;

    font-size:11px;

    font-weight:600;
}

@keyframes gradientShift {

    0% {
        background-position:0% center;
    }

    50% {
        background-position:100% center;
    }

    100% {
        background-position:0% center;
    }
}

@keyframes heroGlow {

    0%,100% {
        transform:scale(1);
        opacity:.72;
    }

    50% {
        transform:scale(1.12);
        opacity:1;
    }
}


/* CARDS */

.dashboard-card {

    background:
        linear-gradient(
            145deg,
            rgba(19,25,40,.88),
            rgba(11,16,28,.75)
        );

    border:
        1px solid rgba(255,255,255,.07);

    border-radius:19px;

    padding:21px 22px;

    min-height:112px;

    box-shadow:
        0 14px 45px rgba(0,0,0,.17);
}

.dashboard-label {

    color:#8f9caf;

    font-size:10px;

    font-weight:800;

    letter-spacing:1.05px;
}

.dashboard-value {

    margin-top:9px;

    color:#ffffff;

    font-size:29px;

    font-weight:800;
}

.dashboard-small {

    margin-top:6px;

    color:#9aa7b8;

    font-size:11px;

    line-height:1.5;
}


/* SECTION */

.section-title {

    color:#ffffff;

    font-size:26px;

    font-weight:800;

    margin-top:37px;

    margin-bottom:6px;
}

.section-subtitle {

    color:#9da9b9;

    font-size:13px;

    line-height:1.65;

    margin-bottom:20px;
}


/* SCORE */

.ai-score-wrapper {

    padding:28px;

    margin-top:20px;

    border-radius:22px;

    background:
        linear-gradient(
            145deg,
            rgba(20,26,43,.92),
            rgba(10,15,27,.82)
        );

    border:
        1px solid rgba(139,92,246,.18);
}

.score-row {

    margin-top:17px;
}

.score-label-row {

    display:flex;

    justify-content:space-between;

    color:#cbd5e1;

    font-size:12px;

    font-weight:600;

    margin-bottom:7px;
}

.score-track {

    height:7px;

    background:
        rgba(255,255,255,.07);

    border-radius:20px;

    overflow:hidden;
}

.score-fill {

    height:100%;

    border-radius:20px;

    background:
        linear-gradient(
            90deg,
            #6366f1,
            #a855f7
        );
}


/* SKILLS */

.skill-chip {

    display:inline-flex;

    padding:8px 13px;

    margin:4px;

    border-radius:50px;

    background:
        rgba(99,102,241,.13);

    border:
        1px solid rgba(129,140,248,.25);

    color:#d7d9ff;

    font-size:12px;

    font-weight:650;
}

.missing-chip {

    display:inline-flex;

    padding:8px 13px;

    margin:4px;

    border-radius:50px;

    background:
        rgba(244,63,94,.08);

    border:
        1px solid rgba(244,63,94,.22);

    color:#ffb0bc;

    font-size:12px;

    font-weight:650;
}


/* PROJECT CARD */

.project-card {

    padding:23px;

    margin-bottom:14px;

    border-radius:19px;

    background:
        linear-gradient(
            145deg,
            rgba(20,26,43,.90),
            rgba(10,15,27,.80)
        );

    border:
        1px solid rgba(255,255,255,.07);
}

.project-title {

    color:#ffffff;

    font-size:18px;

    font-weight:750;
}

.project-description {

    color:#aeb9c8;

    font-size:13px;

    line-height:1.75;

    margin-top:9px;
}


/* COMPARISON */

.compare-card {

    padding:22px;

    border-radius:18px;

    background:
        rgba(15,23,42,.58);

    border:
        1px solid rgba(255,255,255,.07);

    min-height:220px;
}


/* BUTTON */

.stButton > button {

    min-height:43px;

    border-radius:12px;

    background:
        linear-gradient(
            135deg,
            #6366f1,
            #8b5cf6
        );

    border:
        1px solid rgba(139,92,246,.32);

    color:#ffffff !important;

    font-weight:700;
}

p {
    color:#c7d1df;
}

label {
    color:#d4dce8 !important;
}


/* USER-FRIENDLY FILE UPLOAD */
[data-testid="stFileUploaderDropzone"] {
    background: linear-gradient(
        135deg,
        rgba(99,102,241,0.16),
        rgba(139,92,246,0.10)
    ) !important;
    border: 1px dashed rgba(167,139,250,0.70) !important;
    border-radius: 15px !important;
    transition: all 0.25s ease;
}
[data-testid="stFileUploaderDropzone"]:hover {
    background: linear-gradient(
        135deg,
        rgba(99,102,241,0.25),
        rgba(139,92,246,0.18)
    ) !important;
    border-color: #c4b5fd !important;
}
[data-testid="stFileUploaderDropzone"] * {
    color: #e2e8f0 !important;
}
[data-testid="stFileUploaderDropzone"] button {
    background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
    color: #ffffff !important;
    border: 1px solid rgba(196,181,253,0.45) !important;
    border-radius: 9px !important;
    font-weight: 700 !important;
}
[data-testid="stFileUploaderDropzone"] button:hover {
    background: linear-gradient(135deg, #7c7ff7, #a78bfa) !important;
    border-color: #c4b5fd !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] {
    color: #cbd5e1 !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span {
    color: #c4b5fd !important;
}

</style>
""")


# ============================================================
# HERO
# ============================================================

st.html("""
<div class="hero-wrapper">

    <div class="hero-grid"></div>

    <div class="hero-glow"></div>

    <div class="hero-content">

        <div class="hero-badge">
            ✦ YOUR CAREER, MADE CLEARER
        </div>

        <h1 class="hero-title">
            ResumeIQ
        </h1>

        <div class="hero-description">

            Make your next career move with confidence. Discover jobs that fit your skills,
            improve your resume, identify what to learn next, and get a personalized
            plan to help you reach your goals.

        </div>

        <div class="hero-mini-row">

            <div class="hero-mini">◈ Resume Insights</div>

            <div class="hero-mini">
                ◈ Career Matches
            </div>

            <div class="hero-mini">
                ◈ Skill Insights
            </div>

            <div class="hero-mini">
                ◈ Personalised Guidance
            </div>

        </div>

    </div>

</div>
""")


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "## ResumeIQ ✦"
    )

    st.caption(
        "Your Personal Career Assistant"
    )

    st.markdown(
        "### Upload Resume"
    )

    uploaded_resume = st.file_uploader(

        "Choose a PDF or Word document",

        type=[
            "pdf",
            "docx"
        ],

        key="resume_uploader"
    )

    st.divider()

    st.html("""
    <style>
    .pipeline-container {
        margin-top: 14px;
    }
    .pipeline-step {
        display: flex;
        align-items: flex-start;
        gap: 11px;
        padding: 12px 10px;
        margin-bottom: 8px;
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 13px;
        background: linear-gradient(
            135deg,
            rgba(99,102,241,0.12),
            rgba(139,92,246,0.04)
        );
        transition: all 0.25s ease;
    }
    .pipeline-step:hover {
        border-color: rgba(167,139,250,0.48);
        background: rgba(99,102,241,0.16);
        transform: translateX(3px);
    }
    .pipeline-icon {
        flex: 0 0 32px;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 10px;
        background: rgba(139,92,246,0.18);
        border: 1px solid rgba(167,139,250,0.22);
        font-size: 15px;
    }
    .pipeline-title {
        color: #f1f5f9;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 4px;
    }
    .pipeline-description {
        color: #aab6c8;
        font-size: 10px;
        line-height: 1.5;
    }
    .pipeline-heading {
        color: #a78bfa;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.4px;
        margin: 4px 0 13px;
    }
    </style>

    <div class="pipeline-container">
        <div class="pipeline-heading">YOUR CAREER JOURNEY</div>

        <div class="pipeline-step">
            <div class="pipeline-icon">📄</div>
            <div>
                <div class="pipeline-title">Read Your Resume</div>
                <div class="pipeline-description">Understand your education, projects and experience.</div>
            </div>
        </div>

        <div class="pipeline-step">
            <div class="pipeline-icon">✨</div>
            <div>
                <div class="pipeline-title">Understand Your Skills</div>
                <div class="pipeline-description">Discover the skills and tools in your resume.</div>
            </div>
        </div>

        <div class="pipeline-step">
            <div class="pipeline-icon">🎯</div>
            <div>
                <div class="pipeline-title">Find Career Matches</div>
                <div class="pipeline-description">Explore roles that fit your current profile.</div>
            </div>
        </div>

        <div class="pipeline-step">
            <div class="pipeline-icon">💡</div>
            <div>
                <div class="pipeline-title">Find Skills to Improve</div>
                <div class="pipeline-description">See what you could learn for your target role.</div>
            </div>
        </div>

        <div class="pipeline-step">
            <div class="pipeline-icon">🤖</div>
            <div>
                <div class="pipeline-title">Get Personal Advice</div>
                <div class="pipeline-description">Get suggestions based on your resume.</div>
            </div>
        </div>

        <div class="pipeline-step">
            <div class="pipeline-icon">🗺️</div>
            <div>
                <div class="pipeline-title">Build Your Learning Plan</div>
                <div class="pipeline-description">Follow clear steps to build new skills.</div>
            </div>
        </div>

        <div class="pipeline-step">
            <div class="pipeline-icon">🔎</div>
            <div>
                <div class="pipeline-title">Check a Job</div>
                <div class="pipeline-description">Compare your resume with a job posting.</div>
            </div>
        </div>

        <div class="pipeline-step">
            <div class="pipeline-icon">🚀</div>
            <div>
                <div class="pipeline-title">Grow Your Portfolio</div>
                <div class="pipeline-description">Find project ideas to show your skills.</div>
            </div>
        </div>
    </div>
    """)

    st.divider()

    st.caption(
        "Career guidance only — not a hiring decision."
    )


# ============================================================
# EMPTY STATE
# ============================================================

if uploaded_resume is None:

    st.info(
        "Upload your resume to start ResumeIQ."
    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.html("""
        <div class="dashboard-card">

            <div class="dashboard-label">
                ANALYZE
            </div>

            <div class="dashboard-value"
                 style="font-size:20px;">
                Resume Intelligence
            </div>

            <div class="dashboard-small">
                Extract technical skills,
                projects and experience.
            </div>

        </div>
        """)

    with c2:

        st.html("""
        <div class="dashboard-card">

            <div class="dashboard-label">
                DISCOVER
            </div>

            <div class="dashboard-value"
                 style="font-size:20px;">
                Career Paths
            </div>

            <div class="dashboard-small">
                Find roles that match
                your current profile.
            </div>

        </div>
        """)

    with c3:

        st.html("""
        <div class="dashboard-card">

            <div class="dashboard-label">
                BUILD
            </div>

            <div class="dashboard-value"
                 style="font-size:20px;">
                Career Roadmap
            </div>

            <div class="dashboard-small">
                Convert skill gaps into
                actionable learning.
            </div>

        </div>
        """)

    st.stop()


# ============================================================
# RESUME EXTRACTION
# ============================================================

try:

    if uploaded_resume.name.lower().endswith(".pdf"):

        raw_text = extract_from_pdf(
            uploaded_resume
        )

    else:

        raw_text = extract_from_docx(
            uploaded_resume
        )

except Exception as e:

    st.error(
        f"Resume extraction failed: {e}"
    )

    st.stop()


if not raw_text.strip():

    st.error(
        "No readable text was found."
    )

    st.stop()


# ============================================================
# NLP
# ============================================================

cleaned_text = clean_text(
    raw_text
)

resume_skills = extract_skills(
    cleaned_text
)

section_results, completeness_score = analyze_resume(
    cleaned_text
)


# ============================================================
# CAREER MATCH
# ============================================================

with st.spinner(
    "Running ResumeIQ analysis..."
):

    results = calculate_match_scores(
        cleaned_text,
        resume_skills
    )


if results.empty:

    st.error(
        "No career roles found."
    )

    st.stop()


best_role = results.iloc[0]

best_role_name = best_role["job_role"]


# ============================================================
# SESSION STATE
# ============================================================

if (
    "ai_score" not in st.session_state
):

    with st.spinner(
        "Generating AI resume score..."
    ):

        try:

            st.session_state.ai_score = (
                calculate_ai_resume_score(
                    cleaned_text,
                    best_role_name,
                    resume_skills
                )
            )

        except Exception as e:

            st.session_state.ai_score = {

                "ats_score": 0,
                "skills_score": 0,
                "projects_score": 0,
                "experience_score": 0,
                "structure_score": 0,
                "relevance_score": 0,
                "overall_score": 0,

                "summary":
                    f"AI score unavailable: {e}"
            }


ai_score = st.session_state.ai_score


# ============================================================
# KPI
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.html(f"""
    <div class="dashboard-card">

        <div class="dashboard-label">
            BEST CAREER
        </div>

        <div class="dashboard-value"
             style="font-size:20px;">
            {best_role_name}
        </div>

        <div class="dashboard-small">
            Strongest current match
        </div>

    </div>
    """)


with c2:

    st.html(f"""
    <div class="dashboard-card">

        <div class="dashboard-label">
            AI MATCH
        </div>

        <div class="dashboard-value">
            {best_role["match_score"]:.1f}%
        </div>

        <div class="dashboard-small">
            Skill + semantic compatibility
        </div>

    </div>
    """)


with c3:

    st.html(f"""
    <div class="dashboard-card">

        <div class="dashboard-label">
            AI RESUME SCORE
        </div>

        <div class="dashboard-value">
            {ai_score["overall_score"]}/100
        </div>

        <div class="dashboard-small">
            LLM resume evaluation
        </div>

    </div>
    """)


with c4:

    st.html(f"""
    <div class="dashboard-card">

        <div class="dashboard-label">
            SKILLS DETECTED
        </div>

        <div class="dashboard-value">
            {len(resume_skills)}
        </div>

        <div class="dashboard-small">
            Technologies identified
        </div>

    </div>
    """)


# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Overview",
        "Career Match",
        "AI Roadmap",
        "Job Description",
        "Portfolio"
    ]
)


# ============================================================
# OVERVIEW
# ============================================================

with tab1:

    st.html("""
    <div class="section-title">
        Resume Intelligence
    </div>

    <div class="section-subtitle">
        A complete AI-powered view of your resume quality,
        career compatibility and technical profile.
    </div>
    """)


    # ========================================================
    # AI SCORE
    # ========================================================

    st.html(f"""
    <div class="ai-score-wrapper">

        <div style="
            color:#ffffff;
            font-size:21px;
            font-weight:800;
        ">
            ✦ AI Resume Intelligence
        </div>

        <div style="
            color:#8e9bad;
            font-size:12px;
            margin-top:5px;
        ">
            Evaluated for {best_role_name}
        </div>

        <div style="
            margin-top:22px;
            font-size:58px;
            font-weight:800;
            color:#ffffff;
        ">
            {ai_score["overall_score"]}
            <span style="
                font-size:18px;
                color:#8793a5;
            ">
                /100
            </span>
        </div>

        <div class="score-row">
            <div class="score-label-row">
                <span>ATS Compatibility</span>
                <span>{ai_score["ats_score"]}/100</span>
            </div>

            <div class="score-track">
                <div class="score-fill"
                     style="width:{ai_score["ats_score"]}%;">
                </div>
            </div>
        </div>

        <div class="score-row">
            <div class="score-label-row">
                <span>Technical Skills</span>
                <span>{ai_score["skills_score"]}/100</span>
            </div>

            <div class="score-track">
                <div class="score-fill"
                     style="width:{ai_score["skills_score"]}%;">
                </div>
            </div>
        </div>

        <div class="score-row">
            <div class="score-label-row">
                <span>Projects</span>
                <span>{ai_score["projects_score"]}/100</span>
            </div>

            <div class="score-track">
                <div class="score-fill"
                     style="width:{ai_score["projects_score"]}%;">
                </div>
            </div>
        </div>

        <div class="score-row">
            <div class="score-label-row">
                <span>Experience</span>
                <span>{ai_score["experience_score"]}/100</span>
            </div>

            <div class="score-track">
                <div class="score-fill"
                     style="width:{ai_score["experience_score"]}%;">
                </div>
            </div>
        </div>

        <div class="score-row">
            <div class="score-label-row">
                <span>Structure</span>
                <span>{ai_score["structure_score"]}/100</span>
            </div>

            <div class="score-track">
                <div class="score-fill"
                     style="width:{ai_score["structure_score"]}%;">
                </div>
            </div>
        </div>

        <div class="score-row">
            <div class="score-label-row">
                <span>Role Relevance</span>
                <span>{ai_score["relevance_score"]}/100</span>
            </div>

            <div class="score-track">
                <div class="score-fill"
                     style="width:{ai_score["relevance_score"]}%;">
                </div>
            </div>
        </div>

        <div style="
            margin-top:24px;
            color:#aeb9c8;
            font-size:13px;
            line-height:1.7;
        ">

            <b style="color:#ffffff;">
                AI Summary
            </b>

            <br>

            {ai_score["summary"]}

        </div>

    </div>
    """)


    # ========================================================
    # ORIGINAL GAUGE — DO NOT CHANGE
    # ========================================================

    left, right = st.columns(
        [0.85, 1.15]
    )


    with left:

        score = float(
            best_role["match_score"]
        )

        fig = go.Figure(
            go.Indicator(

                mode="gauge+number",

                value=score,

                number={
                    "suffix": "%",
                    "font": {
                        "size":42,
                        "color":"#ffffff"
                    }
                },

                title={
                    "text":"Overall Career Match",
                    "font":{
                        "size":16,
                        "color":"#cbd5e1"
                    }
                },

                gauge={

                    "axis":{
                        "range":[0,100],
                        "tickcolor":"#64748b"
                    },

                    "bar":{
                        "color":"#8b5cf6"
                    },

                    "bgcolor":"#111827",

                    "borderwidth":0,

                    "steps":[

                        {
                            "range":[0,40],
                            "color":"#21151b"
                        },

                        {
                            "range":[40,70],
                            "color":"#211e14"
                        },

                        {
                            "range":[70,100],
                            "color":"#14221c"
                        }

                    ]
                }
            )
        )

        fig.update_layout(

            height=330,

            margin=dict(
                l=20,
                r=20,
                t=50,
                b=10
            ),

            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={
                "displayModeBar":False
            },

            key="overview_match_gauge"
        )


    with right:

        chart_data = results.sort_values(
            "match_score",
            ascending=True
        )

        fig = go.Figure()

        fig.add_trace(
            go.Bar(

                x=chart_data["match_score"],

                y=chart_data["job_role"],

                orientation="h",

                text=[
                    f"{x:.0f}%"
                    for x in chart_data["match_score"]
                ],

                textposition="outside",

                hovertemplate=
                    "<b>%{y}</b><br>"
                    "Career Match: %{x:.1f}%"
                    "<extra></extra>"
            )
        )

        fig.update_layout(

            title={
                "text":"Career Match Results",
                "font":{
                    "size":20,
                    "color":"#ffffff"
                }
            },

            xaxis={
                "range":[0,110],
                "showgrid":True,
                "gridcolor":
                    "rgba(255,255,255,.055)",
                "zeroline":False
            },

            height=360,

            margin=dict(
                l=20,
                r=65,
                t=70,
                b=35
            ),

            paper_bgcolor="rgba(0,0,0,0)",

            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(

            fig,

            use_container_width=True,

            config={
                "displayModeBar":False
            },

            key="overview_career_chart"
        )


# ============================================================
# CAREER MATCH
# ============================================================

with tab2:

    st.html("""
    <div class="section-title">
        Career Match Engine
    </div>

    <div class="section-subtitle">
        Compare your technical profile against different
        technology career paths.
    </div>
    """)


    selected_role = st.selectbox(

        "Select career role",

        results["job_role"].tolist(),

        key="career_role_selector"
    )


    selected_row = results[
        results["job_role"] == selected_role
    ].iloc[0]


    required_skills = get_required_skills(
        selected_role
    )


    missing_skills = find_missing_skills(
        resume_skills,
        required_skills
    )


    resume_lower = [
        x.lower()
        for x in resume_skills
    ]


    matched_skills = [

        skill

        for skill in required_skills

        if skill.lower()
        in resume_lower

    ]


    c1, c2, c3 = st.columns(3)


    with c1:

        st.metric(
            "Career Match",
            f'{selected_row["match_score"]:.1f}%'
        )


    with c2:

        st.metric(
            "Skills You Have",
            len(matched_skills)
        )


    with c3:

        st.metric(
            "Skills to Learn",
            len(missing_skills)
        )


    st.html("""
    <div class="section-title">
        Skill Gap Analysis
    </div>
    """)


    col1, col2 = st.columns(2)


    with col1:

        st.markdown(
            "### ✦ Skills You Have"
        )

        if matched_skills:

            html = ""

            for skill in matched_skills:

                html += (
                    f'<span class="skill-chip">'
                    f'{skill}'
                    f'</span>'
                )

            st.html(
                f"<div>{html}</div>"
            )

        else:

            st.info(
                "No matching skills detected."
            )


    with col2:

        st.markdown(
            "### ⚡ Skills To Develop"
        )

        if missing_skills:

            html = ""

            for skill in missing_skills:

                html += (
                    f'<span class="missing-chip">'
                    f'{skill}'
                    f'</span>'
                )

            st.html(
                f"<div>{html}</div>"
            )

        else:

            st.success(
                "No major skill gaps detected."
            )


    # ========================================================
    # AI ADVISOR
    # ========================================================

    st.html("""
    <div class="section-title">
        Generative AI Career Advisor
    </div>
    """)


    if st.button(
        "✦ Get My Career Advice",
        key="ai_career_button"
    ):

        with st.spinner(
            "Generating personalized advice..."
        ):

            try:

                response = analyze_resume_with_llm(

                    cleaned_text,

                    selected_role,

                    missing_skills

                )

                st.markdown(
                    response
                )

            except Exception as e:

                st.error(
                    f"Could not generate advice: {e}"
                )


    # ========================================================
    # RESUME REWRITER
    # ========================================================

    st.html("""
    <div class="section-title">
        ✦ AI Resume Rewriter
    </div>

    <div class="section-subtitle">
        Improve individual resume sections without inventing
        experience or achievements.
    </div>
    """)


    rewrite_section = st.selectbox(

        "Section",

        [
            "Professional Summary",
            "Experience",
            "Project",
            "Skills",
            "Achievements"
        ],

        key="rewrite_section"
    )


    rewrite_text = st.text_area(

        "Existing content",

        height=180,

        placeholder=
            "Paste your current resume content here...",

        key="rewrite_text"
    )


    if st.button(
        "✦ Rewrite Section",
        key="rewrite_button"
    ):

        if not rewrite_text.strip():

            st.warning(
                "Paste some content first."
            )

        else:

            with st.spinner(
                "Improving your resume section..."
            ):

                try:

                    rewritten = improve_resume_section(

                        rewrite_text,

                        rewrite_section,

                        selected_role

                    )

                    st.markdown(
                        "### Improved Version"
                    )

                    st.success(
                        rewritten
                    )

                except Exception as e:

                    st.error(
                        f"Rewriter failed: {e}"
                    )


# ============================================================
# AI ROADMAP
# ============================================================

with tab3:

    st.html("""
    <div class="section-title">
        AI-Personalized Learning Roadmap
    </div>

    <div class="section-subtitle">
        A roadmap generated specifically from your current
        skills, missing skills and target role.
    </div>
    """)


    roadmap_key = (
        "ai_roadmap_"
        + selected_role
    )


    if roadmap_key not in st.session_state:

        if st.button(
            "✦ Generate My 6-Week Roadmap",
            key="generate_roadmap_button"
        ):

            with st.spinner(
                "Building your personalized roadmap..."
            ):

                try:

                    st.session_state[
                        roadmap_key
                    ] = generate_ai_roadmap(

                        resume_skills,

                        missing_skills,

                        selected_role

                    )

                except Exception as e:

                    st.error(
                        f"Could not create your learning plan: {e}"
                    )


    if roadmap_key in st.session_state:

        ai_roadmap = st.session_state[
            roadmap_key
        ]

        for week in ai_roadmap.get(
            "roadmap",
            []
        ):

            with st.expander(
                f'WEEK {week.get("week")} · '
                f'{week.get("skill")}'
            ):

                st.markdown(
                    f"""
                    **Topic**

                    {week.get("topic", "")}

                    **What to learn**

                    {week.get("what_to_learn", "")}

                    **Practice task**

                    {week.get("practice_task", "")}

                    **Mini project**

                    {week.get("mini_project", "")}
                    """
                )


    st.divider()


    st.markdown(
        "### Recommended Courses and Resources"
    )


    curated_roadmap = generate_roadmap(
        missing_skills
        if missing_skills
        else required_skills
    )


    if curated_roadmap:

        for item in curated_roadmap:

            st.markdown(
                f"""
                **Week {item.get("week")} ·
                {item.get("skill")}**

                {item.get("topic")}
                """
            )

            if pd.notna(
                item.get("course_url", "")
            ):

                st.markdown(
                    f'[↗ {item.get("course_name", "Course")}]'
                    f'({item.get("course_url")})'
                )


# ============================================================
# JOB DESCRIPTION
# ============================================================

with tab4:

    st.html("""
    <div class="section-title">
        Job Description Intelligence
    </div>

    <div class="section-subtitle">
        Upload a real job description and let AI understand
        its technical requirements.
    </div>
    """)


    uploaded_jd = st.file_uploader(

        "Upload a job posting (PDF or Word)",

        type=[
            "pdf",
            "docx"
        ],

        key="jd_uploader"
    )


    if uploaded_jd:

        try:

            if uploaded_jd.name.lower().endswith(".pdf"):

                jd_text = extract_from_pdf(
                    uploaded_jd
                )

            else:

                jd_text = extract_from_docx(
                    uploaded_jd
                )

        except Exception as e:

            st.error(
                f"Could not read JD: {e}"
            )

            st.stop()


        if jd_text.strip():

            jd_cleaned = clean_text(
                jd_text
            )


            # =================================================
            # AI JD EXTRACTION
            # =================================================

            if st.button(
                "✦ Find Job Requirements",
                key="analyze_jd_button"
            ):

                with st.spinner(
                    "AI is analyzing the job description..."
                ):

                    try:

                        st.session_state.jd_info = (
                            extract_jd_information(
                                jd_text
                            )
                        )

                    except Exception as e:

                        st.error(
                            f"Could not analyze the job posting: {e}"
                        )


            if "jd_info" in st.session_state:

                jd_info = st.session_state[
                    "jd_info"
                ]


                st.markdown(
                    "### ✦ AI-Extracted Requirements"
                )


                categories = [

                    (
                        "Your Technical Skills",
                        "technical_skills"
                    ),

                    (
                        "Programming",
                        "programming_languages"
                    ),

                    (
                        "Frameworks",
                        "frameworks"
                    ),

                    (
                        "Databases",
                        "databases"
                    ),

                    (
                        "Cloud",
                        "cloud"
                    ),

                    (
                        "AI / ML",
                        "ai_ml"
                    ),

                    (
                        "Tools",
                        "tools"
                    )

                ]


                cols = st.columns(2)


                for index, (
                    title,
                    key
                ) in enumerate(categories):

                    with cols[
                        index % 2
                    ]:

                        st.markdown(
                            f"**{title}**"
                        )

                        values = jd_info.get(
                            key,
                            []
                        )

                        if values:

                            html = ""

                            for value in values:

                                html += (
                                    f'<span class="skill-chip">'
                                    f'{value}'
                                    f'</span>'
                                )

                            st.html(
                                f"<div>{html}</div>"
                            )

                        else:

                            st.caption(
                                "Not detected"
                            )


            # =================================================
            # RESUME ↔ JD MATCH
            # =================================================

            st.divider()

            st.markdown(
                "### Resume ↔ Job Match"
            )


            with st.spinner(
                "Comparing your resume with the job requirements..."
            ):

                jd_result = calculate_jd_match(

                    cleaned_text,

                    jd_cleaned

                )


            c1, c2, c3 = st.columns(3)


            with c1:

                st.metric(
                    "Overall Match",
                    f'{jd_result["match_score"]:.1f}%'
                )


            with c2:

                st.metric(
                    "Skill Match",
                    f'{jd_result["skill_score"]:.1f}%'
                )


            with c3:

                st.metric(
                    "Content Match",
                    f'{jd_result["semantic_score"]:.1f}%'
                )


            # =================================================
            # BREAKDOWN CHART
            # =================================================

            jd_breakdown = pd.DataFrame(
                {
                    "Component": [
                        "Skill Match",
                        "Content Match",
                        "Text Match"
                    ],

                    "Score": [
                        jd_result["skill_score"],
                        jd_result["semantic_score"],
                        jd_result["tfidf_score"]
                    ]
                }
            )


            fig = go.Figure()

            fig.add_trace(
                go.Bar(

                    x=jd_breakdown[
                        "Component"
                    ],

                    y=jd_breakdown[
                        "Score"
                    ],

                    text=[
                        f"{x:.1f}%"
                        for x in jd_breakdown[
                            "Score"
                        ]
                    ],

                    textposition="outside"
                )
            )


            fig.update_layout(

                title={
                    "text":
                        "Your Job Match Breakdown",
                    "font":{
                        "size":20,
                        "color":"#ffffff"
                    }
                },

                yaxis={
                    "range":[0,110],
                    "gridcolor":
                        "rgba(255,255,255,.055)"
                },

                height=350,

                paper_bgcolor=
                    "rgba(0,0,0,0)",

                plot_bgcolor=
                    "rgba(0,0,0,0)"
            )


            st.plotly_chart(

                fig,

                use_container_width=True,

                config={
                    "displayModeBar":False
                },

                key="jd_breakdown_chart"
            )


            # =================================================
            # MATCHED / MISSING
            # =================================================

            col1, col2 = st.columns(2)


            with col1:

                st.markdown(
                    "### ✦ Matched Skills"
                )

                for skill in jd_result[
                    "matched_skills"
                ]:

                    st.markdown(
                        f"✓ {skill}"
                    )


            with col2:

                st.markdown(
                    "### ⚡ Missing Skills"
                )

                for skill in jd_result[
                    "missing_skills"
                ]:

                    st.markdown(
                        f"• {skill}"
                    )


            # =================================================
            # AI SIDE-BY-SIDE ANALYSIS
            # =================================================

            st.markdown(
                "### ✦ AI Resume ↔ JD Analysis"
            )


            comparison_key = (
                "comparison_"
                + uploaded_jd.name
            )


            if st.button(
                "Generate Detailed Comparison",
                key="comparison_button"
            ):

                with st.spinner(
                    "AI is comparing your resume with the JD..."
                ):

                    try:

                        st.session_state[
                            comparison_key
                        ] = analyze_resume_vs_jd(

                            cleaned_text,

                            jd_text

                        )

                    except Exception as e:

                        st.error(
                            f"Comparison failed: {e}"
                        )


            if comparison_key in st.session_state:

                comparison = st.session_state[
                    comparison_key
                ]


                col1, col2 = st.columns(2)


                with col1:

                    st.markdown(
                        "#### Resume Strengths"
                    )

                    for item in comparison.get(
                        "strong_matches",
                        []
                    ):

                        st.success(
                            item
                        )


                    st.markdown(
                        "#### Relevant Experience"
                    )

                    for item in comparison.get(
                        "relevant_experience",
                        []
                    ):

                        st.write(
                            "• " + item
                        )


                with col2:

                    st.markdown(
                        "#### Missing Requirements"
                    )

                    for item in comparison.get(
                        "missing_requirements",
                        []
                    ):

                        st.warning(
                            item
                        )


                    st.markdown(
                        "#### Recommendations"
                    )

                    for item in comparison.get(
                        "recommendations",
                        []
                    ):

                        st.write(
                            "→ " + item
                        )


# ============================================================
# PORTFOLIO
# ============================================================

with tab5:

    st.html("""
    <div class="section-title">
        AI Portfolio Builder
    </div>

    <div class="section-subtitle">
        Get project ideas specifically designed to close
        your current skill gaps.
    </div>
    """)


    if st.button(
        "✦ Recommend Projects",
        key="recommend_projects_button"
    ):

        with st.spinner(
            "Finding projects for your profile..."
        ):

            try:

                st.session_state.projects = (
                    recommend_projects(

                        resume_skills,

                        missing_skills,

                        selected_role

                    )
                )

            except Exception as e:

                st.error(
                    f"Project recommendation failed: {e}"
                )


    if "projects" in st.session_state:

        projects = st.session_state[
            "projects"
        ]


        for project in projects.get(
            "projects",
            []
        ):

            technologies = project.get(
                "technologies",
                []
            )

            skills = project.get(
                "skills_gained",
                []
            )


            tech_text = ", ".join(
                technologies
            )

            skill_text = ", ".join(
                skills
            )


            st.html(
                f"""
                <div class="project-card">

                    <div class="project-title">
                        {project.get("title", "")}
                    </div>

                    <div style="
                        margin-top:7px;
                        color:#a78bfa;
                        font-size:11px;
                        font-weight:700;
                    ">
                        {project.get("difficulty", "")}
                    </div>

                    <div class="project-description">
                        {project.get("description", "")}
                    </div>

                    <div style="
                        margin-top:14px;
                        color:#aeb9c8;
                        font-size:12px;
                    ">

                        <b style="color:#ffffff;">
                            Technologies:
                        </b>

                        {tech_text}

                        <br><br>

                        <b style="color:#ffffff;">
                            Skills gained:
                        </b>

                        {skill_text}

                    </div>

                </div>
                """
            )


# ============================================================
# PDF REPORT
# ============================================================

def create_pdf_report():

    buffer = io.BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "ResumeIQ — AI Career Report",
            styles["Title"]
        )
    )

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            f"Target Role: {best_role_name}",
            styles["Heading2"]
        )
    )

    story.append(
        Spacer(1, 10)
    )

    story.append(
        Paragraph(
            f"Career Match: "
            f"{best_role['match_score']:.1f}%",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"AI Resume Score: "
            f"{ai_score['overall_score']}/100",
            styles["BodyText"]
        )
    )

    story.append(
        Paragraph(
            f"Resume Readability: "
            f"{ai_score['ats_score']}/100",
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            "Skills Found in Your Resume",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            ", ".join(resume_skills),
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            "Resume Feedback Summary",
            styles["Heading2"]
        )
    )

    story.append(
        Paragraph(
            str(ai_score["summary"]),
            styles["BodyText"]
        )
    )

    story.append(
        Spacer(1, 15)
    )

    story.append(
        Paragraph(
            "Career Match Results",
            styles["Heading2"]
        )
    )


    table_data = [
        [
            "Role",
            "Match"
        ]
    ]


    for _, row in results.iterrows():

        table_data.append(
            [
                row["job_role"],
                f'{row["match_score"]:.1f}%'
            ]
        )


    table = Table(
        table_data
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0,0),
                    (-1,0),
                    colors.HexColor("#eeeeee")
                ),

                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    .5,
                    colors.grey
                ),

                (
                    "PADDING",
                    (0,0),
                    (-1,-1),
                    7
                )
            ]
        )
    )


    story.append(
        table
    )

    story.append(
        Spacer(1,20)
    )

    story.append(
        Paragraph(
            "Generated by ResumeIQ. "
            "Results are AI-assisted estimates and "
            "should not be treated as automated hiring decisions.",
            styles["Italic"]
        )
    )

    document.build(
        story
    )

    buffer.seek(0)

    return buffer


# ============================================================
# DOWNLOAD REPORT
# ============================================================

st.divider()

st.markdown(
    "### ✦ Export Your Career Report"
)

pdf_data = create_pdf_report()


st.download_button(

    label="Download Career Report",

    data=pdf_data,

    file_name="ResumeIQ_Career_Report.pdf",

    mime="application/pdf",

    key="download_report"
)


# ============================================================
# FOOTER
# ============================================================

st.html("""
<div style="
    text-align:center;
    margin-top:60px;
    padding:25px 0;
    border-top:1px solid rgba(255,255,255,.06);
    color:#596579;
    font-size:11px;
    line-height:1.7;
">

    <b style="color:#727e91;">
        ResumeIQ
    </b>

    · AI Resume & Career Intelligence

    <br>

    Resume Insights · Career Matches · Skill Development · Personalized Guidance

</div>
""")