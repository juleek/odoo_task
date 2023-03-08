from odoo import models, fields


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="partner_id", required=True)
    property_id = fields.Many2one("estate.property", string="property_id", required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )
