from pathlib import Path
import pandas as pd


# Get the folder where this Python file is located
BASE_DIR = Path(__file__).resolve().parent

# Build the correct path to the CSV file
RESOURCE_FILE = BASE_DIR / "data" / "learning_resources.csv"


def load_learning_resources():

    if not RESOURCE_FILE.exists():
        raise FileNotFoundError(
            f"Learning resources file not found:\n{RESOURCE_FILE}"
        )

    return pd.read_csv(RESOURCE_FILE)


def generate_roadmap(skills):

    resources = load_learning_resources()

    if not skills:
        return []

    skills_lower = [
        skill.lower().strip()
        for skill in skills
    ]

    resources["skill_lower"] = (
        resources["skill"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    roadmap = resources[
        resources["skill_lower"].isin(skills_lower)
    ].copy()

    roadmap = roadmap.sort_values(
        by=["week", "priority"],
        ascending=[True, True]
    )

    roadmap = roadmap.drop(
        columns=["skill_lower"]
    )

    return roadmap.to_dict(
        orient="records"
    )