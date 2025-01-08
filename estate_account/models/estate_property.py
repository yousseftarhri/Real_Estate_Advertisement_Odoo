from odoo import api, models, Command



class EstateProperty(models.Model):
    _inherit = 'estate.property'

    def sold_property(self):

        for prop in self:
            invoice_vals = {
                'move_type': 'out_invoice',
                'partner_id': prop.buyer.id,
                #'journal_id': journal.id,  # company comes from the journal
                "invoice_line_ids": [
                    Command.create({
                        "name": prop.name,
                        "quantity": 1.0,
                        "price_unit": prop.selling_price * 6.0 / 100.0,
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1.0,
                        "price_unit": 100.0,
                    }),
                ]
            }
            self.env["account.move"].create(invoice_vals)


        return super().sold_property()
