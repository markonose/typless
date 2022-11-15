from typing import Dict, List

from bson import ObjectId
from fastapi import APIRouter, Depends
from fastapi.responses import PlainTextResponse

from app.db import db

from .contracts import GetDocumentsRequest, GetDocumentsResponse, DeleteDocumentRequest, UpdateDocumentRequest

router = APIRouter(prefix='/api/v1')


def _get_find_filter(request: GetDocumentsRequest) -> Dict[str, any]:
    filter_ = {}

    if request.identifier:
        filter_['identifier'] = request.identifier

    if request.type:
        filter_['type'] = request.type

    if request.datetime:
        filter_['datetime'] = request.datetime

    return filter_


@router.get('/documents', response_model=List[GetDocumentsResponse])
async def get_documents(request: GetDocumentsRequest = Depends(GetDocumentsRequest)):
    request.validate()

    documents = await db.documents.find(_get_find_filter(request)).to_list(100)

    response = []
    for document in documents:
        document_response = GetDocumentsResponse(
            _id=str(document['_id']),
            identifier=document['identifier'],
            type=document['type'],
            datetime=document['datetime'],
        )

        response.append(document_response)

    return response


@router.delete('/documents/{id}', status_code=204)
async def delete_document(request: DeleteDocumentRequest = Depends(DeleteDocumentRequest)):
    await db.documents.delete_one({'_id': ObjectId(request.id)})


def _get_updated_fields(request: UpdateDocumentRequest) -> Dict[str, any]:
    updated_fields = {}

    if request.identifier:
        updated_fields['identifier'] = request.identifier

    if request.type:
        updated_fields['type'] = request.type

    if request.datetime:
        updated_fields['datetime'] = request.datetime

    return updated_fields


@router.patch('/documents/{id}', response_class=PlainTextResponse)
async def update_document(request: UpdateDocumentRequest = Depends(UpdateDocumentRequest)):
    await db.documents.update_one({'_id': ObjectId(request.id)},
                                  {"$set": _get_updated_fields(request)})

    return "Ok"
