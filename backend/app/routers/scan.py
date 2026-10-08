
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
import joblib
import pandas as pd
import math
import ipaddress
import re

from urllib.parse import urlparse

from backend.app.database.connection import get_db
from backend.app.database.models import SecurityScan, User
from backend.app.dependencies import get_current_user


router = APIRouter(
    prefix="/scan",
    tags=["Security Scan"]
)


# ============================================================
# Load trained ML model
# ============================================================

MODEL_PATH = "ml_models/phishing_url_model.joblib"

try:
    model_package = joblib.load(MODEL_PATH)

    model = model_package["model"]
    FEATURE_NAMES = model_package["features"]

    print("Phishing URL ML model loaded successfully.")

except Exception as e:
    model = None
    FEATURE_NAMES = []

    print(f"Warning: Could not load phishing model: {e}")


# ============================================================
# IP Address Detection
# ============================================================

def is_ip_address(hostname):
    if not hostname:
        return 0

    try:
        ipaddress.ip_address(hostname)
        return 1

    except ValueError:
        return 0


# ============================================================
# Entropy Calculation
# ============================================================

def calculate_entropy(text):
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


# ============================================================
# URL Feature Extraction
# ============================================================

def extract_url_features(url):

    url = str(url).strip()

    parsed_url = urlparse(
        url if "://" in url else "http://" + url
    )

    hostname = parsed_url.hostname or ""
    path = parsed_url.path or ""
    query = parsed_url.query or ""

    domain = hostname.lower()

    domain_parts = (
        domain.split(".")
        if domain
        else []
    )

    subdomain_count = max(
        len(domain_parts) - 2,
        0
    )

    features = {

        "url_length": len(url),

        "hostname_length": len(hostname),

        "path_length": len(path),

        "query_length": len(query),

        "domain_length": len(domain),

        "is_ip_address": is_ip_address(
            hostname
        ),

        "has_https": int(
            parsed_url.scheme.lower() == "https"
        ),

        "number_of_dots": url.count("."),

        "number_of_hyphens": url.count("-"),

        "number_of_underscores": url.count("_"),

        "number_of_slashes": url.count("/"),

        "number_of_question_marks": url.count("?"),

        "number_of_equals": url.count("="),

        "number_of_ampersands": url.count("&"),

        "number_of_at": url.count("@"),

        "number_of_percent": url.count("%"),

        "number_of_digits": sum(
            char.isdigit()
            for char in url
        ),

        "number_of_letters": sum(
            char.isalpha()
            for char in url
        ),

        "number_of_special_chars": len(
            re.findall(
                r"[^a-zA-Z0-9]",
                url
            )
        ),

        "has_at_symbol": int(
            "@" in url
        ),

        "has_double_slash": int(
            "//" in url.replace(
                "https://",
                ""
            ).replace(
                "http://",
                ""
            )
        ),

        "has_www": int(
            "www." in domain
        ),

        "has_login_word": int(
            any(
                word in url.lower()
                for word in [
                    "login",
                    "signin",
                    "sign-in",
                    "account",
                    "verify",
                    "verification"
                ]
            )
        ),

        "has_security_word": int(
            any(
                word in url.lower()
                for word in [
                    "secure",
                    "security",
                    "confirm",
                    "update",
                    "authenticate"
                ]
            )
        ),

        "has_suspicious_word": int(
            any(
                word in url.lower()
                for word in [
                    "free",
                    "winner",
                    "prize",
                    "bonus",
                    "claim",
                    "gift"
                ]
            )
        ),

        "subdomain_count": subdomain_count,

        "hostname_entropy": calculate_entropy(
            hostname
        ),

        "url_entropy": calculate_entropy(
            url
        )
    }

    return features


# ============================================================
# POST /scan/
# Perform Security Scan
# ============================================================

@router.post("/")
def create_scan(
    input_text: str = Body(..., embed=True),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate input
    if not input_text.strip():

        raise HTTPException(
            status_code=400,
            detail="URL cannot be empty"
        )

    # Check ML model
    if model is None:

        raise HTTPException(
            status_code=500,
            detail="ML model is not available"
        )

    # Extract URL features
    features = extract_url_features(
        input_text
    )

    # Convert features to DataFrame
    feature_df = pd.DataFrame(
        [features]
    )

    # Ensure exact feature order
    try:

        feature_df = feature_df[
            FEATURE_NAMES
        ]

    except KeyError as e:

        raise HTTPException(
            status_code=500,
            detail=f"Feature mismatch: {str(e)}"
        )

    # ========================================================
    # ML Prediction
    # ========================================================

    prediction = model.predict(
        feature_df
    )[0]

    probabilities = model.predict_proba(
        feature_df
    )[0]

    confidence = float(
        max(probabilities) * 100
    )

    # Dataset labels:
    #
    # 0 = Phishing
    # 1 = Legitimate

    if prediction == 0:

        threat_type = "Phishing"

        if confidence >= 90:
            risk_level = "High"

        elif confidence >= 70:
            risk_level = "Medium"

        else:
            risk_level = "Low"

    else:

        threat_type = "Legitimate"

        if confidence >= 90:
            risk_level = "Low"

        elif confidence >= 70:
            risk_level = "Medium"

        else:
            risk_level = "High"

    # ========================================================
    # Save scan to PostgreSQL
    # ========================================================

    scan = SecurityScan(

        user_id=current_user.id,

        input_text=input_text,

        threat_type=threat_type,

        risk_level=risk_level,

        confidence=f"{confidence:.2f}%"
    )

    db.add(scan)

    db.commit()

    db.refresh(scan)

    # ========================================================
    # API Response
    # ========================================================

    return {

        "message": "Scan completed successfully",

        "scan_id": scan.id,

        "user_id": current_user.id,

        "input_text": input_text,

        "threat_type": threat_type,

        "risk_level": risk_level,

        "confidence": f"{confidence:.2f}%"
    }


# ============================================================
# GET /scan/history
# Get Current User's Scan History
# ============================================================

@router.get("/history")
def get_scan_history(

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )

):

    scans = (

        db.query(SecurityScan)

        .filter(
            SecurityScan.user_id == current_user.id
        )

        .order_by(
            SecurityScan.created_at.desc()
        )

        .all()
    )

    return {

        "user_id": current_user.id,

        "total_scans": len(scans),

        "scans": [

            {

                "scan_id": scan.id,

                "input_text": scan.input_text,

                "threat_type": scan.threat_type,

                "risk_level": scan.risk_level,

                "confidence": scan.confidence,

                "created_at": scan.created_at

            }

            for scan in scans

        ]

    }
@router.get("/statistics")
def get_scan_statistics(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    scans = (
        db.query(SecurityScan)
        .filter(SecurityScan.user_id == current_user.id)
        .all()
    )

    total_scans = len(scans)

    phishing_detected = sum(
        1 for scan in scans
        if scan.threat_type == "Phishing"
    )

    legitimate_urls = sum(
        1 for scan in scans
        if scan.threat_type == "Legitimate"
    )

    high_risk = sum(
        1 for scan in scans
        if scan.risk_level == "High"
    )

    medium_risk = sum(
        1 for scan in scans
        if scan.risk_level == "Medium"
    )

    low_risk = sum(
        1 for scan in scans
        if scan.risk_level == "Low"
    )

    return {
        "user_id": current_user.id,
        "total_scans": total_scans,
        "phishing_detected": phishing_detected,
        "legitimate_urls": legitimate_urls,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk
    }
