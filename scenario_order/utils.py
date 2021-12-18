from flask import session


def add_to_basket(items):
    basket = session.get('basket', [])
    for item in items:
        basket.append(item)
    session['basket'] = basket


def clear_basket():
    if 'basket' in session:
        session.pop('basket')


def clear_client():
    if 'client_id' in session:
        session.pop('client_id')
