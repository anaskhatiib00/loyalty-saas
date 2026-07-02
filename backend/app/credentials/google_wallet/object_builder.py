from app.credentials.google_wallet.schemas import GoogleWalletContext


def build_google_loyalty_object(context: GoogleWalletContext) -> dict:
    class_id = f"{context.issuer_id}.{context.class_suffix}"
    object_id = f"{context.issuer_id}.{context.public_id}"

    return {
        "id": object_id,
        "classId": class_id,
        "accountId": context.card_number,
        "accountName": context.customer_name,
        "loyaltyPoints": {
            "label": "Progress",
            "balance": {
                "string": str(context.current_progress),
            },
        },
        "barcode": {
            "type": "QR_CODE",
            "value": context.public_id,
        },
        "state": "ACTIVE",
    }