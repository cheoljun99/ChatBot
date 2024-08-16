import datetime
import ssl
import asyncio
import logging
import os
import json
import subprocess
from threading import Event
import requests
from slack_sdk.web import WebClient
from slack_sdk.socket_mode import SocketModeClient
from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest
from requests.packages.urllib3.exceptions import InsecureRequestWarning # pylint: disable=import-error
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from config import conf
import re
from vt import virustotal  # vt.py에 있는 virustotal 함수 가져옴
from urlscanio import urlscan_query  # urlscan.py에 있는 urlscan_query 함수 가져옴

##############################################
from crud import get_bobwiki_data_in_db
from sqlalchemy.orm import Session
from database import db  # db 세션 가져오기
##############################################



ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

BOT_TOKEN = conf['bot_token']
SOCKET_TOKEN = conf['bot_socket']
BOTNAME = 'bot'

ALLOW_USERS = ['U05K140HSUQ','']

SLACK_CLIENT = SocketModeClient(
    # This app-level token will be used only for establishing a connection
    app_token=SOCKET_TOKEN,  # xapp-A111-222-xyz
    # You will be using this AsyncWebClient for performing Web API calls in listeners
    web_client=WebClient(token=BOT_TOKEN, ssl=ssl_context)  # xoxb-111-222-xyz
)

from slack_sdk.socket_mode.response import SocketModeResponse
from slack_sdk.socket_mode.request import SocketModeRequest

def process(client: SocketModeClient, req: SocketModeRequest):
    if req.type == "events_api":
        # Acknowledge the request anyway
        response = SocketModeResponse(envelope_id=req.envelope_id)
        client.send_socket_mode_response(response)

        
        # Add a reaction to the message if it's a new message
        event = req.payload["event"]

        # 메시지가 봇에서 보낸 것인지 사용자가 보낸 것인지 확인
        if event["type"] == "message" and event.get("subtype") is None:
            if "bot_id" in event:
                # 봇이 보낸 메시지일 경우, "loudspeaker" 이모지를 추가
                client.web_client.reactions_add(
                    name="loudspeaker",
                    channel=event["channel"],
                    timestamp=event["ts"],
                )
            else:
                # 사용자가 보낸 메시지일 경우, "eyes" 이모지를 추가
                client.web_client.reactions_add(
                    name="eyes",
                    channel=event["channel"],
                    timestamp=event["ts"],
                )

        if req.payload["event"]["type"] == "message" \
            and req.payload["event"].get("subtype") is None:
            text = req.payload["event"]["text"]
            channel = req.payload["event"]["channel"]

            # "ioc" 단어를 찾고 그 뒤의 값을 파싱 # ioc 키워드를 처리하는 로직
            match_ioc  = re.search(r'\bioc\s+([^\s]+)', text)
            if match_ioc :
                query_item = match_ioc.group(1)
                query_type = None

                # IP인지 URL인지 확인
                if re.match(r'\b\d{1,3}(\.\d{1,3}){3}\b', query_item):
                    query_type = 'ip'
                elif re.match(r'https?://', query_item) or re.match(r'<https?://', query_item)or re.match(r'http?://', query_item)or re.match(r'<http?://', query_item):
                    # 슬랙에서 URL이 < >로 감싸져 있을 경우를 처리
                    query_type = 'url'
                    query_item = query_item.strip('<>')
                    # 도메인 문자열에서 | 이후의 부분 추출
                    if '|' in query_item:
                        query_item = query_item.split('|')[1]
                        if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', query_item):
                            query_type = 'domain'


                if query_type:
                    # virustotal 함수로 질의
                    result = virustotal(query_item, query_type)
                    urlscan_result = None

                    if query_type in ['ip','url', 'domain']:
                        urlscan_result = urlscan_query(query_item)

                    print(urlscan_result)

                    message_text = f"VirusTotal 분석 결과: {result}"
                    if urlscan_result:
                        message_text += f"\nURLScanio 분석 결과: {urlscan_result}"

                    # 결과를 슬랙 채널에 전송
                    client.web_client.chat_postMessage(
                        channel=channel,
                        text=message_text
                    )
                else:
                    client.web_client.chat_postMessage(
                        channel=channel,
                        text="IP, URL 또는 도메인이 아닌 값을 입력하셨습니다."
                    )

            # bob 키워드를 처리하는 새로운 로직
            match_bob = re.search(r'\bbob\s+([^\s]+)', text, re.IGNORECASE)
            if match_bob:
                name = match_bob.group(1)

                print(name)

                # 세션을 수동으로 관리 (제너레이터에서 세션을 가져오기)
                session = next(db.get_session())

                try:
                    bobwiki_data = get_bobwiki_data_in_db(name, session)
                finally:
                    session.close()


                if bobwiki_data:
                    message_text = f"이름: {bobwiki_data.name}\n직책: {bobwiki_data.role}\n정보: {bobwiki_data.info}"
                else:
                    message_text = f"'{name}'에 대한 데이터를 찾을 수 없습니다."

                client.web_client.chat_postMessage(
                    channel=channel,
                    text=message_text
                )

        
    if req.type == "interactive" \
        and req.payload.get("type") == "shortcut":
        if req.payload["callback_id"] == "hello-shortcut":
            # Acknowledge the request
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)
            # Open a welcome modal
            client.web_client.views_open(
                trigger_id=req.payload["trigger_id"],
                view={
                    "type": "modal",
                    "callback_id": "hello-modal",
                    "title": {
                        "type": "plain_text",
                        "text": "Greetings!"
                    },
                    "submit": {
                        "type": "plain_text",
                        "text": "Good Bye"
                    },
                    "blocks": [
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": "Hello!"
                            }
                        }
                    ]
                }
            )

    if req.type == "interactive" \
        and req.payload.get("type") == "view_submission":
        if req.payload["view"]["callback_id"] == "hello-modal":
            # Acknowledge the request and close the modal
            response = SocketModeResponse(envelope_id=req.envelope_id)
            client.send_socket_mode_response(response)

if __name__ == "__main__":
    try:
        #rtm.start()
        # Add a new listener to receive messages from Slack
        # You can add more listeners like this
        SLACK_CLIENT.socket_mode_request_listeners.append(process)
        # Establish a WebSocket connection to the Socket Mode servers
        SLACK_CLIENT.connect()
        # Just not to stop this process
        Event().wait()
    except Exception as main_e:
        error = str(main_e)
        logging.warning('main func: %s', error)