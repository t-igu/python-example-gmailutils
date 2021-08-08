import pickle
import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Gmail APIのスコープを設定
SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/gmail.readonly',
]

class EasyGmailConnect:
    def __init__(self, creds_path, token_path):
        """
        # 初期処理
        """
        self.__creds_path = creds_path
        self.__token_path = token_path
        self.__service = self.__build_service()
    def __build_service(self):
        """
        # Gmail APIのサービスオブジェクトを構築
        """
        creds = self.__get_credential()
        self.service = build('gmail', 'v1', credentials=creds)
    def __get_credential(self):
        """
        # 認証認可情報を取得する
        """
        creds = None
        if os.path.exists(self.__token_path):
            with open(self.__token_path, "rb") as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.__creds_path, SCOPES)
                # creds = flow.run_local_server()
                creds = flow.run_console()
            with open(self.__token_path, "wb") as token:
                pickle.dump(creds, token)
        return creds
