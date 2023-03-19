from odoo import models, fields

class TelegramBot(models.Model):
    _name = "telegram.bot"
    _description = "Bot ID"

    bot_id = fields.Char()
    name = fields.Char()
