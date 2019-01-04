#!/usr/bin/python3
from collections import namedtuple
from requests import Request

RequestNamedTuple = namedtuple("RequestNamedTuple", "method headers atlas_url payload credentials")


def create_lineage(atlas_url, description, inputs, operation_type, name, outputs, qualified_name, type_name):
    return payload(description=description, inputs=inputs, operation_type=operation_type, name=name, outputs=outputs,
                   qualified_name=qualified_name, type_name=type_name)


def payload(description, inputs, operation_type, name, outputs, qualified_name, type_name, guid=-1):
    return {
        'description': description,
        'inputs': inputs,
        'operationType': operation_type,
        'name': name,
        'outputs': outputs,
        'qualifiedName': qualified_name,
        'typeName': type_name,
        'guid': guid
    }


def build_request(atlas_url, payload={}, credentials=("admin", "hortonworks1"), method="GET"):
    return RequestNamedTuple(method=method,
                             headers={'Content-Type': 'application/json', 'Accept': 'application/json;charset=UTF-8'},
                             payload=payload,
                             credentials=credentials,
                             atlas_url=atlas_url)


def prepare_request_object(request_named_tuple):
    request = Request(method=request_named_tuple.method,
                      url=request_named_tuple.atlas_url,
                      headers=request_named_tuple.headers,
                      json=request_named_tuple.payload,
                      auth=request_named_tuple.credentials)
    return request.prepare()
