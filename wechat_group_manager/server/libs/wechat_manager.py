import httplib

class WechatManager(object):
    def __init__(self, uuid=''):
        self.set_uuid(uuid)

    def set_uuid(self, uuid):
        if uuid:
            self.uuid = uuid
            return
        uri = "/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=en_US"
        response = self._get_response(uri)
        if response:
            self.uuid = self._get_value_from_response(response, 'window.QRLogin.uuid')
        else:
            self.uuid = None

    def get_qrcode_uri(self):
        if self.uuid:
            return "https://login.weixin.qq.com/qrcode/{0}".format(self.uuid)
        else:
            return ""

    def get_portal_uri(self):
        uri = "/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={0}".format(self.uuid)
        response = self._get_response(uri)
        if response:
            redirect_uri = self._get_value_from_response(response, 'window.redirect_uri')
            return redirect_uri
        return ""

    def _get_response(self, uri):
        headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "application/json","Content-type":"application/xml; charset=utf=8"}
        conn = httplib.HTTPConnection("login.weixin.qq.com")
        conn.request("GET", uri, "", headers)
        response = conn.getresponse()
        if response.status == 200:
            usersdata = response.read()
            return usersdata
        return ""

    def _get_value_from_response(self, response, key):
        for line in response.split(';'):
            line = line.strip()
            if line.startswith(key):
                start = line.index('"')
                end = line.rindex('"')
                return line[start+1:end]


if __name__ == "__main__":
    import time
    manager = WechatManager()
    print manager.get_qrcode_uri()
    time.sleep(30)
    print manager.get_portal_uri()
