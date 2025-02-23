from typing import Any, Dict, List, Literal, Union
from pydantic import BaseModel
from video_merge.configs.index import CONFIG
from supabase.client import create_client, Client
from datetime import datetime

url = CONFIG.SUPABASE_URL
key = CONFIG.SUPABASE_KEY

class UserIdentity(BaseModel):
    id: str
    user_id: str
    identity_data: Dict[str, Any]
    provider: str
    created_at: datetime
    last_sign_in_at: Union[datetime, None] = None
    updated_at: Union[datetime, None] = None


class Factor(BaseModel):
    """
    A MFA factor.
    """

    id: str
    """
    ID of the factor.
    """
    friendly_name: Union[str, None] = None
    """
    Friendly name of the factor, useful to disambiguate between multiple factors.
    """
    factor_type: Union[Literal["totp"], str]
    """
    Type of factor. Only `totp` supported with this version but may change in
    future versions.
    """
    status: Literal["verified", "unverified"]
    """
    Factor's status.
    """
    created_at: datetime
    updated_at: datetime


class SupabaseUser(BaseModel):
    id: str
    app_metadata: Dict[str, Any]
    user_metadata: Dict[str, Any]
    aud: str
    confirmation_sent_at: Union[datetime, None] = None
    recovery_sent_at: Union[datetime, None] = None
    email_change_sent_at: Union[datetime, None] = None
    new_email: Union[str, None] = None
    invited_at: Union[datetime, None] = None
    action_link: Union[str, None] = None
    email: Union[str, None] = None
    phone: Union[str, None] = None
    created_at: datetime
    confirmed_at: Union[datetime, None] = None
    email_confirmed_at: Union[datetime, None] = None
    phone_confirmed_at: Union[datetime, None] = None
    last_sign_in_at: Union[datetime, None] = None
    role: Union[str, None] = None
    updated_at: Union[datetime, None] = None
    identities: Union[List[UserIdentity], None] = None
    factors: Union[List[Factor], None] = None

class UserResponse(BaseModel):
    user: SupabaseUser

if not url or not key:
    raise Exception("SUPABASE_URL or SUPABASE_KEY is not set")

supabase: Client = create_client(url, key)