# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Project Tags",
    "summary": """Project Tags""",
    "author": "Patrick Wilson, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/project",
    "category": "Project Management",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["project"],
    "data": ["views/project_views.xml",
             "views/project_main_tag_views.xml",
             "views/stage_views.xml",
             "menus/project_main_tag_menus.xml",
             "security/security.xml",
             "security/ir.model.access.csv",
             ],
    "application": False,
    "development_status": "Beta",
    "maintainers": ["patrickrwilson"],
}
