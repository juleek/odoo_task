from odoo import models, fields, api

class Measurements(models.Model):
    _name = "measurements"
    _description = "Storing temperature"

    temperature = fields.Integer()
    date = fields.Date()
    tube_name = fields.Selection(
        selection=[('ambient', 'Ambient'), ('bottom', 'Bottom Tube')]
    )

    @api.model
    def read_all_tempretarures(self, for_tube):
        domain = [('tube_name', '=', for_tube)]
        temperatures = self.search(domain)

        result = []
        for temp in temperatures:
            result.append(temp.temperature)
        return result
