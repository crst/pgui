from importlib import import_module
import logging
import logging.handlers

from flask import Flask, request, redirect, url_for, escape, get_flashed_messages
from flask.ext.login import LoginManager, login_user, logout_user, login_required

import config
import pages.index
from pg import pg_connection, User


app = Flask(__name__)
app.secret_key = config.SECRET_KEY


# -----------------------------------------------------------------------------
# Setup auth
#
# There is no real application auth, as we just use the database
# connection parameters. To make this work with flask.ext.login, we
# construct a (temporary) user on-the-fly at login. The auth check is
# then if we can connect with the given parameters to the database.
#
# IMPORTANT: The application is not intended to be available on a
# public network, as access to the application is basically equivalent
# to direct access to the database!

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = 'strong'
login_manager.login_message = ''
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(key):
    if key in User.users:
        return User.users[key]
    return None

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        name = 'name' in request.form and escape(request.form['name']) or ''
        pw = 'password' in request.form and escape(request.form['password']) or ''
        host = 'host' in request.form and escape(request.form['host']) or 'localhost'
        port = 'port' in request.form and int(escape(request.form['port'])) or 5432
        u = User(name, pw, 'postgres', host, port)
        if u.is_authenticated():
            login_user(u)
            return redirect(url_for('index'))

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
    logging.basicConfig(filename='pgui.log',
                        level=logging.WARNING,
                        format='%(asctime)s %(message)s'
    )

    app.run(debug=config.DEBUG)
