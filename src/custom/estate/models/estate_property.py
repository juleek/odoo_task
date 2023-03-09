from odoo import models, fields, api
from odoo.exceptions import MissingError


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Information about properties"

    name = fields.Char(required=True)
    active = fields.Boolean('Active', default=True)
    description = fields.Text()
    postcode = fields.Char()
    available_from = fields.Date(copy=False, default=lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')]
    )
    state = fields.Selection(
        selection=[('new', 'New'), ('offer received', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')]
    )
    property_type_id = fields.Many2one("estate.property.type")
    buyer = fields.Many2one("res.partner", string="Buyer")
    salesperson = fields.Many2one("res.users", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    total_area = fields.Integer(compute="_compute_total")
    @api.depends("garden_area", "living_area")
    def _compute_total(self):
        for elem in self:
            elem.total_area = elem.garden_area + elem.living_area

    best_offer = fields.Integer(default=0, compute="_compute_offer_price", store=True)
    @api.depends("offer_ids.price")
    def _compute_offer_price(self):
        self.best_offer = max(self.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    def sold_property(self):
        if self.state == "canceled":
            raise MissingError('Сanceled property cannot be sold')
        else:
            self.state = "sold"
        return True

    def cancel_property(self):
        if self.state == "sold":
            raise MissingError('Sold property cannot be canceled')
        else:
            self.state = "canceled"
        return True

