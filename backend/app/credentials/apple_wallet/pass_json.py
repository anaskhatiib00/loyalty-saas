from app.credentials.apple_wallet.schemas import ApplePassContext


def build_pass_json(context: ApplePassContext) -> dict:
    return {
        "formatVersion": 1,
        "passTypeIdentifier": context.pass_type_identifier,
        "serialNumber": context.serial_number,
        "teamIdentifier": context.team_identifier,
        "organizationName": context.organization_name,
        "description": context.description,
        "logoText": context.logo_text,
        "foregroundColor": context.foreground_color,
        "backgroundColor": context.background_color,
        "labelColor": context.label_color,
        "authenticationToken": context.authentication_token,
        "barcode": {
            "message": context.public_id,
            "format": "PKBarcodeFormatQR",
            "messageEncoding": "iso-8859-1",
        },
        context.pass_type.value: {
            "primaryFields": [
                {
                    "key": "customer",
                    "label": "Customer",
                    "value": context.customer_name,
                }
            ],
            "secondaryFields": [
                {
                    "key": "business",
                    "label": "Business",
                    "value": context.business_name,
                },
                {
                    "key": "progress",
                    "label": "Progress",
                    "value": context.current_progress,
                },
            ],
            "auxiliaryFields": [
                {
                    "key": "card_number",
                    "label": "Card Number",
                    "value": context.card_number,
                }
            ],
        },
    }