# © 2020 Solvos Consultoría Informática (<http://www.solvos.es>)
# License LGPL-3 - See http://www.gnu.org/licenses/lgpl-3.0.html

from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class MaintenanceStage(models.Model):
    _inherit = 'maintenance.stage'

    ifs_checked = fields.Boolean(
        'IFS checked',
        default=False)


class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    ifs_check_repaired_correctly = fields.Boolean(
        string='Equipment repaired correctly')
    ifs_check_free_strange_elements = fields.Boolean(
        string='Free strange elements')
    ifs_check_collected_location = fields.Boolean(
        string='Collected location')
    ifs_check_cleaning_area = fields.Boolean(
        string='Cleaning the area')
    ifs_checked = fields.Boolean(
        string='IFS checked',
        related='stage_id.ifs_checked')

    def _ifs_check_ok(self):
        self.ensure_one()
        return self.ifs_check_repaired_correctly \
               and self.ifs_check_free_strange_elements \
               and self.ifs_check_collected_location \
               and self.ifs_check_cleaning_area

    @api.constrains('stage_id')
    def _check_ifs_checked(self):
        for req in self:
            if req.stage_id.ifs_checked and not req._ifs_check_ok():
                raise ValidationError(
                    _("It can´t be IFS check stage"
                      " without checked all IFS checks"))
