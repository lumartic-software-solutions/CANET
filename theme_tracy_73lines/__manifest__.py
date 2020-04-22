# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by 73lines
# See LICENSE file for full copyright and licensing details.
{
    'name': 'Theme Tracy',
    'description': 'Theme Tracy',
    'category': 'Theme/Business',
    'version': '11.0.1.0.0',
    'author': '73Lines',
    'website': 'https://www.73lines.com',
    'application': True,
    'depends': ['business_all_in_one_73lines', 'mass_mailing', 'website_blog'],
    'data': [
        'views/assets.xml',
        'views/customize_modal.xml',
        'views/homepage.xml',
        'views/footer_template.xml',
    ],
    'images': [
        'static/description/tracy_business_banner.png',
        'static/description/tracy_screenshot.png',
    ],
    'license': 'OPL-1',
    'live_test_url': ''
}
