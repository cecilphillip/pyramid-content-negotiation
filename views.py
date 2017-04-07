from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from customer import CustomerFactory

__CUSOMTERS = CustomerFactory.create_batch(20)


@view_config(route_name='customers', renderer='json',request_method='GET',accept="application/json")
def retrieve_customers(request):
    return __CUSOMTERS


# @view_config(route_name='customer', renderer='json', request_method='GET', accept="application/json")
# @view_config(route_name='customer', renderer='vcard', request_method='GET', accept="text/vcard")
# @view_config(route_name='customer', renderer='img', request_method='GET', accept="image/png")
@view_config(route_name='customer', renderer='negotiate', request_method='GET')
def retrieve_customer(request):
    name = request.matchdict['name']
    customer = [cus for cus in __CUSOMTERS if cus.first_name.lower() == name.lower()]
    return customer[0] if any(customer) else HTTPNotFound()
