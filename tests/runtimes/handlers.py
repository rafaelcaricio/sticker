

def handler_set_status_code(params):
    return {"status": 201}


def handler_set_status_and_content(params):
    return {
        "content": '{"id":"123"}',
        "status": 201
    }


def handler_set_status_code_to_400(params):
    return {"status": 400}


def handler_set_headers(params):
    return {
        "headers": {
            "Content-Type": "application/json"
        },
        "content": '{"id":"123"}',
        "status": 201
    }
