# Copyright 2019 Patrick Wilson <patrickraymondwilson@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api, SUPERUSER_ID
from odoo.exceptions import ValidationError

class Project(models.Model):
    _inherit = "project.project"

    def get_default_project_main_tag_ids(self):
        return self.env['project.main.tag'].search(['&',('is_default', '=', True),('company_id', '=', self.env.company.id)]).ids

    project_main_tag_ids = fields.Many2many("project.main.tag", string="Project Tags", default=get_default_project_main_tag_ids)

    @api.onchange('project_main_tag_ids')
    def _onchange_project_main_tag_ids(self):
        if self.project_main_tag_ids :
            self.type_ids = self.env['project.task.type'].search([
                    ('project_main_tag_ids', 'in', self.project_main_tag_ids.ids),
                ])
        else:
            self.type_ids = None

    # @api.model
    # def create(self, vals):
    #     project = super(Project, self).create(vals)
    #     if self.project_main_tag_ids:
    #         self.type_ids = self.project_main_tag_ids.project_task_type_ids
    #         print(self.type_ids, self.project_main_tag_ids, "LLLLLLLLLLLLLLLL")
    #     else :
    #         self.type_ids = None
    #         print(self.type_ids, self.project_main_tag_ids, "LLLLLLLLLLLLLLLL")
    #     return project


    # @api.model
    # def create(self, vals):
    #     res = super(Project, self).create(vals)
    #     stage_ids = self.env['project.task.type'].search([('project_main_tag_ids', 'in', res.project_main_tag_ids.ids)])
    #     if stage_ids:
    #         stage_ids.write({'project_ids' : [(4, res.id)]})
    #     return res

class ProjectTaskType(models.Model):
    _inherit = "project.task.type"

    project_main_tag_ids = fields.Many2many("project.main.tag", string="Project Tags")
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=False, default = lambda self : self.env.company)
    task_ids = fields.Many2many('project.task', 'project_id', string='Tasks',
                               domain=['|', ('stage_id.fold', '=', False), ('stage_id', '=', False)])

    #@api.multi
    @api.constrains('name')
    def _check_name_unicity(self):
        if self.name:
            for task_type in self:
                if self.search_count([
                    ('name', '=', task_type.name),
                    # ('company_id', '=', task_type.company_id),
                ]) > 1:
                    raise ValidationError(("Already Exist, Please Create Different One !"))

    _sql_constraints = [
        ('name_company_uniq', 'unique (name,company_id)', 'The name of the stage must be unique per company !')
    ]

class ProjectMainTag(models.Model):
    """ Tags of project's tasks """
    _name = "project.main.tag"
    _description = "Project Main Tag"

    name = fields.Char('Project Main Tag', required=True)
    color = fields.Integer(string='Color Index')
    is_default = fields.Boolean(string="Default ?",  )
    default_company_ids = fields.Many2many(comodel_name="res.company", relation="", column1="", column2="", string="Default Companies", )
    company_id = fields.Many2one(comodel_name="res.company", string="Company", required=False, default = lambda self : self.env.company)
    project_task_type_ids = fields.Many2many("project.task.type", string="Project Stages")

    # _sql_constraints = [
    #     ('name_uniq', 'unique (name)', "Tag name already exists!"),
    # ]

    _sql_constraints = [
        ('name_company_uniq', 'unique (name,company_id)', 'The name of the stage must be unique per company !')
    ]

class ProjectTask(models.Model):
    _inherit = "project.task"

    # @api.model
    # def read_group_stage_ids(self, present_ids, domain, **kwargs):
    #     result = self.env['project.task.type'].search([]).name
    #     return result, None
    #
    # _group_by_full = {'stage_id': read_group_stage_ids}

    # @api.model
    # def _read_group_stage_ids(self, stages, domain, order):
    #     stage_ids = self.env['project.task.type'].search([])
    #     print(self.env.context, "TTTTTTTTTTTTTTTTTTTTTTT")
    #     return stage_ids

    @api.model
    def _read_group_stage_ids(self, stages, domain, order):
        search_domain = [('id', 'in', stages.ids)]
        if 'default_project_id' in self.env.context:
            search_domain = ['|', ('project_ids', '=', self.env.context['default_project_id'])] + search_domain
            stage_ids = stages._search(search_domain, order=order, access_rights_uid=SUPERUSER_ID)
            return stages.browse(stage_ids)
        return self.env['project.task.type'].search([])



#    stage_id = fields.Many2one('project.task.type', group_expand='_read_group_stage_ids')



    # @api.model
    # def stage_groups(self, present_ids, domain, **kwargs):
    #     stages = self.env['project.task.type'].search([]).name_get()
    #     return stages, None  #

    # _group_by_full = {'stage_id': stage_groups,}
    #

    # @api.model
    # def stage_groups(self, present_ids, domain, **kwargs):
    #     stages = self.env['project.task.type'].search([]).name_get()
    #     return stages, None



