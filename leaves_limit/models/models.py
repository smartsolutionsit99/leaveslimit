# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, AccessError, ValidationError
from odoo.tools.translate import _


class hr_holidays_status(models.Model):
    _inherit = 'hr.holidays.status'


    monthly_limit = fields.Boolean("Limit By Month")
    monthly_limit_amount = fields.Integer("Maximum monthly Request")
    annual_limit = fields.Boolean("Limit By Year")
    annual_limit_amount = fields.Integer("Maximum annual Request")

class hr_holidays(models.Model):
    _inherit = 'hr.holidays'

    @api.constrains('employee_id', 'holiday_status_id', 'number_of_days_temp')
    def _check_request_limit(self):
        for rec in self:
            ids = self.env['hr.holidays'].search(
                [('employee_id', '=', self.employee_id.id), ('type', '!=', 'add'), ('id', '!=', self.id),
                 ('state', '=', 'validate')])
            if rec.holiday_status_id and rec.holiday_status_id.monthly_limit:
                m = 0
                for request in ids:
                    if fields.Datetime.from_string(request.date_from).month == fields.Datetime.from_string(rec.date_from).month:
                        m = m + 1
                m = m + 1
                if m > rec.holiday_status_id.monthly_limit_amount:
                    raise UserError(_("Leave Request Exceeded For This Month"))

            if rec.holiday_status_id and rec.holiday_status_id.annual_limit:
                y = 0
                for request in ids:
                    if fields.Datetime.from_string(request.date_from).year == fields.Datetime.from_string(rec.date_from).year:
                        y = y + 1
                y = y + 1
                if y > rec.holiday_status_id.annual_limit_amount:
                    raise UserError(_("Leave Request Exceeded For This Year"))