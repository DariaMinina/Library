from flask import session, request, current_app, render_template
from functools import wraps


def group_permission_validation(config: dict, sess:session) -> bool:
    group = session.get('group_name', 'unauthorized')
    book = {
        1: '',
        2: request.endpoint
    }
    target_app = book[len(request.endpoint.split('.'))]
    if group in config and target_app in config[group]:
        return True
    return False


def login_permission_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if group_permission_validation(current_app.config['ACCESS_CONFIG'], session):
            return f(*args, **kwargs)
        return render_template('back_in_menu_nv.html', text='Доступ к странице запрещен.')
    return wrapper



