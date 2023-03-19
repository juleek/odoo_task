from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offers"
    _order = "price desc"

    price = fields.Float()
    partner_id = fields.Many2one("res.partner", string="partner_id", required=True)
    property_id = fields.Many2one("estate.property", string="property_id", required=True)
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    _sql_constraints = [
        ('price', 'CHECK(price >= 0)', 'The price should be positive.')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            curr_date = record.create_date.date() if record.create_date else fields.Date.today()
            record.date_deadline = curr_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            time_diff = self.date_deadline - fields.Date.today()
            record.validity = time_diff.days

    def offer_accepted(self):
        for rec in self.env[self._name].search([]):
            rec.status = "refused"
        self.status = "accepted"
        self.property_id.buyer = self.partner_id
        self.property_id.selling_price = self.price


    def offer_refused(self):
        self.status = "refused"
        self.property_id.buyer = False
        self.property_id.selling_price = 0
