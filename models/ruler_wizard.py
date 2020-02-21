# -*- coding: utf-8 -*-
from openerp import models, fields, api

# class RulerWizard(models.TransientModel):
#     _name = 'ruler.wizard'
#     _description = 'Ruler Wizard'
#     _inherit = 'rulers'
#
#     @api.depends('ruler_field')
#     def _compute_fields_type(self):
#         if self.ruler_field:
#             self.fields_type = self.ruler_field.ttype
#
#     @api.onchange('ruler_field')
#     def onchange_method(self):
#
#         self.fields_type = self.ruler_field.ttype
#
#         if self.fields_type in ['selection', 'many2many', 'many2one']:
#             self.many2many_value = False
#
#             transient_ids = []
#
#             if self.fields_type == 'selection':
#                 ruler_model = self.ruler_model.model
#                 ruler_field = self.ruler_field.name
#
#                 selection_values = self.env[ruler_model]._fields[ruler_field].selection
#
#                 for value in selection_values:
#                     key_id = value[0]
#                     name = value[1]
#
#                     transient = self.env['transient_selection'].create(
#                         {
#                             'name': name,
#                             'key_id': key_id,
#                         }
#                     )
#
#                     transient_ids.append(transient.id)
#             else:
#
#                 model_id = self.ruler_field.relation  # esto es el modelo
#                 records = self.env[model_id].search([])
#
#                 for record in records:
#                     transient = self.env['transient_selection'].create(
#                         {
#                             'name': record.name,
#                             'model_id': record.id,
#                         }
#                     )
#
#                     transient_ids.append(transient.id)
#
#             return {'domain': {'many2many_value': [('id', 'in', transient_ids)]}}
#
#     @api.multi
#     def create_ruler(self):
#
#         context = self.env.context
#         ruler_generator_id = self.ruler_generator_id
#
#         if context and ruler_generator_id:
#             self.env['rulers'].create({
#                 'name': "Temp Name!!",
#                 'generator_id': ruler_generator_id,
#                 'ruler_model': self.ruler_model.id,
#                 'ruler_field': self.ruler_field.id,
#                 'logical_operator': self.logical_operator.id,
#                 'fields_type': self.fields_type,
#                 'date_value': self.date_value,
#                 'integer_value': self.integer_value,
#                 'bool_value': self.bool_value,
#                 'char_value': self.char_value,
#                 'float_value': self.float_value,
#                 'many2many_value': self.many2many_value,
#             })
#             return True
#         return False

