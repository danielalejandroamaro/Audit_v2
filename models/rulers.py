# -*- coding: utf-8 -*-

from openerp import models, fields, api


class Rulers(models.Model):
    _name = 'rulers'
    _description = 'Rulers'
    _order = 'sequence'

    """
    En el campo name estará la estructura que se mostrará al usuario 
    en forma de texto com:
    Del modelo: "X", el campo: "Y", es igual a el valor: "Z"
    
    TODO: hay que implementar una opción para permitir 
    comparar dos campos de modelos ejemplo:

    """
    sequence = fields.Integer(
        string='Secuencia',
        default=0,
        required=True,
    )

    name = fields.Char(
        string='Name',
        required=True,
    )

    description = fields.Text(
        string="Descripción",
        required=False,
    )

    ruler_generator_id = fields.Many2one(
        comodel_name='rulers.generator',
        string='Rulers Generator id',
        required=True,
        ondelete='cascade',
    )

    ruler_type = fields.Selection(
        string='Rule_type',
        selection=[('ruler', 'Regla'),
                   ('operator', 'Operador'), ],
        required=True,
    )

    fields_type = fields.Char(
        compute='_compute_fields_type',
        store=True,
    )

    ruler_model = fields.Many2one(
        comodel_name='ir.model',
        # string='Rule_model',
        required=True
    )

    ruler_field = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Rule_field',
        required=True,
    )

    logical_operator = fields.Many2one(
        comodel_name='logical.operators',
        string='logical_operator',
        required=True
    )

    date_value = fields.Date(
        string='Date',
        required=False,
    )

    date_time_value = fields.Datetime(
        string='Date_time_value',
        required=False,
    )

    integer_value = fields.Integer(
        string='integer_value',
        required=False,
    )

    bool_value = fields.Boolean(
        string='Bool_value',
        required=False,
    )

    char_value = fields.Char(
        string='Char_value',
        required=False,
    )

    float_value = fields.Float(
        string='Float_value',
        required=False,
    )

    # este campo es para los many2one, many2many y selection
    many2many_value = fields.Many2many(
        comodel_name='transient.selection',
        string='Many2many_value',
    )

    @api.multi
    def edit(self):

        fields_type = self.fields_type

        context = {
            'default_name': self.name,
            'default_ruler_generator_id': self.ruler_generator_id.id,
            'default_ruler_model': self.ruler_model.id,
            'default_ruler_field': self.ruler_field.id,
            'default_ruler_type': self.ruler_type,
            'default_logical_operator': self.logical_operator.id,
            'ruler_operation': 'edit',
            'ruler_id': self.id,
        }

        if fields_type == 'date':
            context['default_date_value'] = self.date_value

        elif fields_type == 'datetime':
            context
        elif fields_type == 'integer':
            context['default_integer_value'] = self.integer_value

        elif fields_type == 'boolean':
            context['default_bool_value'] = self.bool_value

        elif fields_type == 'char':
            context['default_char_value'] = self.char_value

        elif fields_type in ['float', 'monetary']:
            context['default_float_value'] = self.float_value

        elif fields_type in ['many2many', 'many2one']:
            context['default_many2many_value'] = self.many2many_value

        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ruler.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': context,
            'nodestroy': True,
        }


class TransientSelection(models.TransientModel):
    _name = 'transient.selection'
    _description = 'Transient Selection'

    name = fields.Char(
        string='Nombre',
    )

    model_id = fields.Integer(
        string='Model_id',
        required=False,
    )

    key_id = fields.Char(
        string='Key_id',
        required=False,
    )
