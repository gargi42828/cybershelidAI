import os
import re
import math
import ipaddress
from urllib.parse import urlparse

import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# Configuration
# ============================================================

DATASET_PATH = "datasets/phishing_urls.csv"
MODEL_PATH = "ml_models/phishing_url_model.joblib"


# ============================================================
# URL Feature Extraction
# ============================================================

def is_ip_address(hostname):
    """Return 1 if the hostname is an IP address, otherwise 0."""
    if not hostname:
        return 0

    try:
        ipaddress.ip_address(hostname)
        return 1
    except ValueError:
        return 0


def calculate_entropy(text):
    """Calculate Shannon entropy of a string."""
    if not text:
        return 0.0

    probabilities = [
        text.count(char) / len(text)
        for char in set(text)
    ]

    return -sum(
        p * math.log2(p)
        for p in probabilities
        if p > 0
    )


def extract_url_features(url):
    """Extract features that can be calculated directly from a URL."""

    url = str(url).strip()

    # Make sure urlparse can identify the hostname
    parsed_url = urlparse(url if "://" in url else "http://" + url)

    hostname = parsed_url.hostname or ""
    path = parsed_url.path or ""
    query = parsed_url.query or ""

    # Remove leading www for basic domain analysis
    domain = hostname.lower()

    # Count subdomains
    domain_parts = domain.split(".") if domain else []
    subdomain_count = max(len(domain_parts) - 2, 0)

    features = {
        "url_length": len(url),

        "hostname_length": len(hostname),

        "path_length": len(path),

        "query_length": len(query),

        "domain_length": len(domain),

        "is_ip_address": is_ip_address(hostname),

        "has_https": int(parsed_url.scheme.lower() == "https"),

        "number_of_dots": url.count("."),

        "number_of_hyphens": url.count("-"),

        "number_of_underscores": url.count("_"),

        "number_of_slashes": url.count("/"),

        "number_of_question_marks": url.count("?"),

        "number_of_equals": url.count("="),

        "number_of_ampersands": url.count("&"),

        "number_of_at": url.count("@"),

        "number_of_percent": url.count("%"),

        "number_of_digits": sum(char.isdigit() for char in url),

        "number_of_letters": sum(char.isalpha() for char in url),

        "number_of_special_chars": len(
            re.findall(r"[^a-zA-Z0-9]", url)
        ),

        "has_at_symbol": int("@" in url),

        "has_double_slash": int("//" in url.replace("https://", "").replace("http://", "")),

        "has_www": int("www." in domain),

        "has_login_word": int(
            any(word in url.lower() for word in [
                "login",
                "signin",
                "sign-in",
                "account",
                "verify",
                "verification"
            ])
        ),

        "has_security_word": int(
            any(word in url.lower() for word in [
                "secure",
                "security",
                "confirm",
                "update",
                "authenticate"
            ])
        ),

        "has_suspicious_word": int(
            any(word in url.lower() for word in [
                "free",
                "winner",
                "prize",
                "bonus",
                "claim",
                "gift"
            ])
        ),

        "subdomain_count": subdomain_count,

        "hostname_entropy": calculate_entropy(hostname),

        "url_entropy": calculate_entropy(url),
    }

    return features


# ============================================================
# Load Dataset
# ============================================================

print("Loading dataset...")

df = pd.read_csv(DATASET_PATH)

print("Dataset shape:", df.shape)


# ============================================================
# Create URL features
# ============================================================

print("Extracting URL features...")

feature_rows = []

for index, url in enumerate(df["URL"]):

    feature_rows.append(
        extract_url_features(url)
    )

    if (index + 1) % 25000 == 0:
        print(
            f"Processed {index + 1} / {len(df)} URLs"
        )


X = pd.DataFrame(feature_rows)

# Dataset:
# 1 = legitimate
# 0 = phishing
y = df["label"]


print("\nFeature matrix shape:", X.shape)

print("\nFeatures used:")
print(X.columns.tolist())


# ============================================================
# Train / Test Split
# ============================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# Train Random Forest
# ============================================================

print("\nTraining URL phishing model...")

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42,
    n_jobs=-1,
    class_weight="balanced"
)

model.fit(X_train, y_train)

print("Training completed.")


# ============================================================
# Evaluate Model
# ============================================================

predictions = model.predict(X_test)

accuracy = accuracy_score(
    y_test,
    predictions
)

print("\n========================================")
print("MODEL RESULTS")
print("========================================")

print(f"\nAccuracy: {accuracy:.4f}")

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        predictions,
        target_names=[
            "Phishing",
            "Legitimate"
        ]
    )
)


# ============================================================
# Save Model
# ============================================================

os.makedirs(
    "ml_models",
    exist_ok=True
)

model_package = {
    "model": model,
    "features": list(X.columns)
}

joblib.dump(
    model_package,
    MODEL_PATH
)

print("\n========================================")
print("MODEL SAVED")
print("========================================")

print(
    f"Location: {MODEL_PATH}"
)