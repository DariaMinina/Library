import os

from flask import Blueprint, render_template, session, request, current_app
from scenario_auth.sql_provider import SQLProvider
from database import work_with_db

auth_app = Blueprint('auth', __name__, template_folder='templates')
provider = SQLProvider("scenario_auth/sql/")


@auth_app.route('/', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        login = request.form.get('login', None)
        password = request.form.get('password', None)
        sql = provider.get('find_group.sql', login=login, password=password)
        if not sql or not login or not password:
            return render_template('not_correct_data.html')
        else:
            user_group = str(work_with_db(current_app.config['DB_CONFIG'], sql))[17:-3]
            if user_group:
                session['group_name'] = user_group
                return render_template('back_in_menu.html', text="Вы авторизованы как ", user=str(user_group))
            else:
                return render_template('login.html', error='Вы не авторизованы в системе. ')
