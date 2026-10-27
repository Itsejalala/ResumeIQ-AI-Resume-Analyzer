import re


def clean_text(text):
    # Convert text to lowercase
    text = text.lower()

    # Replace multiple spaces/newlines with one space
    text = re.sub(r"\s+", " ", text)

    # Remove unnecessary characters
    text = re.sub(r"[^a-zA-Z0-9+#.\s-]", "", text)

    # Remove extra spaces from beginning and end
    text = text.strip()

    return text