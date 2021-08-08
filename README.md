
This software is released under the MIT License, see LICENSE

## setup

```bash
python setup.py develop
```

## Usage:

### Example for get gmail messages.

```python:example.py
import pprint
from gmailutils import EasyGmail

gmail_creds_path="./settings/google.apps.credentials.json"
gmail_token_path="./settings/saved_auth_token.pikle"

gmail = EasyGmail(gmail_creds_path, gmail_token_path)

sender = "example@gmail.com"
to = "example_to@gmail.com"
cc = "example_cc1@gmail.com, example_cc2@gmail.com"

query = f"after:2021/7/30 from:{sender}"
messages = gmail.list_message(query)
for message in messages:
    print(message)
```

### Example for send gmail message.

```python:example.py

message = gmail.send_message(
    sender = sender, 
    to = to,
    subject = '[テスト]pythonで送信するテストメール',
    message_text = "本文",
)

```

### This is a sample to send the text in html.

```python:example.py

message = gmail.send_message(
    sender = sender, 
    to = to,
    subject = '[テスト]pythonで送信するテストメール(html)',
    message_text = "<h1>本文</h1>",
    mime_type ="html",
)
```

### Example for send gmail message with attachement.

```python:example.py

    gmail.send_message(
        sender = sender, 
        to = to,
        cc = cc,
        subject = '[テスト]pythonで送信するテストメール',
        message_text = """
お疲れ様です。これはテストです。
受信した方はこのメールを削除してください。
""",
        filepath_list = ['aaa.xlsx', 'あいうえお.csv']
    )
```
