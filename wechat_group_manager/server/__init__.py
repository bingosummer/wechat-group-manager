from flask import Flask
from config import config
#from libs import WechatDriver
from libs import WechatManager

#wechat_driver = WechatDriver()
wechat_manager = WechatManager()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app
