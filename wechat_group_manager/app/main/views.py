from flask import request, render_template, session, redirect, url_for, current_app
import logging
import json
from .. import db
from ..models import User
from ..emails import send_email
from . import main
#from .forms import NameForm
from .forms import MsgsGroupsForm
from ..logger import handler
from .. import wechat_client


logger = logging.getLogger(__file__)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


@main.route('/', methods=['GET', 'POST'])
def index():
    qrcode_uri = wechat_client.get_qrcode_uri()
    logger.info(qrcode_uri) 
    return render_template('index.html',
                           qrcode_uri=qrcode_uri)

@main.route('/portal', methods=['GET', 'POST'])
def portal():
    msgs_groups_form = MsgsGroupsForm()
    if msgs_groups_form.validate_on_submit():
        msgs = msgs_groups_form.msgs.data.split()
        groups = msgs_groups_form.groups.data.split()
        print msgs
        print groups
        portal_uri = wechat_client.get_portal_uri()
        wechat_client.send_msgs_to_groups(portal_uri, msgs, groups)
        return redirect(url_for('.portal'))
    #form = NameForm()
    #if form.validate_on_submit():
    #    user = User.query.filter_by(username=form.name.data).first()
    #    if user is None:
    #        data = form.name.data
    #        user = User(username=data)
    #        db.session.add(user)
    #        session['known'] = False
    #        if current_app.config['FLASKY_ADMIN']:
    #            send_email(current_app.config['FLASKY_ADMIN'], 'New User',
    #                       'mail/new_user', user=user)
    #    else:
    #        session['known'] = True
    #    session['name'] = form.name.data
    #    return redirect(url_for('.portal'))
    #return render_template('portal.html',
    #                       form=form, name=session.get('name'),
    #                       known=session.get('known', False))
    return render_template('portal.html',
                           form=msgs_groups_form)

@main.route('/login', methods=['POST'])
def login():
    portal_uri = wechat_client.get_portal_uri()
    logger.info(portal_uri)
    wechat_client.login(portal_uri)
    return redirect(url_for('.portal'))
