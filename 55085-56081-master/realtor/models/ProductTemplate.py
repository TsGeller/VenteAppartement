from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'
    appartement_id =fields.Many2one('realtor.appartement',string='Appartement') 
   
    

