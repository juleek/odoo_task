import odoo
from odoo.http import request, route
import requests
import json
from dataclasses import dataclass
import sys
from werkzeug.wrappers import Response
import typing as t


# ======================================================================================================================
# Logging:

import logging
class ShutdownHandler(logging.Handler):
    def emit(self, record):
        print(record, file=sys.stderr)
        logging.shutdown()
        sys.exit(1)

logger = logging.getLogger()
logger.addHandler(ShutdownHandler(level=logging.CRITICAL))
logging.basicConfig(format='%(asctime)s %(levelname)s %(funcName)s:%(lineno)d: %(message)s')


# ======================================================================================================================
# Helpers:

@dataclass
class SendResult:
    """Represents status of sending a notification via Sender."""
    is_ok: bool
    http_code: int
    err_str: str


def try_sending(req: requests.Request, msg: str, bot_id) -> SendResult:
    prepared = req.prepare()

    response_received: bool = False
    MAX_RETRIES: int = 3
    logger.debug(f'About to send POST request of size {len(prepared.body) / 1024} KiB: request: Headers:{req.headers}')
    for i in range(MAX_RETRIES):
        try:
            with requests.Session() as s:
                response = s.send(prepared, timeout=(1, 19))

        except requests.ConnectTimeout:
            logger.debug(f"Connection timed out")
        except requests.ReadTimeout:
            logger.debug(f"Read timed out")
        except requests.Timeout:
            logger.debug(f"Request timed out")
        else:
            response_received = True
            logger.debug(f'Sent {msg} to: {bot_id}. Response status_code: {response.status_code}, data: {response.text}')
            break

    if not response_received:
        return SendResult(is_ok=False, http_code=0, err_str=f"Failed to send HTTP request: {req} {MAX_RETRIES} times")

    try:
        parsed_json = json.loads(response.text)
    except json.JSONDecodeError as exc:
        return SendResult(is_ok=False, http_code=response.status_code,
                                 err_str=f"Failed to decode JSON: {response.text}: details: {type(exc)}, {exc}")
    if 'ok' not in parsed_json:
        return SendResult(is_ok=False, http_code=response.status_code,
                                 err_str=f"'Ok' is not in JSON response: {parsed_json}")
    ok = parsed_json['ok']
    return SendResult(is_ok=ok, http_code=response.status_code, err_str="")


# # ======================================================================================================================
# # HTTP entry-point:

def get_chatid_from_json(d) -> t.Optional[int]:
    if 'message' in d:
        try:
            return d['message']['chat']['id']
        except:
            return None
    elif 'edited_message' in d:
        try:
            return d['edited_message']['chat']['id']
        except:
            return None
    else:
        return None

def get_tube_name(jsn):
    # Telegram Bot API responses are represented as JSON-objects. https://core.telegram.org/bots/api#message
    text: str = jsn['message']['text']
    # 'entities' is Array of MessageEntity. https://core.telegram.org/bots/api#messageentity
    command_type: str = jsn['message']['entities'][0]['type']
    if command_type == "bot_command" and (text == "/ambient" or text == "/bottom"):
        return text


def send_text(chat_id: int, text: str, bot_id: int):
    logger.info(f'{text} to bot_id: {bot_id}')
    url = f"https://api.telegram.org/bot{bot_id}/sendMessage"
    data = {'chat_id': chat_id, 'bot_id': bot_id, 'text': text}
    req = requests.Request('POST', url, data=data)
    result: SendResult = try_sending(req, "message", bot_id)
    logger.info(f"Result: {result}")
    return result


class MyController(odoo.http.Controller):
    @route('/odoo', auth='public', type='http', csrf=False)
    def handler(self):
        logger.info(f'Request = {request.httprequest.data}')
        jsn = json.loads(request.httprequest.data.decode("utf-8"))
        tube_name = get_tube_name(jsn)[1:]

        chat_id: int = get_chatid_from_json(jsn)

        measurements_model = request.env['measurements']
        temperatures = measurements_model.read_all_tempretarures(tube_name)

        bot_id: int = 0
        for record in request.env['telegram.bot'].search([]):
            bot_id = record.bot_id
        msg = f'Temperatures for {tube_name}: {temperatures}'
        send_text(chat_id, msg, bot_id)
        return Response("OK", status=200)
