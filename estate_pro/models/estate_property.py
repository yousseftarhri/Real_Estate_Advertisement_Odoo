from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstateProperty(models.Model):
    _name = "estate.property"
    _order = "id desc"
    _description = "Real Estate Property"

    name = fields.Char()
    stats = fields.Selection(
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )
    last_seen = fields.Datetime(default=fields.Datetime.now)
    status = fields.Boolean()
    property_type = fields.Many2one("estate.property.type")
    buyer = fields.Many2one("res.partner", string="Buyer")
    sales_man = fields.Many2one("res.users", string="Sales Man", default=lambda self: self.env.user)
    tag = fields.Many2many("estate.property.tag")
    offer = fields.One2many("estate.property.offer", "property")
    date_availability = fields.Datetime("Date availability", optional=True)
    living_area = fields.Integer("Living area")
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South')],
        help="Orientation is used to separate north and South")
    garden = fields.Boolean(string="garden")
    living_area = fields.Integer(string="Living Area")
    garden_area = fields.Integer(string="garden area")
    total_area = fields.Integer(string="total area", compute="_compute_total")

    best_price = fields.Float(string="best price", compute="_compute_sum")
    expected_price = fields.Float(string="Expected price")
    selling_price = fields.Float(string="Selling Price", readonly=True)

    @api.constrains('selling_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < record.expected_price*0.9:
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
        # all records passed the test, don't return anything


    _sql_constraints = [
        ('check_garden_area', 'CHECK(garden_area >= 0 AND garden_area <= 100)',
         'The garden of an analytic distribution should be between 0 and 100.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer.price")
    def _compute_sum(self):
        for record in self:
            # Ensure there are offers before computing the max price
            if record.offer:
                record.best_price = max(record.offer.mapped("price"))
            else:
                record.best_price = 0  # Default to 0 if there are no offers

    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = 10
        self.garden_orientation = "north"

    def cancel_property(self):
        if self.stats == "sold":
            raise UserError("The property is already sold and cannot be canceled")
        else:
            return self.write({"stats": "canceled"})

    def sold_property(self):
        if self.stats == "canceled":
            raise UserError("The property is already canceled and cannot be sold")
        else:
            return self.write({"stats": "sold"})

    @api.ondelete(at_uninstall=False)
    def _unlink_if_new_offer(self):
        if any(record.stats == "new" or record.stats == "canceled" for record in self):
            raise UserError("Can't delete new offer!")