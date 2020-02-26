# -*- coding: utf-8 -*-
from openerp import models, fields, api


class RulerWizard(models.TransientModel):
    _name = 'ruler.wizard'
    _description = 'Ruler Wizard'
    _inherit = 'rulers'

    @api.depends('ruler_field')
    def _compute_fields_type(self):
        if self.ruler_field:
            self.fields_type = self.ruler_field.ttype

    def __set_transient_selection_env(self, name, key_id):
        return self.env[
            'transient.selection'
            ].create(
                {
                    'name': name,
                    'key_id': key_id,
                }
            )

    def create_select(self, ruler_model , ruler_field):
        selection_values = self.env[ruler_model]._fields[ruler_field].selection
        transient_ids = [
            self.__set_transient_selection_env(name,key_id) for key_id,name value in selection_values:
        ]
        return {'domain': {'many2many_value': [('id', 'in', transient_ids)]}}

    def create_relation(self,ruler_model):
        records = self.env[ruler_model].search([])
        transient_ids = [
            self.__set_transient_selection_env(record.name , record.id)
            for record in records:
        ]
        return {'domain': {'many2many_value': [('id', 'in', transient_ids)]}}

    @api.onchange('ruler_field')
    def onchange_method(self):
        if self.fields_type:
            self.fields_type = self.ruler_field.ttype
            
            if self.fields_type not in ['selection','many2many', 'many2one']:
                return {'domain': {'many2many_value': [('id', 'in', [])]}}

            self.many2many_value = False
            if self.fields_type == 'selection':
                return self.create_using_select( self.ruler_model.model, self.ruler_field.name)

            if self.fields_type in ['many2many', 'many2one']:
               return self.create_relation(self.ruler_field.relation)


    @api.multi
    def create_ruler(self):

        context = self.env.context
        ruler_generator_id = self.ruler_generator_id

        fields_type = self.fields_type

        ruler = {
            'generator_id': ruler_generator_id,
            'ruler_model': self.ruler_model.id,
            'ruler_field': self.ruler_field.id,
            'ruler_type': self.ruler_type,
            'logical_operator': self.logical_operator.id,
            'fields_type': self.fields_type,
        }

        if context and ruler_generator_id:
            if fields_type == 'date':
                ruler['date_value'] = self.date_value
                selected_value = self.date_value

            elif fields_type == 'datetime':
                ruler['datetime'] = self.date_time_value
                selected_value = self.date_time_value

            elif fields_type == 'integer':
                ruler['integer_value'] = str(self.integer_value)
                selected_value = str(self.integer_value)

            elif fields_type == 'boolean':
                ruler['bool_value'] = self.bool_value

                if fields_type == "True":
                    selected_value = "Verdadero"
                else:
                    selected_value = "Falso"

            elif fields_type == 'char':
                ruler['char_value'] = self.char_value
                selected_value = self.char_value

            elif fields_type in ['float', 'monetary']:
                ruler['float_value'] = str(self.float_value)
                selected_value = str(self.float_value)

            elif fields_type in [' many2many', 'many2one']:
                ruler['many2many_value'] = str(self.many2many_value)
                selected_value = self.many2many_value.name

            else:
                return False

            name = "Del el Modelo: " + self.ruler_model.name + \
                   ", El campo: " + self.ruler_field.name + \
                   " " + self.logical_operator.name + \
                   " " + selected_value

            ruler['name'] = name

            self.env['rulers'].create(ruler)
