from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.tools import float_compare


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _order = "price desc"
    _description = "Real Estate Property offers"

    price = fields.Float(string="price")
    property = fields.Many2one("estate.property", string="Property")
    partner = fields.Many2one("res.partner", string="Partner")
    stats = fields.Char(string="Status", readonly=True)
    property_type_id = fields.Many2one(related="property.property_type", store=True, string="property type")

    def action_confirm(self):
        if "Accept" in self.mapped("property.offer.stats"):
            raise UserError("An offer as already been accepted.")

        self.write(
            {
                "stats": "Accept",
            }
        )
        return self.mapped("property").write(
            {
                "stats": "sold",
                "selling_price": self.price,
                "buyer": self.partner.id,
            }
        )

    def action_cancel(self):
        self.write(
            {
                "stats": "Refuse",
            })

    @api.model
    def create(self, vals):
        if vals.get("property") and vals.get("price"):
            prop = self.env["estate.property"].browse(vals["property"])
            # We check if the offer is higher than the existing offers
            if prop.offer:
                max_offer = max(prop.mapped("offer.price"))
                if float_compare(vals["price"], max_offer, precision_rounding=0.01) <= 0:
                    raise UserError("The offer must be higher than %.2f" % max_offer)
            prop.stats = "offer_received"
        return super().create(vals)


