from odoo import fields, models, api, exceptions
from odoo.exceptions import ValidationError
class HostelRoom(models.Model):
        _name = "hostel.room"
        _inherit = ['base.archive']
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
        #hostel_amenities_ids = fields.Many2many("hostel.amenities", "hostel_room_amenities_rel", "room_id", "amenity_id", string="Amenities", domain="[('active', '=', True)]", help="Select hostel room amenities")
        # current fix for proper inheritance
        hostel_amenities_ids = fields.Many2many("hostel.amenities", string="Amenities", domain="[('active', '=', True)]", help="Select hostel room amenities")

        student_per_room = fields.Integer("Student Per room", required=True, help="Students allocated per room")
        availability = fields.Float(compute="_compute_check_availability", store=True, string="Availability", help="Room availability in hostel")

        admission_date = fields.Date("Admission Date", help="Date of admission in hostel", default=fields.Datetime.today)
        discharge_date = fields.Date("Discharge Date", help="Date on which student discharge")
        duration = fields.Integer("Duration", compute="_compute_check_duration", inverse="_inverse_duration", help="Enter duration of living")

        date_terminate = fields.Date('Date of Termination')
        remarks = fields.Text('Remarks')

        previous_room_id = fields.Many2one('hostel.room', string='Previous Room')

        cost_price = fields.Float('Room Cost')
        category_id = fields.Many2one('hostel.room.category')

        @api.depends("admission_date", "discharge_date")
        def _compute_check_duration(self):
            """Method to check duration"""
            for rec in self:
                if rec.discharge_date and rec.admission_date:
                    rec.duration = (rec.discharge_date - rec.admission_date).days

        def _inverse_duration(self):
            for stu in self:
                if stu.discharge_date and stu.admission_date:
                    duration = (stu.discharge_date - stu.admission_date).days
                    if duration != stu.duration:
                            stu.discharge_date = (stu.admission_date + timedelta(days=stu.duration)).strftime('%Y-%m-%d')

        @api.depends("student_per_room", "student_ids")
        def _compute_check_availability(self):
            """Method to check room availability"""
            for rec in self:
                rec.availability = rec.student_per_room - len(rec.student_ids.ids)

        @api.constrains("rent_amount")
        def _check_rent_amount(self):
            """Constraint on negative rent amount"""
            if self.rent_amount < 0:
                raise ValidationError(_("Rent Amount Per Month should not be a negative value!"))

        def log_all_room_members(self):
            # This is an empty recordset of model hostel.room.member
            hostel_room_obj = self.env['hostel.room.member']

            sll_members = hostel_room_obj.search([])
            print("ALL MEMBERS:", all_members)
            return True

        def update_room_no(self):
            self.ensure_one()
            self.room_no = "RM002"
            # Option 2 -> Only works with recorsets with a length of 1
            # self.update ({
            #     'room_no': "RM002",
            #     'another_field': 'value'
            #     ...
            # })

        def find_room(self):
            domain = [
                    '|',
                    '&', ('name', 'ilike', 'Room Name'),
                         ('category_id.name', 'ilike', 'Category Name'),
                    '&', ('name', 'ilike', 'Second Room Name 2'),
                         ('category_id.name', 'ilike', 'SecondCategory Name'),
                    ]
            rooms = self.search(domain)

        def filter_members(self, room):
            all_rooms = self.search([])
            filtered_rooms = self.rooms_with_multiple_members(all_rooms)

        @api.model
        def room_with_multiple_members(self, all_rooms):
            def predicate(room):
                if len(room.member_ids) > 1:
                    return True
                return False
            return all_room.filter(predicate)

        @api.model
        def room_with_multiple_rooms(self, all_rooms):
            # return all_rooms.filter('category_id')
            return all_rooms.filter(lambda b: len(b.member_ids > 1))

        @api.model
        def get_members_names(self, rooms):
            return rooms.mapped('member_ids.name')

        @api.model
        def sort_rooms_by_rating(self, rooms):
            return rooms.sorted(key='room_rating') # reverse=True -> optional parameter

        @api.model
        def create(self, values):
            if not self.user_has_groups('my_hostel.group_hostel_manager'):
                if values.get('remarks'):
                    raise UserError(
                        'You are not allowed to modify'
                        'remarks'
                    )
            return super(HostelRoom, self).create(values)

        @api.model
        def write(self, values):
            if not self.user_has_groups('my_hostel.group_hostel_manager'):
                if values.get('remarks'):
                    # del values['remarks'] -> alternative
                    raise UserError(
                        'You are not allowed to modify'
                        'manager_remarks'
                    )
            return super(HostelRoom, self).create(values)

        def name_get(self):
            result = []
            for room in self:
                member = room.member_ids.mapped('name')
                name = '%s (%s)' % (room.name, ', '.join(member))
                result.append((room.id, name))
                return result

        @api.model
        def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
            args = [] if args is None else args.copy()
            if not(name == '' and operator == 'ilike'):
                args += ['|', '|',
                         ('name', operator, name),
                         ('isbn', operator, name),
                         ('author_ids.name', operator, name)
                         ]
            return super(HostelRoom, self)._name_search(
                    name=name, args=args, operator=operator,
                    limit=limit, name_get_uid=name_get_uid)

        @api.model
        def _get_average_cost(self):
            grouped_result = self.read_group(
                    [('cost_price', "!=", False)], # Domain
                    ['category_id', 'cost_price:avg'], #Fields to access
                    ['category_id'] # group_by
                    )
            return grouped_result

        def action_remove_room_members(self):
            student.with_context(is_hoste_room=True).action_remove_room()
            # alternative options
            # new_context = self.env.context.copy()
            # new_context.update({'is_hostel_room': True})
            # student.with_context(new_context)

class HostelRoomMember(models.Model):
    _name = 'hostel.room.member'
    _inherits = {'res.partner': 'partner_id'}
    _description = "Hostel Room member"

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    date_of_birth = fields.Date('Date of birth')
