import odoo
from odoo.http import request, route
import datetime
from ..models import measurements as mes
from ..models import bot
import requests
import json

#
# # ======================================================================================================================
# # Logging:
#
# import logging
# class ShutdownHandler(logging.Handler):
#     def emit(self, record):
#         print(record, file=sys.stderr)
#         logging.shutdown()
#         sys.exit(1)
#
# logger = logging.getLogger()
# logger.addHandler(ShutdownHandler(level=logging.CRITICAL))
# logging.basicConfig(format='%(asctime)s %(levelname)s %(funcName)s:%(lineno)d: %(message)s')
#
#
# # ======================================================================================================================
# # Helpers:
#
# from dataclasses import dataclass
# import sys
#
#
# @dataclass
# class SendResult:
#     """Represents status of sending a notification via Sender."""
#     is_ok: bool
#     http_code: int
#     err_str: str
#
#
# def try_sending(req: request.Request, msg: str, bot_id) -> SendResult:
#     prepared = req.prepare()
#
#     response_received: bool = False
#     MAX_RETRIES: int = 3
#     logger.debug(f'About to send POST request of size {len(prepared.body) / 1024} KiB: request: Headers:{req.headers}')
#     for i in range(MAX_RETRIES):
#         try:
#             with requests.Session() as s:
#                 response = s.send(prepared, timeout=(1, 19))
#
#         except requests.ConnectTimeout:
#             logger.debug(f"Connection timed out")
#         except requests.ReadTimeout:
#             logger.debug(f"Read timed out")
#         except requests.Timeout:
#             logger.debug(f"Request timed out")
#         else:
#             response_received = True
#             logger.debug(f'Sent {msg} to: {bot_id}. Response status_code: {response.status_code}, data: {response.text}')
#             break
#
#     if not response_received:
#         return SendResult(is_ok=False, http_code=0, err_str=f"Failed to send HTTP request: {req} {MAX_RETRIES} times")
#
#     try:
#         parsed_json = json.loads(response.text)
#     except json.JSONDecodeError as exc:
#         return SendResult(is_ok=False, http_code=response.status_code,
#                                  err_str=f"Failed to decode JSON: {response.text}: details: {type(exc)}, {exc}")
#     if 'ok' not in parsed_json:
#         return SendResult(is_ok=False, http_code=response.status_code,
#                                  err_str=f"'Ok' is not in JSON response: {parsed_json}")
#     ok = parsed_json['ok']
#     return SendResult(is_ok=ok, http_code=response.status_code,
#                              err_str="")
#
#
# # ======================================================================================================================
# # HTTP entry-point:
#
class MyController(odoo.http.Controller):
    @route('/odoo', auth='public', type='http')
    def handler(self):
        # temperature = mes.Measurements.temperature
        print(f'req = {request.httprequest}')
#         jsn = json.loads(request.httprequest.data)
#         print(f'jsn = {jsn}')
#         temperature = mes.Measurements.temperature
#         date = mes.Measurements.date
#         text: str = create_msg(temperature, date)
#         bot_id: int = bot.TelegramBot.bot_id
#         return 'OK'
#
# def create_msg(temperature: int, date: datetime.date) -> str:
#     return f'The last measurument of temperature was on {date}: {temperature}'
#
#
# def send_text(text: str, bot_id: int):
#     logger.info(f'text: {text}')
#     url = f"https://api.telegram.org/bot{bot_id}/sendMessage"
#     data = {'bot_id': bot_id, 'text': text}
#     req = requests.Request('POST', url, data=data)
#     result: SendResult = try_sending(req, "message", bot_id)
#     logger.info(f"Result: {result}")
#     return result

