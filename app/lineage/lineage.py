#!/usr/bin/python3
from collections import namedtuple
from requests import Request, Session, PreparedRequest, Response

RequestNamedTuple = namedtuple("requestnamedtuple", "method headers atlas_url payload credentials")


def create_lineage(atlas_url: str, description: str, inputs: [dict], operation_type: str, name: str, outputs: [dict],
                   qualified_name: str, type_name: str, credentials=("", "")):
    prepared_request = create_lineage_prepare(atlas_url=atlas_url, description=description, inputs=inputs,
                                              operation_type=operation_type, name=name, outputs=outputs,
                                              qualified_name=qualified_name,
                                              type_name=type_name,
                                              credentials=credentials)
    response = create_lineage_send(prepared_request)
    return create_lineage_prossess(response)


def create_lineage_prepare(atlas_url: str, description: str, inputs: [dict], operation_type: str, name: str,
                           outputs: [dict], qualified_name: str, type_name: str, credentials=("", "")) -> PreparedRequest:
    return prepare_request(
        build_request_named_tuple(
            atlas_url=atlas_url,
            payload=create_lineage_payload(description=description, inputs=inputs, operation_type=operation_type,
                                           name=name, outputs=outputs, qualified_name=qualified_name,
                                           type_name=type_name),
            credentials=credentials,
            method="POST"))


def create_lineage_send(prepared_request: Request) -> Response:
    return send_request(prepared_request)


def create_lineage_prossess(response: Response):
    return True if response.status_code == 200 else (response.status_code, response.reason)


def create_lineage_payload(description: str, inputs: [dict], operation_type: str, name: str, outputs: [dict],
                           qualified_name: str, type_name: str, guid=-1) -> dict:
    return dict(description=description, inputs=inputs, operationType=operation_type, name=name, outputs=outputs,
                qualifiedName=qualified_name, typeName=type_name, guid=guid)


def build_request_named_tuple(atlas_url: str, payload={}, credentials=("", ""),
                              method="GET") -> RequestNamedTuple:
    return RequestNamedTuple(method=method,
                             headers={'Content-Type': 'application/json', 'Accept': 'application/json;charset=UTF-8'},
                             payload=payload,
                             credentials=credentials,
                             atlas_url=atlas_url)


def prepare_request(request_named_tuple: RequestNamedTuple) -> PreparedRequest:
    return Request(method=request_named_tuple.method,
                   url=request_named_tuple.atlas_url,
                   headers=request_named_tuple.headers,
                   json=request_named_tuple.payload,
                   auth=request_named_tuple.credentials).prepare()


def send_request(prepared_request: PreparedRequest) -> Response:
    return Session().send(prepared_request)
