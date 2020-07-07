# -*- coding: utf-8 -*-
import logging
import copy
from odoo import SUPERUSER_ID
from odoo import http
from odoo.http import request
import json
_logger = logging.getLogger(__name__)



class APISaleOrder(http.Controller):


    @http.route('/snow-call-login-supper', type='json', auth='none', methods=['post'], csrf=False)
    def api_paid_so(self, **kw):

        data = request.jsonrequest
        data.get('odoo_password')
        data.get('odoo_id')
        request.session.authenticate('axys-work',data.get('odoo_id'),data.get('odoo_password'))
        return request.env['ir.http'].session_info()

    @http.route('/get-api-test/<string:funtion>',type='http', auth='user',methods=['get'])
    def get_account_info(self,funtion, **kw):
        return_data={}
        if funtion == 'api_login':
            input={'sam_user':'huy','sam_password':'1'}
            data = request.env['hr.employee'].api_login('huy','1')
        if funtion == 'get_employee_detail':
            data = request.env['hr.employee'].get_employee_detail(64623)
        if funtion == 'get_project_menu':
            data = request.env['project.project'].get_project_menu(64623)
        if funtion == 'get_project_detail':
            data = request.env['project.project'].get_project_detail(46)
        if funtion == 'get_project_output':
            data = request.env['project.project'].get_project_output(42)
        if funtion == 'api_change_password':
            data = request.env['hr.employee'].api_change_password(user='',old_password='',new_password='')
        if funtion == 'get_employee_role_in_project':
            data = request.env['project.member'].get_employee_role_in_project(64623,46)
        if funtion == 'get_notifications':
            data = request.env['project.project'].get_notifications(46)
        if funtion == 'get_hr_employee_list':
            data = request.env['hr.employee'].get_hr_employee_list()
        if funtion == 'get_hr_department_list':
            data = request.env['hr.department'].get_hr_department_list()
        if funtion == 'get_notifications':
            data = request.env['project.project'].get_notifications(46)
        if funtion == 'get_hr_holidays_status_list':
            data = request.env['hr.holidays.status'].get_hr_holidays_status_list()
        if funtion == 'get_hr_holidays_list':
            data = request.env['hr.holidays.status'].get_hr_holidays_list(64623)
        if funtion == 'get_project_shiftis':
            data = request.env['project.project'].get_project_shiftis(42,12)
        if funtion == 'get_hr_department_list':
            data = request.env['hr.department'].get_hr_department_list()
        if funtion == 'get_hr_department_detail':
            data = request.env['hr.department'].get_hr_department_detail(3242)
        if funtion == 'get_project_member_list':
            data = request.env['project.member'].get_project_member_list(42,12)
        if funtion == 'get_hr_holidays_list_all':
            data = request.env['hr.holidays'].get_hr_holidays_list_all(42)
        if funtion == 'get_hr_holidays_detail':
            data = request.env['hr.holidays'].get_hr_holidays_detail(3009)
        if funtion == 'get_hr_holidays_detail':
            data = request.env['hr.holidays'].get_hr_holidays_detail(3009)
        if funtion == 'get_project_holiday':
            data = request.env['project.project'].get_project_holiday(42,12)
        if funtion == 'get_hr_attendance_list':
            data = request.env['hr.attendance'].get_hr_attendance_list(166)
        if funtion == 'get_notifications':
            data = request.env['project.project'].get_notifications(42)
        if funtion == 'get_hr_attendance_all':
            data = request.env['hr.attendance'].get_hr_attendance_all(42)
        # if funtion == 'set_attendance':
        #     data = request.env['hr.attendance'].set_attendance({'check_in': '2020-07-03 16:12:04',
        #                                                        'employee_id': 1, 'company_id': 1,
        #                                                        'state': 'draft','check_out': False},0)
        if funtion == 'check_inout':
            data = request.env['hr.attendance'].check_inout(42,1)
        if funtion == 'set_attendance':
            data = request.env['hr.attendance'].set_attendance({'check_out': '2020-07-03 18:12:04'},115297)
        if funtion == 'set_hr_holidays':
            data = request.env['hr.holidays'].set_hr_holidays({
                                                                       'holiday_status_id': 9,
                                                                       'employee_id': 57673,
                                                                       'date_from': '2020-07-05 15:49:46',
                                                                       'holiday_type': 'employee',
                                                                       'type': 'remove',
                                                                       'date_to': '2020-07-06 15:49:48',
                                                                       'name': 'Create Lead From Customer',
                                                                     },0)
        # if funtion == 'get_notifications':
        #     data = request.env['hr.attendance'].get_hr_attendance_all({
        #                                                                'holiday_status_id': 9,
        #                                                                'employee_id': 57673,
        #                                                                'date_from': '2020-07-03 15:49:46',
        #                                                                'holiday_type': 'employee',
        #                                                                'type': 'remove',
        #                                                                'date_to': '2020-07-04 15:49:48',
        #                                                                'name': 'Create Lead From Customer',
        #                                                              })
        if funtion == 'get_notifications':
            data = request.env['project.project'].get_notifications(42,0,True)
        if funtion == 'search_hr_attendance_list':
            data = request.env['hr.attendance'].search_hr_attendance_list(166,'2020-02-01','2020-05-31')
        if funtion == 'create_project_member_list':
            data = request.env['project.member'].create_project_member_list([{'employee_id': 63690, 'end_date': '2020-08-04', 'job_position_id': 1, 'check_id': 17, 'project_location_id': 2, 'active': True, 'project_id': 42, 'project_shiftis_id': 1, 'start_date': '2020-09-04', 'project_role': 'User'}])
        if funtion == 'set_project_notification':
            data = request.env['project.notification'].set_project_notification({'name':'abc','description':'abxxxx',
                                                                                 'specail_list':[64623,64670],
                                                                                 'project_id':42,
                                                                                 'active':True,

                                                                                 },0)
        return data