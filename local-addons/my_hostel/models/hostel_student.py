from odoo import fields, models

class HostelStudent(models.Model):
    _name = "hostel.student"
    name = fields.Char("Student Name")
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender", help="Student gender")
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
    room_id = fields.Many2one("hostel.room", "Room", help="Select hostel room")
