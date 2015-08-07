#!/usr/bin/env python
import sys
from client import WechatClient

wechat_client = WechatClient()

with open(sys.argv[1], 'r') as f:
    msgs = f.read().split('\n')
    msgs = [msg.decode('utf-8') for msg in msgs]
groups = sys.argv[2].split()

print msgs
print groups
portal_uri = wechat_client.get_portal_uri()
wechat_client.send_msgs_to_groups(portal_uri, msgs, groups)
