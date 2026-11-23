from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
DIAS_MAXIMOS_ESTUDIANTE = 7 
LIMITE_EQUIPOS_ESTUDIANTE = 2
  
  
class PrestamoPrestamo(models.Model): 
    _name = "prestamo.prestamo" 
    _description = "Préstamo de equipo" 
    _inherit = ["mail.thread"] 
    _order = "fecha_prestamo desc, id desc" 
  
    name = fields.Char(string="Motivo", required=True) 
    partner_id = fields.Many2one("res.partner", string="Solicitante", required=True) 
    tipo_solicitante = fields.Selection( 
        [("estudiante", "Estudiante"), ("docente", "Docente")], 
        string="Tipo de solicitante", 
        required=True, 
        default="estudiante", 
    ) 
    fecha_prestamo = fields.Date( string="Fecha de préstamo", required=True, default=fields.Date.context_today 
    ) 
    fecha_devolucion = fields.Date(string="Fecha de devolución", required=True) 
    state = fields.Selection( 
        [ 
            ("borrador", "Borrador"), 
            ("prestado", "Prestado"), 
            ("devuelto", "Devuelto"), 
            ("atrasado", "Atrasado"), 
        ], 
        string="Estado", 
        required=True, 
        default="borrador", 
        tracking=True, 
    ) 
    linea_ids = fields.One2many("prestamo.linea", "prestamo_id", string="Equipos") 
    cantidad_equipos = fields.Integer( 
        string="Cantidad de equipos", compute="_compute_cantidad_equipos", store=True 
    ) 
    dias_prestamo = fields.Integer( 
        string="Días de préstamo", compute="_compute_dias_prestamo", store=True 
    ) 
  
    @api.depends("linea_ids") 
    def _compute_cantidad_equipos(self): 
        for prestamo in self: 
            prestamo.cantidad_equipos = len(prestamo.linea_ids) 
  
    @api.depends("fecha_prestamo", "fecha_devolucion") 
    def _compute_dias_prestamo(self): 
        for prestamo in self: 
            if prestamo.fecha_prestamo and prestamo.fecha_devolucion: 
                dias = (prestamo.fecha_devolucion - prestamo.fecha_prestamo).days 
                prestamo.dias_prestamo = dias 
            else: 
                prestamo.dias_prestamo = 0 

    def action_prestar(self): 
        for prestamo in self: 
            if prestamo.state != "borrador": 
                raise UserError("Solo se puede prestar un préstamo en borrador.") 
            if not prestamo.linea_ids: 
                raise UserError("Agregue al menos un equipo al préstamo.") 
            prestamo.linea_ids.equipo_id.write({"estado": "prestado"}) 
            prestamo.state = "prestado" 
            prestamo.message_post( 
                body=f"Se prestaron {prestamo.cantidad_equipos} equipo(s) " 
                     f"a {prestamo.partner_id.name}." 
            ) 
            # TODO 4: si el solicitante es estudiante y lleva más de 
#     LIMITE_EQUIPOS_ESTUDIANTE equipos, lanzar UserError con el límite. 
# TODO 5: recorrer las líneas; si algún equipo no está "disponible", 
#     lanzar UserError con el nombre del equipo.
  
    def action_devolver(self): 
        for prestamo in self: 
            if prestamo.state not in ("prestado", "atrasado"): 
                raise UserError("Solo se puede devolver un préstamo activo.") 
            prestamo.linea_ids.equipo_id.write({"estado": "disponible"}) 
            prestamo.state = "devuelto" 
            prestamo.message_post(body="Los equipos fueron devueltos.")
@api.constrains("fecha_prestamo", "fecha_devolucion", "tipo_solicitante") 
def _check_fechas(self): for prestamo in self: 
# TODO 1: la fecha de devolución no puede ser anterior a la fecha de préstamo. 
# TODO 2: si el solicitante es estudiante, dias_prestamo no puede superar 
#     DIAS_MAXIMOS_ESTUDIANTE. 
pass 
@api.constrains("linea_ids") 
def _check_equipos_repetidos(self): 
for prestamo in self: 
# TODO 3: un equipo no puede aparecer dos veces en el mismo préstamo. 
# Pista: compare len(prestamo.linea_ids) con len(prestamo.linea_ids.equipo_id). 
pass
def action_marcar_atrasado(self):
    hoy = fields.Date.context_today(self)

    for prestamo in self:
        if prestamo.state != "prestado":
            raise UserError("Solo se puede marcar como atrasado un préstamo prestado.")

        if prestamo.fecha_devolucion >= hoy:
            raise UserError("La fecha de devolución todavía no ha pasado.")

        prestamo.state = "atrasado"

        prestamo.message_post(
            body="El préstamo fue marcado como atrasado."
        )