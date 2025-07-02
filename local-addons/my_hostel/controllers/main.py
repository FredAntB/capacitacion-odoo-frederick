from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class Main(http.Controller):
    @http.route('/demo_page', type='http', auth='none')
    def demo_page(self):
        image_url = '/my_hostel/static/src/image/odoo.png'
        html_result = """<html>
            <body>
                <img src="%s"/>
            </body>
        </html>""" % image_url
        return html_result

    @http.route('/my_hostel/students', type='http', auth='none')
    def students(self):
        students = request.env['hostel.student'].sudo().search([])
        html_result = '<html><body><ul>'
        for student in students:
            html_result += "<li> %s </li>" % student.name
        html_result += '</ul></body></html>'
        return html_result

    @http.route('/my_hostel/students/json', type='json', auth='none')
    def students_json(self):
        records = request.env['hostel.student'].sudo().search([])
        return records.read(['name'])

class WebsiteInfo(Website):
    @http.route()
    def website_info(self):
        result = super(WebsiteInfo, self).website_info()
        result.qcontext['apps'] = result.qcontext['apps'].filtered(
            lambda x: x.name != 'website'
        )
        return result
