import json

from sticker import FlaskAPI

api = FlaskAPI('petstore.yml')

PETS_STORAGE = []


def list_pets(params):
    limit = min(params.get('limit', 100), 100)
    return {'content': json.dumps(PETS_STORAGE[:limit])}


def create_pets(params):
    global PETS_STORAGE
    PETS_STORAGE.append(params['pet'])
    return {'status_code': 201}


def show_pet_by_id(params):
    pet_id = params['petId']
    for pet in PETS_STORAGE:
        if pet['id'] == pet_id:
            return {'content': json.dumps(pet)}
    return {'status_code': 404}


if __name__ == '__main__':
    api.get_app(__name__).run()
