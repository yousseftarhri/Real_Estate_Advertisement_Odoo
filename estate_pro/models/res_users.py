from odoo import models, fields, api


class ResUsers(models.Model):
    _inherit = "res.users"
    _description = "Real Estate Property users"

    property_ids = fields.One2many("estate.property", "sales_man", domain=[("stats", "in", ["new", "offer_received"])])