from pydantic import BaseModel
from typing import Optional, Any


class LinkageJobResult(BaseModel):
    linkage_df: Optional[Any]
