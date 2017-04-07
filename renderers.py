import vobject
from faker import Factory as FakeFactory
from hashlib import md5
import requests
from io import BytesIO
from pyramid import renderers


class VCardRenderer:
    def __call__(self, info):
        def _renderer(value, system):
            request = system.get('request')
            request.response.content_type = 'text/vcard'
            vCard = VCardRenderer._customer_to_vcard(value)
            return vCard.serialize()
        return _renderer

    @staticmethod
    def _customer_to_vcard(customer):
        fakeFactory = FakeFactory.create()

        vCard = vobject.vCard()
        vCard.add('n')
        vCard.n.value = vobject.vcard.Name(family=customer.last_name, given=customer.first_name)
        vCard.add('fn',)
        vCard.fn.value = '{} {}'.format(customer.first_name, customer.last_name)
        vCard.add('email')
        vCard.email.value = customer.email
        vCard.email.type_param = 'WORK'
        tel = vCard.add('TEL')
        tel.value = fakeFactory.phone_number()
        tel.type_param = 'WORK'
        tel = vCard.add('TEL')
        tel.value = fakeFactory.phone_number()
        tel.type_param = 'HOME'
        vCard.add('title')
        vCard.title.value = fakeFactory.job()

        return vCard


class GravatarRenderer:
    def __call__(self, info):
        def _renderer(value, system):
            _GRAVATAR_URL_TEMPLATE = 'http://www.gravatar.com/avatar/{}'

            request = system.get('request')
            request.response.content_type = 'image/png'

            email = value.email
            gravatar_hash = md5(email.encode('utf-8')).hexdigest()
            gravatar_url = _GRAVATAR_URL_TEMPLATE.format(gravatar_hash)
            gravatar_response = requests.get(gravatar_url)
            request.response.content_type = 'image/png'
            return BytesIO(gravatar_response.content)
        return _renderer


class NegotiatingRenderer:
    _CONNEG_MAPPINGS = {
        #'application/json': renderers.json_renderer_factory,
        'text/plain': renderers.string_renderer_factory
    }

    def __init__(self, mappings=None, **kw):
        if mappings is None:
            mappings = {}

        NegotiatingRenderer._CONNEG_MAPPINGS.update(mappings)
        NegotiatingRenderer._CONNEG_MAPPINGS.update(kw)

    def __call__(self, info):
        def _render(value, system):
            request = system.get('request')
            accept_header = request.headers['accept']

            for key in NegotiatingRenderer._CONNEG_MAPPINGS:
                if key in accept_header:
                    negotiated_render = NegotiatingRenderer._CONNEG_MAPPINGS[key]
                    result = negotiated_render(info)(value, system)
                    return result

        return _render
