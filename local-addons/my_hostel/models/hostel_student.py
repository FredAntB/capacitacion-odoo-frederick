from odoo import fields, models

class HostelStudent(models.Model):
    _name = "hostel.student"
    #_inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Student Information"

    name = fields.Char("Student Name")
    gender = fields.Selection([("male", "Male"), ("female", "Female"), ("other", "Other")], string="Gender", help="Student gender")
    active = fields.Boolean("Active", default=True, help="Activate/Deactivate hostel record")
    room_id = fields.Many2one("hostel.room", "Room", help="Select hostel room")

    hostel_id = fields.Many2one("hostel.hostel", related='room_id.hostel_id')
    partner_id = fields.Many2one('res.partner', ondelete='cascade', delegate=True)

    status = fields.Selection([('draft', 'Draft'),
                               ('reservation', 'Reservation'),
                               ('pending', 'Pending'),
                               ('paid', 'Done'),
                               ('discharge', 'Discharge'),
                               ('cancel', 'Cancel')],
                               "Status",
                               copy=False,
                               default="draft",
                               help="State of the student hostel")
    admission_date = fields.Date("Admission Date",
                                 help="Date of admission in hostel",
                                 default=fields.Datetime.today)
    discharge_date = fields.Date("Discharge Date",
                                 help="Date on which student discharge")
    duration = fields.Integer("Duration", compute="_compute_check_duration", inverse="_inverse_duration",
                              help="Enter duration of living")
        
    def action_assign_room(self):
        self.ensure_one()
        if self.status != "paid":
            raise UserError(_("You can't assign a room if it's not paid."))
        room_as_superuser = self.env['hostel.room'].sudo()
        room_rec = room_as_superuser.create({
            "name": "Room A-103",
            "room_no": "A-103",
            "floor_no": 1,
            "room_category_id": self.env.ref("my_hostel.single_room_categ").id,
            "hostel_id": self.hostel_id.id
            })
    
    def action_remove_room(self):
        if self.env.context.get("is_hostel_room"):
            self.room_id = False
