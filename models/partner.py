# -*- coding: utf-8 -*-

from odoo import models, fields, api


class partner(models.Model):
    _inherit='res.partner'
    sesion_ids=fields.Many2many('rnet.sesion','partner_sesion_rel', 'partner_id', 'sesion_id',string='sesiones')
    instructor=fields.Boolean(string='es instructor')
