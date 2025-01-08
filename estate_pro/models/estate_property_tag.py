from odoo import fields, models

class PropertyTag(models.Model):
    _name = "estate.property.tag"
    _order = "name desc"
    _description = "Real Estate Property Tags"

    name = fields.Char()
    color = fields.Integer("Color Index")

    _sql_constraints = [
        ('check_unique_tag', 'UNIQUE(name)',
         'The tag must be unique')
    ]