from pydantic import BaseModel

from app.credentials.apple_wallet.enums import ApplePassType


class ApplePassContext(BaseModel):
    pass_type: ApplePassType = ApplePassType.STORE_CARD

    serial_number: str
    authentication_token: str

    team_identifier: str
    pass_type_identifier: str
    organization_name: str

    description: str
    logo_text: str

    foreground_color: str = "rgb(255, 255, 255)"
    background_color: str = "rgb(0, 0, 0)"
    label_color: str = "rgb(255, 255, 255)"

    card_number: str
    public_id: str
    customer_name: str
    business_name: str
    current_progress: int