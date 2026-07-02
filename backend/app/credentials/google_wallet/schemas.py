from pydantic import BaseModel


class GoogleWalletContext(BaseModel):
    issuer_id: str
    class_suffix: str

    business_name: str
    customer_name: str
    card_number: str
    public_id: str
    current_progress: int

    logo_uri: str | None = None
    hero_image_uri: str | None = None