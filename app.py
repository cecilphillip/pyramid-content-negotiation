from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.renderers import JSON
from customer import Customer
from renderers import VCardRenderer, GravatarRenderer, NegotiatingRenderer


def configure_renderers(config):
    json_renderer = JSON()
    json_renderer.add_adapter(Customer, lambda p, _: p.__dict__)
    config.add_renderer('json', json_renderer)
    config.add_renderer('vcard', VCardRenderer())
    config.add_renderer('img', GravatarRenderer())

    mappings = {
        'application/json' : json_renderer,
        'text/vcard': VCardRenderer(),
        'image/png': GravatarRenderer()
    }
    negotiator = NegotiatingRenderer(mappings)
    config.add_renderer('negotiate', negotiator)

if __name__ == '__main__':
    config = Configurator()
    config.add_route('customers', '/api/customers')
    config.add_route('customer', '/api/customers/{name}')
    config.scan('views')


    configure_renderers(config)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 6363, app)
    server.serve_forever()
