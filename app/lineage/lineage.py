#!/usr/bin/python3

def create_lineage(atlas_server, token, description, inputs, operation_type, name, outputs, qualified_name, type_name):
    print("Yh")
    payload = {
            'description': description,
            'inputs': inputs,
            'operationType': operation_type,
            'name': name,
            'outputs': outputs,
            'qualifiedName': qualified_name,
            'typeName': type_name
            }
    print('OK')
    return payload


