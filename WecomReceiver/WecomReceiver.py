from __future__ import annotations

import inspect
import os
import traceback
import xml.etree.cElementTree as ET
import loguru
from flask import Blueprint, request, abort
from urllib.parse import unquote

from .WXBizMsgCrypt.WXBizMsgCrypt3 import WXBizMsgCrypt


class WecomReceiver(Blueprint):
    def __init__(
        self,
        token: str,
        encodingAESKey: str,
        cid: str,
        name: str,
        import_name: str,
        logger: loguru.Logger | None = None,
        static_folder: str | os.PathLike | None = None,
        static_url_path: str | None = None,
        template_folder: str | os.PathLike | None = None,
        url_prefix: str | None = None,
        subdomain: str | None = None,
        url_defaults: dict | None = None,
        root_path: str | None = None
    ):
        super().__init__(
            name=name,
            import_name=import_name,
            static_folder=static_folder,
            static_url_path=static_url_path,
            template_folder=template_folder,
            url_prefix=url_prefix,
            subdomain=subdomain,
            url_defaults=url_defaults,
            root_path=root_path,
        )
        self.wxcpt = WXBizMsgCrypt(token, encodingAESKey, cid)
        self.logger = logger or loguru.logger
        self.callbacks = []
        self.valid_args = ['content', 'toUserName', 'fromUserName', 'createTime', 'msgType', 'msgId', 'agentID',]

        self.add_url_rule('/', view_func=self._validation, methods=['GET'])
        self.add_url_rule('/', view_func=self._on_post, methods=['POST'])

    def _raise_for_ret_error(self, ret, msg):
        if ret != 0:
            self.logger.error(msg)
            abort(500)

    def _validation(self):
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        echostr = request.args.get('echostr', '')
        echostr = unquote(echostr, encoding='utf8')
        ret, echostr = self.wxcpt.VerifyURL(msg_signature, timestamp, nonce, echostr)
        self._raise_for_ret_error(ret, 'VerifyURL ret: ' + str(ret))
        return echostr

    def _on_post(self):
        msg_signature = request.args.get('msg_signature', '')
        timestamp = request.args.get('timestamp', '')
        nonce = request.args.get('nonce', '')
        reqData = request.get_data(cache=False, as_text=True)
        ret, xmlData = self.wxcpt.DecryptMsg(reqData, msg_signature, timestamp, nonce)
        self.logger.info('Receive message:\n' + str(xmlData))
        self._raise_for_ret_error(ret, 'DecryptMsg ret: ' + str(ret))

        xml_tree = ET.fromstring(xmlData)
        try:
            content = xml_tree.find('Content').text
            toUserName = xml_tree.find('ToUserName').text
            fromUserName = xml_tree.find('FromUserName').text
            createTime = xml_tree.find('CreateTime').text
            msgType = xml_tree.find('MsgType').text
            msgId = xml_tree.find('MsgId').text
            agentID = xml_tree.find('AgentID').text
        except AttributeError:
            self.logger.error(traceback.format_exc())
            abort(500)
            return '', 500

        for callback in self.callbacks:
            callback(
                content=content,
                toUserName=toUserName,
                fromUserName=fromUserName,
                createTime=createTime,
                msgType=msgType,
                msgId=msgId,
                agentID=agentID,
            )

        return '', 200

    def receive(self, func):
        def callback(**kwargs):
            func_args = inspect.signature(func).parameters
            valid_args = {arg: value for arg, value in kwargs.items() if arg in func_args}
            return func(**valid_args)
        self.callbacks.append(callback)
        return callback
