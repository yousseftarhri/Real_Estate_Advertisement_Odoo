from odoo import models, fields, api


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _order = "name desc"
    _description = "Real Estate Property Type"

    name = fields.Char()
    property_ids = fields.One2many("estate.property", "property_type")
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    offer_ids = fields.One2many("estate.property.offer", "property_type_id")

    offer_count = fields.Integer(compute="_compute_offers")

    @api.depends("offer_ids")
    def _compute_offers(self):
        for record in self:
            record.offer_count = len(record.offer_ids)

    def action_get_offers(self):
        self.ensure_one()
        return 1