from app.credentials.google_wallet.schemas import GoogleWalletContext


def build_google_loyalty_class(context: GoogleWalletContext) -> dict:
    class_id = f"{context.issuer_id}.{context.class_suffix}"

    return {
        "id": class_id,
        "issuerName": context.business_name,
        "programName": f"{context.business_name} Loyalty",
        "reviewStatus": "UNDER_REVIEW",
    }