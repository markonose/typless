from datetime import datetime as dt

from pydantic import Field, BaseModel


class GetDocumentsResponse(BaseModel):
    id: str = Field(alias='_id')
    identifier: str = Field()
    type: str = Field()
    datetime: dt = Field()
