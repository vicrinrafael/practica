# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions

class Curso(models.Model):
    _name='rnet.curso'

    name=fields.Char(String='Nombre del curso',required=True,size=50)
    descripcion=fields.Text(String='descripcion')
    responsable_id= fields.Many2one('res.users',
        ondelete='set null', string='Responsable', index=True)
    sesion_ids= fields.One2many('rnet.sesion','curso_id', string='Sesiones')

    _sql_constraints = [
    ('verificar_nombre_descripcion',
    'CHECK(name !=descripcion)',
    'El nombre de un curso no debe ser su descripcion '),

    ('nombre_unico',
    'UNIQUE(name)',
    'El nombre del curso debe ser unico',)

    ]


class Sesion(models.Model):
    _name='rnet.sesion'

    name= fields.Char(string='Nombre', required=True, default='/')
    inicio= fields.Date(default=lambda self:fields.Date.today())
    duracion= fields.Float(string='Duracion', digits=(6,2), help='Duracion en días')
    asientos= fields.Integer(string='Asientos')
    instructor_id=fields.Many2one('res.partner',string='Instructor',
    domain=[('instructor','=', True)])
    curso_id= fields.Many2one('rnet.curso', ondelete='cascade', string='Curso', required=True)
    asistentes_ids= fields.Many2many('res.partner', 'partner_sesion_rel', 'sesion_id', 'partner_id',string='Asistentes')
    asientosReservados=fields.Float(string='Asientos Reservados', compute='_asientosReservados')


    @api.depends('asientos', 'asistentes_ids')
    def _asientosReservados(self):
        for record in self:
            if not record.asientos:
                record.asientosReservados=0.0
            else:
                record.asientosReservados=100*len(record.asistentes_ids) / record.asientos
    @api.onchange('asientos', 'asistentes_ids')
    def _verify_valid_seats(self):
        self.ensure_one()
        if self.asientos<0:
            self.asientos=0
            return{
            'warning':{
                'title':'Numero de Asientos Incorrecto', 'message': 'El Numero de Asientos No Debe Ser Negativo',
                },
            }
        if self.asientos<len(self.asistentes_ids):
            return{
            'warning':{
                'title':'Hay Demasiados Asientos Reservados',
                'message': 'El Numero de Asientos Reservados es Mayor que los '\
                'Asientos Disponibles. Incremente el Numero Asientos o '\
                'Reasigne a los Reservantes'
                },
            }
    @api.constrains('instructor_id', 'asistentes_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id and record.instructor_id in record.asistentes_ids:
                raise exceptions.ValidationError('El Instructor de la Sesion no Puede Estar Entre'\
                'los Reservantes')
