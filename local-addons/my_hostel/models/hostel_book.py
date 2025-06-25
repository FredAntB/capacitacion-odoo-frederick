from odoo import fields, models, api
class ResPartner(models.Model):
    _inherit = "res.partner"
    is_hostel_rector = fields.Boolean("Hostel rector", help="Activate if the following person is hostel rector")
    assign_room_ids = fields.Many2many('library.book', string='Authored Books')
    count_assing_room = fields.Integer('Number of Authored Books', compute="_compute_count_room")

    @api.depends('assign_room_ids')
    def _compute_count_room(self):
        for partner in self:
            partner.count_assing_room = len(partner.assign_room_ids)

    def find_partner(self):
        PartnerObj = self.env['res.partner']
        domain = [
            '&', ('name', 'ilike', 'SerpentCS'),
                 ('company_id.name', '=', 'SCS')
        ]
        partner = PartnerObj.search(domain)

class BaseArchive(models.AbstractModel):
    _name = 'base.archive'
    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active
