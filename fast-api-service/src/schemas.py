from typing import Optional
from pydantic import BaseModel

class ModelLogin(BaseModel):
    username: str
    password: str
    appversion: str
    device_info: Optional[str]
    device_id: str
    imei: str

    
class ModelPromoCompetitor(BaseModel):
    tbluserid: str
    tblstoreid: str
    photo: str
    mobile_generated_id: str
    date_created: str
    date_updated: str