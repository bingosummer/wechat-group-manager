from flask import Flask
from flask import jsonify, request, g, abort, url_for, current_app
from flask import make_response
import json
from libs import WechatManager
from libs import WechatDriver


app = Flask(__name__)
wechat_manager = WechatManager()
wechat_driver = WechatDriver()

@app.route('/')
def get_api():
    return jsonify({
        'api.version': "1.0" 
    })


@app.route('/qrcode')
def get_qrcode_info():
    return jsonify({
        'uuid': wechat_manager.uuid,
        'qrcode.uri': wechat_manager.get_qrcode_uri() 
    })

@app.route('/portal')
def get_portal_uri():
    return jsonify({
        'uuid': wechat_manager.uuid,
        'portal.uri': wechat_manager.get_portal_uri() 
    })

@app.route('/login', methods=['POST'])
def login():
    if not request.json or not 'portal_uri' in request.json:
        abort(400)
    portal_uri = request.json['portal_uri']
    wechat_driver.connect_driver()
    wechat_driver.get(portal_uri)
    wechat_driver.close_driver()
    return jsonify({
        'login': 'ok'
    })

@app.route('/logout', methods=['GET'])
def logout():
    wechat_driver.get(portal_uri)
    return jsonify({
        'logout': 'ok'
    })

@app.route('/msgs', methods=['POST'])
def msgs():
    if not request.json or not 'portal_uri' in request.json or not 'msgs' in request.json or not 'groups' in request.json:
        abort(400)
    portal_uri = request.json['portal_uri']
    msgs = request.json['msgs']
    groups = request.json['groups']
    wechat_driver.connect_driver()
    wechat_driver.get(portal_uri)
    wechat_driver.send_msgs_to_groups(msgs, groups)
    wechat_driver.close_driver()
    return jsonify({
        'send_msgs': 'ok'
    })


if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0")
