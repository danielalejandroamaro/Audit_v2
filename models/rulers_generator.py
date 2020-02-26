# -*- coding: utf-8 -*-

from openerp import models, fields, api


class RulersGenerator(models.Model):
    _name = 'rulers.generator'
    _description = 'Rulers Generator'

    name = fields.Char(
        string='Nombre',
        required=False,
    )

    description = fields.Text(
        string="Descripción",
        required=False,
    )

    rulers = fields.One2many(
        comodel_name='rulers',
        inverse_name='ruler_generator_id',
        string='Reglas',
        required=False,
    )

    @api.multi
    def add_ruler(self):
        return {
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'ruler.wizard',
            'type': 'ir.actions.act_window',
            'target': 'new',
            'context': {
                'default_ruler_generator_id': self.id,
                'default_ruler_type': 'ruler',
                'ruler_operation': 'add'
            },
            'nodestroy': True,
        }

    @api.multi
    def add_operator(self):
        pass
