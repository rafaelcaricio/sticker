import json

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


def run_with_flask():
    from sticker import FlaskAPI
    api = FlaskAPI('petstore.yml')
    api.get_app(__name__).run()


def run_with_bottle():
    from sticker import BottleAPI
    api = BottleAPI('petstore.yml')
    api.run()


def run_with_tornado():
    import tornado.ioloop
    from sticker import TornadoAPI
    api = TornadoAPI('petstore.yml')
    api.get_app().listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run_with_tornado()
