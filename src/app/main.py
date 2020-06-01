import datetime
import logging

import requests as request_other
from flask import render_template, Blueprint, redirect, request, url_for, session

from . import app

main = Blueprint('main', __name__, template_folder='app/templates', static_folder='app/static')
logger = logging.getLogger(__name__)
CLIENT_ID = app.config['CLIENT_ID']
CLIENT_SECRET = app.config['CLIENT_SECRET']
SCOPE = "friends"
VERSION = "5.107"


@main.route('/', methods=['GET'])
def index():
    information = session.get('info')
    if information is None:
        message = 'PLEASE, LOGIN'
        return render_template('base.html', message=message)
    else:
        access_token = information.get('access_token')
        user_id = information.get('user_id')
        logger.warning('GOT: ' + str(access_token))
        my_full_info = request_other.get("https://api.vk.com/method/users.get"
                                    "?user_ids={user_id}"
                                    "&fields=first_name,last_name"
                                    "&access_token={access_token}"
                                    "&v={version}".format(user_id=user_id,
                                                          access_token=access_token,
                                                          version=VERSION)).json()

        friend_list = request_other.get("https://api.vk.com/method/friends.get"
                                        "?order=random"
                                        "&count=5"
                                        "&fields=first_name,last_name"
                                        "&access_token={access_token}"
                                        "&v={version}".format(access_token=access_token,
                                                              version=VERSION)).json()
        friends = friend_list['response']['items']
        my_info = my_full_info['response'][0]
        return render_template('base.html', friends=friends, my_info=my_info)


@main.route('/auth', methods=['GET'])
def auth_second_step():
    code = request.args.get('code')
    data = request_other.get("https://oauth.vk.com/access_token?"
                             "client_id={client_id}"
                             "&client_secret={client_secret}"
                             "&redirect_uri=http://323874-ch74890.tmweb.ru/auth"
                             "&code={code}".format(client_id=str(CLIENT_ID),
                                                   client_secret=str(CLIENT_SECRET),
                                                   code=code)).json()
    if 'access_token' in data:
        access_token = data['access_token']
        expires_in = data['expires_in']
        user_id = data['user_id']
        information = session.get('info')
        if information is None:
            info = {'access_token': str(access_token), 'user_id': str(user_id)}
            session['info'] = info
            session.permanent = True
            app.permanent_session_lifetime = datetime.timedelta(seconds=expires_in)
    return redirect(url_for('main.index'))


@main.route('/auth_first', methods=['GET'])
def auth_first_step():
    return redirect("https://oauth.vk.com/authorize?"
                    "client_id={client_id}"
                    "&display=page"
                    "&redirect_uri=http://323874-ch74890.tmweb.ru/auth"
                    "&scope={scope}"
                    "&response_type=code"
                    "&v=5.107".format(client_id=str(CLIENT_ID),
                                      scope=str(SCOPE)))
