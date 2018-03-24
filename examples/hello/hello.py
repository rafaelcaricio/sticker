

def say_hello(params):
    return {"content": "Hello World!"}


def run_with_flask():
    from sticker import FlaskAPI
    api = FlaskAPI('hello.yml')
    api.get_app(__name__).run()


def run_with_bottle():
    from sticker import BottleAPI
    api = BottleAPI('hello.yml')
    api.run()


if __name__ == '__main__':
    run_with_bottle()
