from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Information about properties type"

    name = fields.Char(required=True)
