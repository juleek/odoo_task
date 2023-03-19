from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Tags"
    _order = "name"

    name = fields.Char(required=True)
    color = fields.Integer()

