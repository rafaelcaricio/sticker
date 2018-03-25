

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


def run_with_tornado():
    import tornado.ioloop
    from sticker import TornadoAPI
    api = TornadoAPI('hello.yml')
    api.get_app().listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    run_with_tornado()
