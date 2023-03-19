from odoo import models, fields, api

class Measurements(models.Model):
    _name = "measurements"
    _description = "Storing temperature"

    temperature = fields.Integer()
    date = fields.Date()
    tube_name = fields.Selection(
        selection=[('ambient', 'Ambient'), ('bottom', 'Bottom Tube')]
    )




