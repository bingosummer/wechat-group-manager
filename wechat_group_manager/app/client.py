import httplib
import json
import requests
import urllib
import urlparse

class WechatClient(object):
    def __init__(self):
        self.session = requests.Session()
        self.port = 5000
        self.base_url = "http://127.0.0.1:{0}/".format(self.port)

    def get_qrcode_uri(self):
        url = urlparse.urljoin(self.base_url, 'qrcode')
        response = self.session.get(url).json()
        return response['qrcode.uri']

    def get_portal_uri(self):
        url = urlparse.urljoin(self.base_url, 'portal')
        response = self.session.get(url).json()
        return response['portal.uri']

    def login(self, portal_uri):
        userdatas = dict()
        userdatas['portal_uri'] = portal_uri
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = urlparse.urljoin(self.base_url, 'login')
        response = requests.post(url, data=json.dumps(userdatas), headers=headers).json()
        return response['login']

    def send_msgs_to_groups(self, portal_uri, msgs, groups):
        userdatas = {'portal_uri': portal_uri, 'msgs': msgs, 'groups': groups}
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        url = urlparse.urljoin(self.base_url, 'msgs')
        response = requests.post(url, data=json.dumps(userdatas), headers=headers).json()



if __name__ == "__main__":
    client = WechatClient()
    #print client.get_qrcode_uri()
    #import time
    #time.sleep(30)
    #portal_uri = client.get_portal_uri()
    #client.login(portal_uri)
    print client.login("test uri")
