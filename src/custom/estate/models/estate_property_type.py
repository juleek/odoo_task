from odoo import models, fields


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Information about properties type"
    _order = "name"

    # sequence = fields.Integer('Sequence')
    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
