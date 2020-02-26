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

    @api.onchange('ruler_field')
    def onchange_method(self):

        if self.fields_type:
            self.fields_type = self.ruler_field.ttype

            if self.fields_type in ['selection', 'many2many', 'many2one']:

                self.many2many_value = False

                transient_ids = []

                if self.fields_type == 'selection':
                    ruler_model = self.ruler_model.model
                    ruler_field = self.ruler_field.name

                    selection_values = self.env[ruler_model]._fields[ruler_field].selection

                    for value in selection_values:
                        key_id = value[0]
                        name = value[1]

                        transient = self.env['transient.selection'].create(
                            {
                                'name': name,
                                'key_id': key_id,
                            }
                        )

                        transient_ids.append(transient.id)
                else:  # 'many2many', 'many2one'

                    ruler_model = self.ruler_field.relation  # esto es el modelo
                    records = self.env[ruler_model].search([])

                    for record in records:
                        transient = self.env['transient.selection'].create(
                            {
                                'name': record.name,
                                'model_id': record.id,
                            }
                        )

                        transient_ids.append(transient.id)

                return {'domain': {'many2many_value': [('id', 'in', transient_ids)]}}

    @api.multi
    def create_ruler(self):

        ruler = {
            'generator_id': self.ruler_generator_id,
            'ruler_model': self.ruler_model.id,
            'ruler_field': self.ruler_field.id,
            'ruler_type': self.ruler_type,
            'logical_operator': self.logical_operator.id,
            'fields_type': self.fields_type,
        }

        fields_type = self.fields_type

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

        ######################## Debug #################################
        import sys
        sys.path.append("/usr/lib/python2.7/debug/pydevd-pycharm.egg")
        import pydevd_pycharm
        pydevd_pycharm.settrace(
            '10.0.75.1',
            port=4020,
            stdoutToServer=True,
            stderrToServer=True,
        )
        ######################## Debug #################################

        context = self.env.context
        ruler_id = context.get('ruler_id', False)
        if context and context.get('ruler_operation', False) == 'add':
            self.env['rulers'].create(ruler)

        elif context and context.get('ruler_operation', False)== 'edit':
            self.env['rulers'].browse(ruler_id).write(ruler)




