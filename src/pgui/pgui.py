from importlib import import_module

from flask import Flask, request, redirect, url_for, escape, get_flashed_messages
from flask.ext.login import LoginManager, login_user, logout_user, login_required

import config
import pages.index
from pg import pg_connection, User


app = Flask(__name__)
app.secret_key = config.SECRET_KEY


# -----------------------------------------------------------------------------
# Setup auth

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_message = ''
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(name):
    if name in User.users:
        return User(name, *User.users[name])
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = 'name' in request.form and escape(request.form['name']) or ''
        pw = 'password' in request.form and escape(request.form['password']) or ''
        host = 'host' in request.form and escape(request.form['host']) or 'localhost'
        port = 'port' in request.form and int(escape(request.form['port'])) or 5432
        login_user(User(name, pw, 'postgres', host, port))
        return redirect(request.args.get('next') or url_for('index'))

    err = get_flashed_messages()
    return pages.index.Login({'err': err}).render()

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# -----------------------------------------------------------------------------
# Setup index pages

@app.route('/')
@app.route('/index')
@login_required
def index():
    return pages.index.Index(request.args).render()


# -----------------------------------------------------------------------------
# Register pages

for page in pages.index.PAGES:
    mod_name = 'pages.%s' % page['name']
    blueprint_name = '%s_page' % page['name']
    try:
        mod = import_module(mod_name)
        blueprint = getattr(mod, blueprint_name)
        app.register_blueprint(blueprint)
    except ImportError as err:
        print('No such module: %s' % err)
    except AttributeError as err:
        if page['name'] != 'index':
            print('Module is missing the expected blueprint: %s' % err)


# -----------------------------------------------------------------------------
# Run app

if __name__ == '__main__':
    app.run(debug=config.DEBUG)
