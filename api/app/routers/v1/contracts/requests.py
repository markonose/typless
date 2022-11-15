from datetime import datetime as dt

from fastapi import HTTPException, Body, Path

from pydantic.dataclasses import dataclass


@dataclass
class GetDocumentsRequest:
    identifier: str | None = None
    type: str | None = None
    datetime: dt | None = None

    def validate(self):
        identifier_has_value = self.identifier is not None
        type_has_value = self.type is not None
        datetime_has_value = self.datetime is not None

        if not any((identifier_has_value, type_has_value, datetime_has_value)):
            raise HTTPException(422, [{'msg': "either 'identifier' or 'type' or 'datetime' must be set"}])


@dataclass
class DeleteDocumentRequest:
    id: str | None = Path()


@dataclass
class UpdateDocumentRequest:
    id: str | None = Path()
    identifier: str | None = Body(default=None)
    type: str | None = Body(default=None)
    datetime: dt | None = Body(default=None)
