from odoo import models, fields, api




class Offer(models.Model):
    _name = 'realtor.offer'
    _order = "price desc, id"
    appartement_id = fields.Many2one('realtor.appartement', string='Appartement', required=True)
    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)
    price = fields.Float(string='Price', required=True)

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price < record.appartement_id.price * 0.9:
                raise models.ValidationError('The price must be at least 90% of the expected price')
    