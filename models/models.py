# -*- coding: utf-8 -*-

from odoo import models, fields, api,exceptions
from datetime import timedelta


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
    inicio= fields.Datetime(default=lambda self:fields.Datetime.now())
    duracion= fields.Float(string='Duracion', digits=(6,2), help='Duracion en días')
    asientos= fields.Integer(string='Asientos')
    instructor_id=fields.Many2one('res.partner',string='Instructor',
    domain=[('instructor','=', True)])
    curso_id= fields.Many2one('rnet.curso', ondelete='cascade', string='Curso', required=True)
    asistentes_ids= fields.Many2many('res.partner', 'partner_sesion_rel', 'sesion_id', 'partner_id',string='Asistentes')
    asientosReservados=fields.Float(string='Asientos Reservados', compute='_asientosReservados')
    fin=fields.Datetime(string='fin', store=True,
    compute='_getFin', inverse='_setFin')

# Flujos de trabajo en que estado se encuentra la sesion

    state = fields.Selection([
    ('borrador', "Borrador"),
    ('confirmado',"Confirmado"),
    ('realizado',"Realizado"),
    ('cancelado',"Cancelado"),
    ], string='Estado',copy=False, default='borrador')

    @api.multi
    def action_borrador(self):
        for x in self:
            x.state = 'borrador'

    @api.multi
    def action_confirmado(self):
        for x in self:
            x.state = 'confirmado'

    @api.multi
    def action_realizado(self):
        for x in self:
            x.state = 'realizado'

    @api.multi
    def action_cancelado(self):
        for x in self:
            x.state = 'cancelado'





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

    @api.depends('inicio', 'duracion')
    def _getFin(self):
        for record in self:
            if not (record.inicio and record.duracion):
                record.fin=record.inicio
                continue
            inicio=fields.Datetime.from_string(record.inicio)
            duracion=timedelta(days=(record.duracion - 1))
            record.fin=inicio + duracion

    def _setFin(self):
        for record in self:
            if not (record.inicio and record.fin):
                continue
            inicio=fields.Datetime.from_string(record.inicio)
            fin=fields.Datetime.from_string(record.fin)
            record.duracion=(fin - inicio).days + 1




    @api.constrains('instructor_id', 'asistentes_ids')
    def _check_instructor_not_in_attendees(self):
        for record in self:
            if record.instructor_id and record.instructor_id in record.asistentes_ids:
                raise exceptions.ValidationError('El Instructor de la Sesion no Puede Estar Entre'\
                'los Reservantes')
