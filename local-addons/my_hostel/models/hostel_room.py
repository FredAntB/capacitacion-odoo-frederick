from odoo import fields, models, api
from odoo.exceptions import ValidationError
class HostelRoom(models.Model):
        _name = "hostel.room"
        _description = "Hostel Room"
        _order = "room_no"
        _sql_constraints = [
                ("room_no_unique", "unique(room_no)", "Room number must be unique!")]
        
        name = fields.Char(string="Room Name", required=True)
        room_no = fields.Integer(string="Room No.", required=True)
        floor_no = fields.Integer(string="Floor No.", help="Enter floor where the room is located at")
        currency_id = fields.Many2one('res.currency', string='Currency')
        rent_amount = fields.Monetary('Rent Amount', help="Enter rent amount per month") # optional attribute: currency_field='currency_id' in case currency field have another name then 'currency_id'
        hostel_id = fields.Many2one("hostel.hostel", "hostel", help="Name of hostel")
        student_ids = fields.One2many("hostel.student", "room_id", string="Students", help="Enter students")
        hostel_amenities_ids = fields.Many2many("hostel.amenities", "hostel_room_amenities_rel", "room_id", "amenity_id", string="Amenities", domain="[('active', '=', True)]", help="Select hostel room amenities")

        @api.constrains("rent_amount")
        def _check_rent_amount(self):
            """Constraint on negative rent amount"""
            if self.rent_amount < 0:
                raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))
