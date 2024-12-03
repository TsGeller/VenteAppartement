import time
from odoo import models, fields, api
from datetime import timedelta



class Appartement(models.Model):
    _name = 'realtor.appartement'
    

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    picture = fields.Binary(string='Picture')
    disponible_date = fields.Date(string='Disponible date', required=True)
    price = fields.Float(string='Price', required=True)
    surface = fields.Integer(string='Surface', required=True)
    garden_surface =    fields.Integer(string='Garden surface')
    total_surface = fields.Integer(string='Total surface', compute='_compute_total_surface',readonly=True)
    buyer_name =  fields.Many2one('res.partner', string='Buyer',compute='_compute_buyer_name',readonly=True)
    best_offer_ids = fields.One2many('realtor.offer', 'appartement_id', string='Offers')
    product_id = fields.One2many('product.template','appartement_id', string='Product')

    
    @api.depends('buyer_name')
    def _compute_buyer_name(self):
        for record in self:
            if record.best_offer_ids:                
                record.buyer_name = record.best_offer_ids[0].buyer_id
            else:
                record.buyer_name = None
    

    
    
    
    @api.depends('surface', 'garden_surface')
    def _compute_total_surface(self):
        for record in self:
            record.total_surface = record.surface + record.garden_surface

    
    @api.constrains('disponible_date')
    def _check_disponible_date(self):
        for record in self:
            if record.disponible_date < fields.date.today()+ timedelta(days=90):
                raise models.ValidationError('The date of disponibility must be greater than 3 months')
    

    @api.constrains('surface')
    def _check_surface(self):
        for record in self:
            if record.surface < 0:
                raise models.ValidationError('The surface must be greater or equals to 0')

    @api.constrains('garden_surface')
    def _check_garden_surface(self):
        for record in self:
            if record.garden_surface <= 0:
                raise models.ValidationError('The surface of the garden must be greater or equals to 0')

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise models.ValidationError('The price must be greater than 0')
                
   

                
        



