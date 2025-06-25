from odoo import models, fields, api
from odoo.exceptions import ValidationError
class HostelCategory(models.Model):
    _name = "hostel.room.category"
    name = fields.Char('Category')
    description = fields.Text('Description')
    parent_id = fields.Many2one(
            'hostel.room.category',
            string='Parent Category',
            ondelete='restrict',
            index=True)
    child_ids = fields.One2many(
            'hostel.room.category', 'parent_id',
            string='Child Categories')
    _name = "hostel.room.category"

    _parent_store = True
    _parent_name = "parent_id" # optional if field is 'parent_id'
    parent_path = fields.Char(index=True, unaccent=False)

    @api.constrains('parent_id')
    def _check_hierarchy(self):
        if not self._check_recursion():
            raise models.ValidationError(
                    'Error! you cannot create recursive categories.')

    def create_categories(self):
        categ1 = {
                'name': 'Child category 1',
                'description': 'Description for child 1'
                }
        categ2 = {
                'name': 'Child category 2',
                'description': 'Description for child 2'
                }
        parent_category_val = {
                'name': 'Parent category',
                'description': 'Description for parent category',
                'child_ids': [
                    (0, 0, categ1),
                    (0, 0, categ2),
                    ]
                }
        self.env['hostel.room.category'].create(parent_category_val)
        # You can also create a category in batches
        # multiple_records = self.env['hostel.room.category'].create([categ1, categ2])
        return True
