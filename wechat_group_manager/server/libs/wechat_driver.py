#!/usr/bin/env python
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class WechatDriver(object):
    def __init__(self):
        self.driver = None

    def connect_driver(self, host='http://127.0.0.1', port='4444'):
        self.driver = webdriver.Remote(
            command_executor='{0}:{1}/wd/hub'.format(host,port),
            desired_capabilities=DesiredCapabilities.CHROME)
        
    def close_driver(self):
        if self.driver:
            self.driver.close()

    def get(self, portal_uri):
        if portal_uri:
            self.driver.get(portal_uri)
            if "check ticket failed" in self.driver.page_source:
                raise Exception("Ticket timeout")

    def send_msgs_to_groups(self, msgs, groups):
        for msg in msgs:
            self.send_msg_to_groups(msg, groups)

    def send_msgs_to_group(self, msgs, group):
        pass

    def send_msg_to_groups(self, msg, groups):
        for group in groups:
            self.send_msg_to_group(msg, group)

    def send_msg_to_group(self, msg, group):
        try:
            self.select_group(group)
            time.sleep(10)
            self.send_msg(msg)
            time.sleep(10)
        except Exception, e:
            print e

    def send_msg(self, msg):
        edit_area = self.driver.find_element_by_id("editArea")
        edit_area.send_keys(msg)
        edit_area.send_keys(Keys.RETURN)

    def recv_msg(self):
        pass

    def select_group(self, group):
        search_input = self.driver.find_element_by_class_name("frm_search")
        search_input.send_keys(group)
        time.sleep(5)
        group_elem = self.driver.find_element_by_class_name("contact_item")
        group_elem.click()
        #search_input.click("xpath=//div[@class='contact_item']")
        #search_input.send_keys(Keys.RETURN)


if __name__ == "__main__":
    wechat_driver = WechatDriver()
    wechat_driver.connect_driver()
    wechat_driver.get(portal_uri="https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?ticket=74b1e8f2f87a45588cb52df39169ff9c&uuid=368eb57e848d42&lang=en_US&scan=1436786474")
    wechat_driver.close_driver()
