from typing import Any, Dict, Optional, Union
from pydantic import BaseModel


class CredentialsPayload(BaseModel):
    url: str
    username: str
    password: str
    ent_name: Optional[str] = "monlycee_net"


class QRCodePayload(BaseModel):
    qr_data: Union[Dict[str, Any], str]
    pin: str
    uuid: Optional[str] = None


class TokenPayload(BaseModel):
    url: str
    username: str
    token: str
    uuid: Optional[str] = None


class DataPayload(BaseModel):
    session: Dict[str, Any]
    resources: Optional[list[str]] = None


class TokenGenPayload(CredentialsPayload):
    pass
