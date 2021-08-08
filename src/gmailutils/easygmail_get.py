import os
from .easygmail_connect import EasyGmailConnect
import base64
import html2text
import email
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from enum import Enum

import datetime
from pytz import timezone
from dateutil import parser

custom_header_columns = [
    'Subject',
    'To',
    'From',
    'Date',
    'Cc',
    'Bcc',
    'Content-Type',
]

class EasyGmailGet(EasyGmailConnect):
    def list_message(self, query, max_count=100):
        """
        メッセージを検索する
        """
        messages = []
        message_ids = (
            self.service.users().messages()
            .list(userId='me', maxResults=max_count, q=query).execute()
        )
        if message_ids["resultSizeEstimate"] == 0:
            return []
        for message_id in message_ids['messages']:
            message = self.detail_message(message_id['id'])
            messages.append(message)
        return messages
    def detail_message(self, message_id):
        """
        メッセージ詳細を取得する
        """
        detail_msg = (
            self.service.users().messages()
            .get(userId="me", id=message_id, format="full").execute()
        )
        ret = self.decode_message(detail_msg)
        return ret
    def decode_message(self, message):
        """
        # メッセージを編集する
        """
        customed_message = {}
        customed_message['id'] = message['id']
        customed_message['threadId'] = message['threadId']
        headers = message['payload']['headers']
        for header in headers:
            if header['name'] in custom_header_columns:
                customed_message[header['name']] = header['value']
        customed_message['attachments']=[]
        if message['payload']['body']['size'] > 0:
            decoded_message = self.__convert_message(message['id'], message['payload'])
            if decoded_message['Content-Type'].startswith('text/html'):
                customed_message['body_html'] = decoded_message['body']['data']
                plain_text = html2text.html2text(decoded_message['body']['data'])
                customed_message['body_text'] = plain_text
            else:
                customed_message['body_text'] = decoded_message['body']['data']
        else:
            # multipartの場合
            if 'parts' in message['payload'].keys():
                for part in message['payload']['parts']:
                    decoded_message = self.__convert_message(message['id'], part)
                    customed_message['attachments'].append(decoded_message)
                    if not part['filename']:
                        customed_message['Content-Type'] = decoded_message['Content-Type']
                        if decoded_message['Content-Type'].startswith('text/html'):
                            customed_message['body_html'] = decoded_message['body']['data']
                            plain_text = html2text.html2text(decoded_message['body']['data'])
                            customed_message['body_text'] = plain_text
                        else:
                            customed_message['body_text'] = decoded_message['body']['data']
        return customed_message
    # ********************************************************************************
    # メッセージを編集する
    # ********************************************************************************
    def __convert_message(self, id, part):
        ret = {}
        ret['filename'] = part['filename']
        ret['body']= {}
        for header in part['headers']:
            if header['name'] in custom_header_columns:
                ret[header['name']] = header['value']
        if part['filename']:
            if 'data' in part['body']:
                data = part['body']['data']
            else:
                # bodyにデータが入っていないケースは、Gmailの添付ファイルを取得する。
                att_id = part['body']['attachmentId']
                att = self.service.users().messages().attachments().get(userId='me', messageId=id, id=att_id).execute()
                data = att['data']
            # encodeされたファイルをdecodeする
            decoded_data = base64.urlsafe_b64decode(data.encode('UTF-8'))
        else:
            decoded_data = email.message_from_string(str(base64.urlsafe_b64decode(part['body']['data']), "utf-8")).get_payload()
        ret['body']['data'] = decoded_data
        return ret
