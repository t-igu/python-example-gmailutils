import os
from .easygmail_connect import EasyGmailConnect
import base64
import urllib.parse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class EasyGmailSend(EasyGmailConnect):
    # ********************************************************************************
    # メール送信
    # ********************************************************************************
    def send_message(
            self, sender, to, subject, message_text, 
            mime_type="plain", cc=None, filepath_list=None, user_id='me'
        ):
        message = self.create_message(
            mime_type=mime_type,
            sender=sender,
            to=to,
            cc=cc,
            subject=subject,
            message_text=message_text,
            filepath_list = filepath_list
        )
        ret = (self.service.users().messages().send(userId=user_id, body=message).execute())
        return ret

    def create_message(self, mime_type, sender, to, cc, subject, message_text, filepath_list):
        msg = MIMEMultipart()
        if filepath_list:
            for path in filepath_list:
                with open(path, "rb") as f:
                    part = MIMEApplication(
                        f.read(),
                        Name=os.path.basename(path)
                    )
                part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(path)
                msg.attach(part)
        msg['to'] = to
        msg['from'] = sender
        msg['subject'] = subject
        if cc:
            msg["Cc"] = cc
        body = MIMEText(message_text, mime_type)
        msg.attach(body)
        encode_message = base64.urlsafe_b64encode(msg.as_bytes())
        return {'raw': encode_message.decode()}
