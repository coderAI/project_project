# -*- coding: utf-8 -*-
import json
from odoo import models, api, fields, _
from datetime import datetime
import logging
from odoo import fields, models, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import Warning
from dateutil import relativedelta

class project_notification(models.Model):
    _name = 'project.notification'

    name = fields.Char(string='Name')
    description = fields.Text(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
    specail_list = fields.Many2many('hr.employee','pn_pm_rel','pm_id','pn_id', string='Project Member')
    all = fields.Boolean(string='All', default=True)
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def create(self, vals):
        return super(project_notification, self).create(vals)

    @api.model
    def set_project_notification(self,obj,id=0):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:

            if obj.get('specail_list'):
                obj.update({'specail_list':[(6,False,obj.get('specail_list'))]})
            self.create(obj)
        else:
            if obj.get('specail_list'):
                obj.update({'specail_list': [(6, False, obj.get('specail_list'))]})
            self.browse(id).write(obj)

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


class project_holidays(models.Model):
    _name = 'project.holidays'

    name = fields.Char(string='Name')
    off_date = fields.Datetime(string='Date')
    project_id = fields.Many2one('project.project', string='Project')
    active = fields.Boolean(string='Active', default=True)

    @api.model
    def set_project_holidays(self,obj,id=0):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            data = self.create(obj).id
        else:
            self.browse(id).write(obj)

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)



class output_image(models.Model):
    _name = 'output.image'
    name = fields.Char(string="description")
    image_medium = fields.Binary("Medium-sized image", attachment=True,
                                 help="Medium-sized image of this contact. It is automatically " \
                                      "resized as a 128x128px image, with aspect ratio preserved. " \
                                      "Use this field in form views or some kanban views.")
    project_output_id = fields.Many2one('project.output',string="Output")

class project_output(models.Model):
    _name = 'project.output'

    name = fields.Char(string='Name')
    description = fields.Char(string='Description')
    project_id = fields.Many2one('project.project', string='Project')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    quantity = fields.Float(string='Quantity', track_visibility='onchange')
    product_uom_id = fields.Many2one('product.uom', string='Uom')
    hr_attendance_id = fields.Many2one('hr.attendance', string='Attendance')
    output_image_ids = fields.One2many('output.image','project_output_id',string="Output Image List")
    active = fields.Boolean(string='Active', default=True)


    @api.model
    def set_project_output(self,obj,id):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            self.create(obj)
        else:
            self.browse(id).write(obj)

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


class project_shiftis(models.Model):
    _name = 'project.shiftis'

    name = fields.Char(string='Name')
    start_time = fields.Float(string='Start Time', track_visibility='onchange')
    end_time = fields.Float(string='End Time', track_visibility='onchange')

    active = fields.Boolean(string='Active', default=True)


    @api.model
    def set_project_shiftis(self,obj,id):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            # data = self.create(obj).id
            project_id = obj.get('project_id')
            project_data = self.env['project.project'].search([('id', '=', project_id)], limit=1)
            project_data.write({'project_shiftis_ids': [(0, 0, obj)]})
        else:
            self.browse(id).write(obj)

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


class project_job_description(models.Model):
    _name = 'project.job.description'

    name = fields.Char(string='Name')
    active = fields.Boolean(string='Active', default=True)


class project_location(models.Model):
    _name = 'project.locations'

    name = fields.Char(string='Name')
    street = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    latitude = fields.Float(stirng='Geo Latitude', digits=(16, 5))
    longitude = fields.Float(string='Geo Longitude', digits=(16, 5))
    active = fields.Boolean(string='active', default=True)
    radius = fields.Float(string='Radius', track_visibility='onchange')
    @api.model
    def get_country_list(self):
        messages = 'Successful'
        code = 200
        data=[]
        for i in self.env['res.country'].search([]):
            data.append({
                'id':i.id,
                'name':i.name,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    @api.model
    def get_state_list(self):
        messages = 'Successful'
        code = 200
        data=[]
        for i in self.env['res.country.state'].search([('active','in',(False,True,None))]):
            data.append({
                'id':i.id,
                'name':i.name,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    @api.model
    def set_project_location(self,obj,id=0):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            project_id = obj.get('project_id')
            project_data = self.env['project.project'].search([('id', '=', project_id)], limit=1)
            project_data.write({'project_location_ids': [(0, 0, obj)]})
            # data = self.create(obj).id
        else:
            self.browse(int(id)).write(obj)

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

class project_worker(models.Model):
    _name = 'project.worker'

    employee_id = fields.Many2one('hr.employee',string='Employee')
    date = fields.Datetime('Date', track_visibility='onchange')
    count_report = fields.Float(string='Report Count')
    count_report_image = fields.Float(string='Report Image')
    check_output = fields.Float(string='Check Output')
    description = fields.Char(string='Description')


class res_partner(models.Model):
    _inherit= 'res.partner'
    sam_user = fields.Char(string='SAM Username')
    sam_password = fields.Char(string='SAM Password')

class helpdesk_ticket(models.Model):
    _inherit= 'helpdesk.ticket'
    project_id = fields.Many2one('project.project', string='Project')


    def ticket_message_post(self,id=0,value={}):
        messages='Successfully'
        code=200
        self.browse(id).message_post(body=value.get('body'))
        res = {'code': code, 'messages':messages}
        return json.dumps(res)


    #Đã đưa Tạo Ticket (ID dự án, Username, Các thông tin Ticket)
    @api.model
    def set_helpdesk_ticket(self,obj,id):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            data = self.create(obj).id
        else:
            data = self.browse(id).write(obj).id

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    #Đã đưa Lấy danh sách ticket theo dự án (Id dự án)
    @api.model
    def get_helpdesk_ticket_list(self,project_id):
        messages = 'Successful'
        code = 200
        data=[]
        for i in self.search([('project_id','=',project_id)]):
            data.append({
            'id':i.id,
            'name':i.name or '',
            'team_id':i.team_id.id or 0,
            'team_name':i.team_id.name or '',
            'ticket_type_id':i.ticket_type_id.id or 0,
            'ticket_type_name':i.ticket_type_id.name or '',
            'create_date':i.create_date,
            'description':i.description or '',
            })
            res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    #Đã đưa Get thông tin Ticket(ID ticket)
    @api.model
    def get_helpdesk_ticket_detail(self, helpdesk_ticket_id):
        messages = 'Successful'
        code = 200
        data = []
        rec = self.search([('id', '=', helpdesk_ticket_id)])
        for i in rec:
            message_note = []
            for i_message in i.message_ids:
                upload = []
                for i_file in i_message.attachment_ids:
                    upload.append({
                        'id': i_file.id or 0,
                        'name': i_file.name or '',
                    })
                message_note.append({
                    'id': i_message.id,
                    'author_name': i_message.author_id.name,
                    'author_id': i_message.author_id.id,
                    'date': i_message.date,
                    'body': i_message.body,
                    'message_type': i_message.message_type,
                    'upload': upload,

                })

            data={
            'id':i.id,
            'name':i.name or '',
            'team_id':i.team_id.id or 0,
            'team_name':i.team_id.name or '',
            'ticket_type_id':i.ticket_type_id.id or 0,
            'ticket_type_name':i.ticket_type_id.name or '',
            'create_date':i.create_date,
            'description':i.description or '',
            'message_note':message_note,
            }
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

class hr_job_position(models.Model):
    _inherit= 'hr.job.position'
    active = fields.Boolean(string='active', default=True)
    description = fields.Char(string='description')
    display_names = fields.Char(string='display name')


    @api.model
    def set_project_hr_job_position(self,obj,id=0):
        messages = 'Successful'
        code=200
        data = 0


        if id ==0:
            project_id = obj.get('project_id')
            project_data = self.env['project.project'].search([('id', '=', project_id)], limit=1)
            project_data.write({'hr_job_position_ids': [(0, 0, obj)]})
            # data = self.create(obj).id
        else:
            logging.info(id)
            self.browse(id).write(obj)

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)
    # Đã đưa Get danh mục công việc
    @api.model
    def get_hr_job_position_list(self):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('active','in',(False,True,None))]):
            data.append({
                'id': i.id,
                'name': i.name,
                'description': i.description or '',
                'display_names': i.display_names or '',
                'active': i.active or False,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

class hr_department(models.Model):
    _inherit= 'hr.department'

    # Đã đưa
    @api.model
    def get_hr_department_list(self):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('active','in',(False,True,None))]):
            data.append({
                'id': i.id,
                'name': i.name,
                'code': i.code or '',
                'parent_id': i.parent_id and i.parent_id.id or 0,
                'parent_name': i.parent_id and i.parent_id.id or '',
                'back_office': i.back_office or False,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)



    @api.model
    def get_hr_department_detail(self,department_id):
        messages = 'Successful'
        code=200
        data={}
        rec = self.search([('id','=',department_id)])
        for i in rec:
            data.update({
                'id': i.id,
                'name': i.name,
                'code': i.code or '',
                'parent_id': i.parent_id and i.parent_id.id or 0,
                'parent_name': i.parent_id and i.parent_id.id or '',
                'back_office': i.back_office or False,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


class hr_attendance(models.Model):
    _inherit= 'hr.attendance'
    image_medium_1 = fields.Binary("Medium-sized image", attachment=True,
                                   help="Medium-sized image of this contact. It is automatically " \
                                        "resized as a 128x128px image, with aspect ratio preserved. " \
                                        "Use this field in form views or some kanban views.")
    image_medium_2 = fields.Binary("Medium-sized image", attachment=True,
                                   help="Medium-sized image of this contact. It is automatically " \
                                        "resized as a 128x128px image, with aspect ratio preserved. " \
                                        "Use this field in form views or some kanban views.")
    check_in_latitude = fields.Float(stirng='Check in Geo Latitude', digits=(16, 5))
    check_in_longitude = fields.Float(string='Check in Geo Longitude', digits=(16, 5))
    check_out_latitude = fields.Float(stirng='Check out Geo Latitude', digits=(16, 5))
    check_out_longitude = fields.Float(string='Check out Geo Longitude', digits=(16, 5))
    project_output_ids = fields.One2many('project.output', 'hr_attendance_id', string='Project Output')
    project_id = fields.Many2one('project.project',string='Project')

    @api.model
    def create(self, vals):
        logging.info("------------------------")
        logging.info(vals)
        logging.info("--------------------------")
        return super(hr_attendance, self).create(vals)




    @api.multi
    def btn_project_output_ids(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'project.output',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.output',
            'domain': [('project_id', 'in', self.ids)],
            "context": {
                "create": False,
                'default_project_id': self.id
            },
        }



    # Đã đưa
    @api.model
    def check_inout(self,project_id,employee_id=0):
        messages = 'Successful'
        code=200
        tmp= False
        data = self.search([('employee_id','=',employee_id),('project_id','=',project_id),('check_out','=',False)],limit=1).ids
        for i in data:
            tmp= i
        res = {'code': code, 'messages': messages, 'data': {'id':tmp or 0}}
        return json.dumps(res)    # Đã đưa
    @api.model
    def set_attendance(self,obj,id=0):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            obj.update({'check_in':datetime.now().date().strftime('%Y-%m-%d')})
            self.create(obj)
        else:
            obj.update({'check_out': datetime.now().date().strftime('%Y-%m-%d')})
            self.browse(id).write(obj)

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa Get danh sách chấm công (ID dự án)
    @api.model
    def get_hr_attendance_all(self,project_id):
        messages = 'Successful'
        code=200

        data = []
        for i in self.search([('project_id','=',project_id)]):
            # project_output_data=[]
            # for i_output in i.project_output_ids:
            #     project_output_data.append({
            #         'name':i_output.name,
            #         'id':i_output.id,
            #         'quantity':i_output.quantity or 0,
            #         'product_uom_id':i_output.product_uom_id and i_output.product_uom_id.id or 0,
            #         'product_uom_name':i_output.product_uom_id and i_output.product_uom_id.name or '',
            #         'active':i_output.active or False,
            #     })
            data.append({
                'id':i.id,
                'employee_name':i.employee_id and i.employee_id.name or '',
                'employee_id':i.employee_id and i.employee_id.id or 0,
                'check_in':i.check_in or 0,
                'check_out':i.check_out or 0,
                'duration':i.duration or 0.0,
                'department_id':i.department_id and i.department_id.id or 0,
                'department_name':i.department_id and i.department_id.name or '',
                'schedule_id':i.schedule_id and i.schedule_id.id or 0,
                'schedule_name':i.department_id and i.schedule_id.name or '',
                'leave_soon':i.leave_soon or False,
                'outside_calendar_duration':i.outside_calendar_duration or 0.0,
                'inside_calendar_duration':i.inside_calendar_duration or 0.0,
                'user_id':i.user_id.id or 0,
                'user_name':i.user_id.name or '',
                'fine_leave_soon':i.fine_leave_soon or 0.0,
                'fine':i.fine or 0.0,
                'fine_arrive_late':i.fine_arrive_late or 0.0,
                'image_medium_1':i.image_medium_1 and i.image_medium_1.decode('utf-8') or '',
                'image_medium_2':i.image_medium_2 and i.image_medium_2.decode('utf-8') or '',
                'check_in_latitude':i.check_in_latitude or 0.0,
                'check_in_longitude':i.check_in_longitude or 0.0,
                'check_out_longitude':i.check_out_longitude or 0.0,
                'check_out_latitude':i.check_out_longitude or 0.0,
                # 'project_output_data':project_output_data,
                'time_arrive_late_in_minute':i.time_arrive_late_in_minute or 0,
                'time_leave_soon_in_minute':i.time_leave_soon_in_minute or 0,
            })

        res = {'code': code, 'messages': messages, 'data': data}
        logging.info(res)
        return json.dumps(res)

    # Đã đưa
    @api.model
    def search_hr_attendance_all(self, project_id, date=''):
        messages = 'Successful'
        code = 200
        domain_from = []
        domain_to = []
        start_date = datetime.strptime(date+"-1", "%Y-%m-%d")

        end_date = (start_date.date() + relativedelta.relativedelta(months=+1, day=1, days=-1)).strftime('%Y-%m-%d')
        start_date = start_date.strftime('%Y-%m-%d')
        domain_from = [('check_in','>=',start_date)]

        domain_to = [('check_out','<=',end_date)]
        data = []
        domain = [('project_id', '=', project_id)] + domain_from + domain_to
        for i in self.search(domain):
            # project_output_data=[]
            # for i_output in i.project_output_ids:
            #     project_output_data.append({
            #         'name':i_output.name,
            #         'id':i_output.id,
            #         'quantity':i_output.quantity,
            #         'product_uom_id':i_output.product_uom_id and i_output.product_uom_id.id or 0,
            #         'product_uom_name':i_output.product_uom_id and i_output.product_uom_id.name or '',
            #         'active':i_output.active or False,
            #     })
            data.append({
                'id':i.id,
                'employee_name':i.employee_id and i.employee_id.name or '',
                'employee_id':i.employee_id and i.employee_id.id or 0,
                'check_in':i.check_in or None,
                'check_out':i.check_out or None,
                'duration':i.duration or 0.0,
                'department_id':i.department_id and i.department_id.id or 0,
                'department_name':i.department_id and i.department_id.name or '',
                'schedule_id':i.schedule_id and i.schedule_id.id or 0,
                'schedule_name':i.department_id and i.schedule_id.name or '',
                'leave_soon':i.leave_soon or False,
                'outside_calendar_duration':i.outside_calendar_duration or 0.0,
                'inside_calendar_duration':i.inside_calendar_duration or 0.0,
                'user_id':i.user_id.id or 0,
                'user_name':i.user_id.name or '',
                'fine_leave_soon':i.fine_leave_soon or 0.0,
                'fine':i.fine or 0.0,
                'fine_arrive_late':i.fine_arrive_late or 0.0,
                'image_medium_1':i.image_medium_1 or '',
                'image_medium_2':i.image_medium_2 or '',
                'check_in_latitude':i.check_in_latitude or 0.0,
                'check_in_longitude':i.check_in_longitude or 0.0,
                'check_out_longitude':i.check_out_longitude or 0.0,
                'check_out_latitude':i.check_out_longitude or 0.0,
                # 'project_output_data':project_output_data,
                'time_arrive_late_in_minute':i.time_arrive_late_in_minute or 0,
                'time_leave_soon_in_minute':i.time_leave_soon_in_minute or 0,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    # Đã đưa
    @api.model
    def get_hr_attendance_list(self,employee_id=0):
        messages = 'Successful'
        code=200

        data = []
        for i in self.search([('employee_id','=',employee_id)]):
            data.append({
                'id':i.id,
                'employee_name':i.employee_id and i.employee_id.name or '',
                'employee_id':i.employee_id and i.employee_id.id or 0,
                'check_in':i.check_in or None,
                'check_out':i.check_out or None,
                'time_arrive_late_in_minute':i.time_arrive_late_in_minute or 0,
                'time_leave_soon_in_minute':i.time_leave_soon_in_minute or 0,

            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    #Đã đưa Get danh sách chấm công theo nhân viên (ID dự án, ID Employee, thời gian)
    @api.model
    def search_hr_attendance_list(self,employee_id,date_from = '',date_to = '', project_id=0):
        messages = 'Successful'
        code=200
        domain_from=[]
        domain_to=[]
        domain_project_id=[]
        date_to=date_to+' 23:59:59'
        if date_from != '':
            domain_from = [('check_in','>=',date_from)]
        if date_to!='':
            domain_to = [('check_out','<=',date_to)]
        if project_id!=0:
            domain_project_id = [('project_id','=',project_id)]

        data = []
        domain = [('employee_id','=',employee_id)]+domain_from+domain_to+domain_project_id

        for i in self.search(domain):
            data.append({
                'id':i.id,
                'employee_name':i.employee_id and i.employee_id.name or '',
                'employee_id':i.employee_id and i.employee_id.id or 0,
                'check_in':i.check_in or None,
                'check_out':i.check_out or None,
                'time_arrive_late_in_minute':i.time_arrive_late_in_minute or 0,
                'time_leave_soon_in_minute':i.time_leave_soon_in_minute or 0,

            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_hr_attendance_detail(self,id):
        messages = 'Successful'
        code=200

        data = []
        for i in self.search([('id','=',id)]):
            # project_output_data=[]
            # for i_output in i.project_output_ids:
            #     project_output_data.append({
            #         'name':i_output.name,
            #         'id':i_output.id,
            #         'quantity':i_output.quantity,
            #         'product_uom_id':i_output.product_uom_id and i_output.product_uom_id.id or 0,
            #         'product_uom_name':i_output.product_uom_id and i_output.product_uom_id.name or '',
            #         'active':i_output.active or False,
            #     })
            data.append({
                'id':i.id,
                'employee_name':i.employee_id and i.employee_id.name or '',
                'employee_id':i.employee_id and i.employee_id.id or 0,
                'check_in':i.check_in or None,
                'check_out':i.check_out or None,
                'duration':i.duration or 0.0,
                'department_id':i.department_id and i.department_id.id or 0,
                'department_name':i.department_id and i.department_id.name or '',
                'schedule_id':i.schedule_id and i.schedule_id.id or 0,
                'schedule_name':i.department_id and i.schedule_id.name or '',
                'leave_soon':i.leave_soon or False,
                'outside_calendar_duration':i.outside_calendar_duration or 0.0,
                'inside_calendar_duration':i.inside_calendar_duration or 0.0,
                'user_id':i.user_id.id or 0,
                'user_name':i.user_id.name or '',
                'fine_leave_soon':i.fine_leave_soon or 0.0,
                'fine':i.fine or 0.0,
                'fine_arrive_late':i.fine_arrive_late or 0.0,
                'image_medium_1':i.image_medium_1 or '',
                'image_medium_2':i.image_medium_2 or '',
                'check_in_latitude':i.check_in_latitude or 0.0,
                'check_in_longitude':i.check_in_longitude or 0.0,
                'check_out_longitude':i.check_out_longitude or 0.0,
                'check_out_latitude':i.check_out_longitude or 0.0,
                # 'project_output_data':project_output_data,
                'time_arrive_late_in_minute':i.time_arrive_late_in_minute or 0,
                'time_leave_soon_in_minute':i.time_leave_soon_in_minute or 0,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)




# class mbb_attendance_line(models.Model):
#     _inherit= 'mbb.attendance.line'
#----------------

class project_member(models.Model):
    _name = 'project.member'
    project_id = fields.Many2one('project.project', string='Project')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    project_shiftis_id = fields.Many2one('project.shiftis', string='Shiftis')
    project_role = fields.Selection([('User', 'User'),
                                     ('Leader', 'Leader'),
                                     ('QLDA', 'QLDA'),
                                     ('Customer', 'Customer')],default='User', string='Role')
    project_location_id = fields.Many2one('project.locations', string='Location')
    job_position_id = fields.Many2one('hr.job.position',string='Job Position')
    start_date = fields.Date(string='Start Date', track_visibility='onchange')
    end_date = fields.Date(string='End Date', track_visibility='onchange')
    active = fields.Boolean(string='Active',default=True)

    @api.model
    def create(self, vals):
        if vals.get('employee_id') and vals.get('project_id'):
            check_data = self.search([('employee_id','=',vals.get('employee_id')),('project_id','=',vals.get('project_id'))], limit=1)
            if len(check_data.ids):
                raise Warning(_(check_data.employee_id.name+" member has been invited to review your data"))
        return super(project_member, self).create(vals)

    @api.multi
    def write(self, values):

        if values.get('employee_id'):
            check_data = self.search([('employee_id', '=', values.get('employee_id')), ('project_id', '=', self.project_id.id)], limit=1)
            # if len(check_data.ids):
            #     raise Warning(_(check_data.employee_id.name+" member has been invited to review your data"))
        return super(project_member, self).write(values)

    @api.onchange('project_id')
    def _onchange_project_id(self):
        if not self.project_id:
            return
        if self.project_id:
            employee_list=[]

            for i in self.project_id.project_member_ids:

                employee_list.append(i.employee_id.id)
            domain = {
                'employee_id': [('id', 'not in', employee_list)],
                'project_shiftis_id': [('id', 'in', self.project_id.project_shiftis_ids.ids)],
                'project_location_id': [('id', 'in', self.project_id.project_location_ids.ids)],
                'job_position_id': [('id', 'in', self.project_id.hr_job_position_ids.ids)]
            }
        return {'domain': domain}

    # Đã đưa Set nhân viên theo dự án (ID dự án, Danh sách ID Employee )
    @api.model
    def set_project_member_list(self, project_id=0, employee_ids=[]):
        messages = 'Successful'
        code = 200
        datas = []
        id = 0
        for employee_id in employee_ids:
            data = self.search([('project_id', '=', project_id), ('employee_id', '=', employee_id)], limit=1)
            if data.id:
                id = data.id
            if id == 0:
                id = self.create({
                    'project_id': project_id,
                    'employee_id': employee_id
                }).id
            datas.append(id)

        res = {'code': code, 'messages': messages}
        return json.dumps(res)

    # Đã đưa Phân công công việc cho nhân viên (ID dự án, ID Employee, ID công việc) 29-32
    @api.model
    def set_project_member_detail(self, obj, employee_id=0, project_id=0):
        messages = 'Successful'
        code = 200

        id = 0
        data = self.search([('project_id', '=', project_id), ('employee_id', '=', employee_id)], limit=1)
        if data and data.id:
            id = data.id
        if id == 0:
            code = 304
            messages = 'No Data Mapping'
        else:
            data.write(obj)
        res = {'code': code, 'messages': messages}
        return json.dumps(res)


    #Đã đưa cấm đụng đụng cắt chym cầm
    @api.model
    def create_project_member_list(self, obj=[]):
        messages = 'Successful'
        code = 200
        logging.info(obj)
        data=[]
        for i_obj in obj:
            if i_obj.get('check_id')==0:
                self.create(i_obj)
            else:
                self.browse(i_obj.get('check_id')).write(i_obj)

        res = {'code': code, 'messages': messages , 'data':data}
        return json.dumps(res)

    #Đã đưa Get danh sách nhân viên dự án (ID dự án)
    @api.model
    def get_project_member_list(self,project_id, employee_id =0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('project_id','=',project_id),('active','in',(False,True,None))]):
            data.append({
                'id':i.id,
                'project_id':i.project_id.id,
                'project_name':i.project_id.name,
                'employee_id':i.employee_id.id,
                'department_id': i.project_id.hr_department_id and i.project_id.hr_department_id.id or 0,
                'department_name': i.project_id.hr_department_id and i.project_id.hr_department_id.name or '',
                'project_role':i.project_role or '',
                'start_date':i.start_date or '0001/1/1',
                'end_date':i.end_date or '0001/1/1',
                'active':i.active or False,
                'employee_name':i.employee_id.name,
                'coach_id':i.employee_id.coach_id and i.employee_id.coach_id.id or 0,
                'coach_name':i.employee_id.coach_id and i.employee_id.coach_id.name or '',
                'employee_code':i.employee_id.employee_code or '',
                'mobile_phone':i.employee_id.mobile_phone or '',
                'birthday':i.employee_id.birthday or '0001/1/1',
                'work_email':i.employee_id.work_email or '',
                'employee_type':i.employee_id.employee_type or '',
                'project_location_id':i.project_location_id and i.project_location_id.id or 0,
                'project_location_name':i.project_location_id and i.project_location_id.name or '',
                'job_position_id':i.job_position_id and i.job_position_id.id or 0,
                'job_position_name':i.job_position_id and i.job_position_id.name or '',
                'project_shiftis_id':i.project_shiftis_id and i.project_shiftis_id.id or 0,
                'project_shiftis_name':i.project_shiftis_id and i.project_shiftis_id.name or '',
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_project_member_detail(self,member_id):
        messages = 'Successful'
        code=200
        data={}
        for i in self.search([('id','=',member_id)]):
            # data = i.read()[0]
            data.update({
                'id':i.id,
                'project_id':i.project_id.id,
                'project_name':i.project_id.name,
                'department_id':i.project_id.hr_department_id and i.project_id.hr_department_id.id or 0,
                'department_name':i.project_id.hr_department_id and i.project_id.hr_department_id.name or '',
                'employee_id':i.employee_id.id,
                'employee_name':i.employee_id.name,
                'project_role':i.project_role or '',
                'start_date':i.start_date or '0001/1/1',
                'end_date':i.end_date or '0001/1/1',
                'active':i.active or False,
                'project_location_id':i.project_location_id and i.project_location_id.id or 0,
                'project_location_name':i.project_location_id and i.project_location_id.name or '',
                'job_position_id':i.job_position_id and i.job_position_id.id or 0,
                'job_position_name':i.job_position_id and i.job_position_id.name or '',
                'project_shiftis_id':i.project_shiftis_id and i.project_shiftis_id.id or 0,
                'project_shiftis_name':i.project_shiftis_id and i.project_shiftis_id.name or '',
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)



    # Đã đưa Get role theo nhân viên (ID dự án, ID Employee)
    @api.model
    def get_employee_role_in_project(self,employee_id,project_id):
        messages = 'Successful'
        code=200
        data={}
        for i in self.search([('project_id','=',project_id),('employee_id','=',employee_id),('active','in',(False,True,None))]):
            # data = i.read()[0]
            data.update({
                'id':i.id,
                'project_id':i.project_id.id,
                'project_name':i.project_id.name,
                'department_id':i.project_id.hr_department_id and i.project_id.hr_department_id.id or 0,
                'department_name':i.project_id.hr_department_id and i.project_id.hr_department_id.name or '',
                'employee_id':i.employee_id.id,
                'employee_name':i.employee_id.name,
                'project_role':i.project_role or '',
                'start_date':i.start_date or '0001/1/1',
                'end_date':i.end_date or '0001/1/1',
                'active':i.active or False,
                'project_location_id':i.project_location_id and i.project_location_id.id or 0,
                'project_location_name':i.project_location_id and i.project_location_id.name or '',
                'job_position_id':i.job_position_id and i.job_position_id.id or 0,
                'job_position_name':i.job_position_id and i.job_position_id.name or '',
                'project_shiftis_id':i.project_shiftis_id and i.project_shiftis_id.id or 0,
                'project_shiftis_name':i.project_shiftis_id and i.project_shiftis_id.name or '',
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)



class hr_employee_leave(models.Model):
    _inherit = 'hr.employee.leave'

    # Đã đưa
    @api.model
    def get_leave_list(self,employee_id=0):
        messages = 'Successful'
        code=200
        data = self.search([('employee_id','=',employee_id)]).read()
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def search_leave_list(self,employee_id,date_from = '',date_to = ''):
        messages = 'Successful'
        code=200
        domain_from=[]
        domain_to=[]
        if date_from != '':
            domain_from = [('check_in','>=',date_from)]
        if date_to!='':
            domain_to = [('check_in','<=',date_from)]

        data = self.search([('employee_id','=',employee_id)]+domain_from+domain_to).read()
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_leave_detail(self,id):
        messages = 'Successful'
        code=200
        data = self.search([('id','=',id)]).read()[0]
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

class hr_holidays_status(models.Model):
    _inherit = 'hr.holidays.status'

    # Đã đưa
    @api.model
    def get_hr_holidays_status_list(self):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('active','in',(False,True,None))]):
            data.append({
                'id':i.id,
                'display_name':i.display_name,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

class hr_holidays(models.Model):
    _inherit = 'hr.holidays'

    @api.model
    def create(self, vals):

        logging.info("----------------------")
        logging.info(vals)
        logging.info("----------------------")
        return super(hr_holidays, self).create(vals)


    # Đã đưa Duyệt nghĩ/Từ chối nghĩ phép (ID đăng ký nghĩ phép)
    @api.model
    def action_validate_hr_holidays(self,id=0):
        messages = 'Successful'
        code=200
        data = self.browse(id)
        if data and data.id:
            data.action_validate()

        res = {'code': code, 'messages': messages}
        return json.dumps(res)

    # Đã đưa Duyệt nghĩ/Từ chối nghĩ phép (ID đăng ký nghĩ phép)
    @api.model
    def action_refuse_hr_holidays(self,id=0):
        messages = 'Successful'
        code=200
        data = self.browse(id)
        if data and data.id:
            data.action_refuse()
        res = {'code': code, 'messages': messages}
        return json.dumps(res)

    # Đã đưa Đăng ký nghĩ phép (ID dự án, ID Employee, Ngày nghĩ) 37
    @api.model
    def set_hr_holidays(self,obj,id=0):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            self.create(obj)
        else:
            self.browse(id).write(obj)

        res = {'code': code, 'messages': messages}
        return json.dumps(res)


    # Đã đưa Get danh sách ngày phép (ID dự án)
    @api.model
    def get_hr_holidays_list_all(self,project_id):
        messages = 'Successful'
        code=200
        data=[]
        employee_ids = self.env['project.project'].search_employee_list_with_project(project_id)
        for employee_id in employee_ids:
            for i in self.search([('employee_id','=',employee_id)]):
                data.append({
                    'id':i.id,
                    'create_date':i.create_date,
                    'display_name':i.display_name or '',
                    'state':i.state or '',
                    'date_from':i.date_from or '0001/1/1',
                    'date_to':i.date_to or '0001/1/1',
                    'number_of_days':i.number_of_days or 0.0,
                    'employee_name':i.employee_id and i.employee_id.name or '',
                    'employee_id':i.employee_id and i.employee_id.id or 0,
                    'holiday_status': i.holiday_status_id and i.holiday_status_id.name or '',
                    'holiday_type': i.holiday_type or '',

                })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    # Đã đưa
    @api.model
    def get_hr_holidays_list(self,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('employee_id','=',employee_id)]):
            data.append({
                'id':i.id,
                'create_date':i.create_date,
                'display_name':i.display_name or '',
                'state':i.state or '',
                'employee_name':i.employee_id and i.employee_id.name or '',
                'employee_id':i.employee_id and i.employee_id.id or 0,
                'holiday_status': i.holiday_status_id and i.holiday_status_id.name or '',
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa Get danh sách ngày phép theo nhân viên (ID dự án, ID Employee, thời gian)
    @api.model
    def search_hr_holidays_list(self,employee_id,date_from = '',date_to = ''):
        messages = 'Successful'
        code=200
        domain_from=[]
        domain_to=[]
        if date_from != '':
            domain_from = [('date_to','>=',date_from)]
        if date_to!='':
            domain_to = [('date_from','<=',date_to)]
        data=[]
        for i in self.search([('employee_id','=',employee_id)]+domain_from+domain_to):
            data.append({
                'id': i.id,
                'create_date': i.create_date,
                'display_name': i.display_name or '',
                'state': i.state or '',
                'employee_name': i.employee_id and i.employee_id.name or '',
                'employee_id': i.employee_id and i.employee_id.id or 0,
                'holiday_status': i.holiday_status_id and i.holiday_status_id.name or '',
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    #Đã đưa
    @api.model
    def search_hr_holidays_list_all(self,project_id,date_from = '',date_to = ''):
        messages = 'Successful'
        code=200
        domain_from=[]
        domain_to=[]
        if date_from != '':
            domain_from = [('date_to','>=',date_from)]
        if date_to!='':
            domain_to = [('date_from','<=',date_to)]
        data=[]
        employee_ids = self.env['project.project'].search_employee_list_with_project(project_id)
        for employee_id in employee_ids:
            for i in self.search([('employee_id','=',employee_id)]+domain_from+domain_to):
                tmp={}
                tmp=i.read()[0]
                tmp.update({
                    'id': i.id,
                    'create_date': i.create_date,
                    'display_name': i.display_name or '',
                    'state': i.state or '',
                    'employee_name': i.employee_id and i.employee_id.name or '',
                    'work_phone': i.employee_id and i.employee_id.work_phone or '',
                    'work_email': i.employee_id and i.employee_id.work_email or '',
                    'employee_id': i.employee_id and i.employee_id.id or 0,
                    'holiday_status': i.holiday_status_id and i.holiday_status_id.name or '',
                    'holiday_status': i.holiday_status_id and i.holiday_status_id.name or '',
                })
                data.append(tmp)
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    # Đã đưa
    @api.model
    def get_hr_holidays_detail(self,id):
        messages = 'Successful'
        code=200

        data=[]
        for i in self.search([('id','=',id)]):
            data.append({
                'id': i.id,
                'create_date': i.create_date,
                'display_name': i.display_name or '',
                'state': i.state or '',
                'employee_name': i.employee_id and i.employee_id.name or '',
                'employee_id': i.employee_id and i.employee_id.id or 0,
                'holiday_status': i.holiday_status_id and i.holiday_status_id.name or '',
                'date_from': i.date_from or '0001/1/1',
                'date_to': i.date_to or '0001/1/1',
                'number_of_days': i.number_of_days or 0.0,
                'holiday_type': i.holiday_type or '',
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)



class hr_employee(models.Model):
    _inherit = 'hr.employee'


    # Đã đưa
    @api.model
    def get_hr_employee_list(self):
        messages = 'Successful'
        code=200
        data=[]
        rec = self.search([])
        for i in rec:
            data.append(i.read())
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


class customer_review_account(models.Model):
    _name = 'customer.review.account'
    name = fields.Char(string='Name')
    user_login = fields.Char(string='User Name')
    user_password = fields.Char(string='User Password')

class project_project(models.Model):
    _inherit = 'project.project'

    # quickly_report_ids = fields.One2many('quickly.report','project_id')
    checkin_type = fields.Selection([
        ('barcode','Barcode'),
        ('coordinates','Coordinates'),
    ], string='Checkin Type')
    customer_user = fields.Char(related="partner_id.sam_user", string='Customer SAM Username')
    customer_password = fields.Char(related="partner_id.sam_password", string='Customer SAM Username')
    customer_login = fields.Boolean(string='Customer Login')
    customer_account = fields.Many2one('customer.review.account', string='Customer')

    quantity_report = fields.Float(string='Quantity')
    check_quantity = fields.Boolean(string='Check Quantity')
    count_report_image = fields.Float(string='Report Image')
    info_description = fields.Char(string='Description')

    hr_department_id = fields.Many2one('hr.department',string='Department')
    hr_job_position_ids = fields.Many2many('hr.job.position','pp_hjp_rel','pp_id','hjp_id',string='Job Position')
    project_location_ids = fields.Many2many('project.locations','pp_pl_rel','project_project_id','project_locations_id',string='Locations')
    project_shiftis_ids = fields.Many2many('project.shiftis','pp_ps_rel','project_project_id','project_shiftis_id',string='Shiftis', track_visibility='onchange')
    # partner_ids = fields.Many2many('res.partner',string='WebAdmin User', track_visibility='onchange')
    helpdesk_ticket_ids = fields.One2many('helpdesk.ticket','project_id', string='Ticket')
    project_member_ids = fields.One2many('project.member','project_id', string='Project Member')
    project_holidays_ids = fields.One2many('project.holidays','project_id', string='Project Holidays')
    project_output_ids = fields.One2many('project.output','project_id', string='Project Output')
    project_notification_ids = fields.One2many('project.notification','project_id', string='Project Notification')
    ticket_count = fields.Integer(string='Ticket Count', compute='_compute_ticket')


    @api.multi
    def search_employee_list_with_project(self,project_id):
        data=[]
        for i in self.env['project.member'].search([('project_id','=',project_id)]):
            data.append(i.employee_id.id)
        return data

    def check_employee_in_project(self,employee_id, project_id):
        data = self.env['project.member'].search([('project_id','=',project_id),('employee_id','=',employee_id)]).ids
        res = False
        if len(data)>0:
            res = True
        return res


    # Đã đưa
    @api.model
    def get_notifications(self,project_id,employee_id=0,special=False):
        messages = 'Successful'
        code=200
        data=[]
        specail_list=[]
        for i in self.search([('id','=',project_id),]).project_notification_ids:
            if special:
                specail_list=[]
                for i_employee in i.specail_list:
                    specail_list.append({
                        'id':i_employee.id,
                        'name':i_employee.name,
                    })
                data.append({
                    'id': i.id or 0,
                    'create_uid': i.create_uid.id or 0,
                    'create_name': i.create_uid.name or '',
                    'name': i.name or '',
                    'create_date': i.create_date or '',
                    'description': i.description or '',
                    'all': i.all or False,
                    'specail_list': specail_list,
                    'active': i.active or False,
                })
            else:
                if employee_id == 0:
                    data.append({
                        'id': i.id or 0,
                        'name': i.name or '',
                        'create_date': i.create_date or '',
                        'description': i.description or '',
                    })
                else:
                    add = False
                    if i.all:
                        add = True
                    else:
                        for specail in specail_list:
                            if specail.id == employee_id:
                                add=True
                    if add:
                        data.append({
                            'id': i.id or 0,
                            'name': i.name or '',
                            'create_uid': i.create_uid.id or 0,
                            'create_name': i.create_uid.name or '',
                            'create_date': i.create_date or '',
                            'description': i.description or '',
                        })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)
    @api.model
    def get_notifications_detail(self, notification_id ,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        res = self.env['project.notification'].search([('id', '=', notification_id)], limit=1)#, ('needaction', '=', True)])

        for i in res:
            specail_list=[]
            for i_employee in i.specail_list:
                specail_list.append({
                    'id': i_employee.id,
                    'name': i_employee.name,
                })
            data.append({
                'id': i.id or 0,
                'name': i.name or '',
                'create_date': i.create_date or '',
                'create_uid': i.create_uid.id or 0,
                'create_name': i.create_uid.name or '',
                'description': i.description or '',
                'all': i.all or False,
                'specail_list': specail_list,
                'active': i.active or False,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)



    @api.multi
    def _compute_ticket(self):
        for ticket in self:
            ticket.ticket_count = self.env['helpdesk.ticket'].search_count([('project_id', '=', self.id)])

    @api.multi
    def btn_add_member(self):
        # for this_rec in self:
        #     list_view_id = self.env['ir.model.data'].xmlid_to_res_id('helpdesk.helpdesk_tickets_view_tree')

        view_id = self.env['helpdesk.ticket'].env.ref('custom_project.view_project_member_form', False)
        logging.info(view_id)
        result = {
            'name': 'Create Project Member',
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id.id,
            'res_model': 'project.member',
            'target': 'new',

            'views': False,
            'context': {
                'default_project_id': self.id
            },
        }
        return result

    @api.multi
    def btn_open_ticket_tree(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'helpdesk.ticket',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'helpdesk.ticket',
            'domain': [('project_id', 'in', self.ids)],
            "context": {
                # "create": False,
                'default_project_id': self.id
            },

        }
    @api.multi
    def btn_open_project_holidays_tree(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'project.holidays',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.holidays',
            'domain': [('project_id', 'in', self.ids)],
            "context": {
                # "create": False,
                'default_project_id': self.id
            },
        }
    @api.multi
    def btn_open_project_output_tree(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'project.output',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.output',
            'domain': [('project_id', 'in', self.ids)],
            "context": {
                # "create": False,
                'default_project_id': self.id
            },
        }
    @api.multi
    def btn_open_project_notification_tree(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'project.notification',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'project.notification',
            'domain': [('project_id', 'in', self.ids)],
            "context": {
                # "create": False,
                'default_project_id': self.id
            },
        }


    # Đã đưa Get địa điểm làm việc của dự án (ID dự án)
    @api.model
    def get_project_location(self,project_id,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('id','=',project_id)]).project_location_ids:
            data.append(i.read()[0])
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa Get ngày nghỉ của dự án (ID dự án)
    @api.model
    def get_project_holiday(self,project_id,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('id','=',project_id)]).project_holidays_ids:
            data.append(i.read()[0])
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_project_holiday_detail(self,project_holiday_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.env['project.holidays'].search([('id','=',project_holiday_id)]):
            data.append(i.read()[0])
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    #Đã đưa Get danh sách sản lượng (ID dự án)
    @api.model
    def get_project_output(self,project_id,employee_id=0,date_from='',date_to=''):
        messages = 'Successful'
        code=200
        data=[]
        domain=[]
        employee_id_list={}
        for i in self.env['project.member'].search([('project_id','=',project_id)]):
            employee_id_list.update({i.employee_id.id:{
                                                        'employee_name':i.employee_id.name,
                                                        'employee_id':i.employee_id.id,
                                                        'project_location_id':i.project_location_id and i.project_location_id.id or 0,
                                                        'project_location_name':i.project_location_id and i.project_location_id.name or '',
                                                        'job_position_id':i.job_position_id and i.job_position_id.id or 0,
                                                        'job_position_name':i.job_position_id and i.job_position_id.name or '',
                                                        'project_shiftis_id':i.project_shiftis_id and i.project_shiftis_id.id or 0,
                                                        'project_shiftis_name':i.project_shiftis_id and i.project_shiftis_id.name or '',

                                                       }
                                    }
            )

        if employee_id == 0:
            domain=[('id', '=', project_id)]
        else:
            domain=[('id', '=', project_id),('employee_id','=',employee_id)]
        if date_from != '':
            domain.append(('create_date','>=',date_from))
        if date_to!= '':
            domain.append(('create_date', '<=', date_to))

        for i in self.search(domain).project_output_ids:
            output_image_ids=[]
            for i_image in i.output_image_ids:
                output_image_ids.append({
                    'image_medium':i_image.image_medium,
                    'name':i_image.name,
                })
            tmp = employee_id_list.get(i.employee_id.id)
            tmp.update({
                'id':i.id or 0,
                'name':i.name or '',
                'quantity':i.quantity or 0,
                'product_uom_id':i.product_uom_id and i.product_uom_id.id or 0,
                'product_uom_name':i.product_uom_id and i.product_uom_id.name or 0,
                'create_date':i.create_date,
                #'hr_attendance_id':i.hr_attendance_id and i.hr_attendance_id.id or 0,
                #'hr_attendance_name':i.hr_attendance_id and i.hr_attendance_id.name or '',
                'output_image':output_image_ids,
            })
            data.append(tmp)
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    #Đã đưa Get danh sách sản lưỡng theo nhân viên (ID dự án, ID Employee)
    @api.model
    def get_project_output_detail(self,project_output_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.env['project.output'].search([('id','=',project_output_id)]):
            output_image_ids = []
            for i_image in i.output_image_ids:
                output_image_ids.append({
                    'image_medium': i_image.image_medium,
                    'name': i_image.name,
                })

            data.append({
                'name': i.name or '',
                'quantity': i.quantity or 0,
                'create_date': i.create_date,
                'description':i.description or '',
                'employee_id': i.employee_id.id or 0,
                'employee_name': i.employee_id.name or '',
                'product_uom_id': i.product_uom_id and i.product_uom_id.id or 0,
                'product_uom_name': i.product_uom_id and i.product_uom_id.name or 0,
                # 'hr_attendance_id': i.hr_attendance_id and i.hr_attendance_id.id or 0,
                # 'hr_attendance_name': i.hr_attendance_id and i.hr_attendance_id.name or '',
                'output_image': output_image_ids,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_project_location_detail(self,location_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.env['project.locations'].search([('id','=',location_id)]):
            data.append(i.read()[0])
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    def convert_time_float_to_string(self,time):
        result = '{0:02.0f}:{1:02.0f}'.format(*divmod(time * 60, 60))
        return result

    # Đã đưa Get ca làm việc của dự án (ID dự án)
    @api.model
    def get_project_shiftis(self,project_id,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('id','=',project_id)]).project_shiftis_ids:
            data.append({
                'id': i.id,
                'name': i.name,
                'active': i.active,
                'start_time_convert': self.convert_time_float_to_string(i.start_time),
                'end_time_convert': self.convert_time_float_to_string(i.end_time),
                'start_time': i.start_time,
                'end_time': i.end_time,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_project_shiftis_detail(self,shiftis_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.env['project.shiftis'].search([('id','=',shiftis_id)]):
            data.append({
                'id': i.id,
                'name':i.name,
                'active':i.active,
                'start_time_convert':self.convert_time_float_to_string(i.start_time),
                'end_time_convert':self.convert_time_float_to_string(i.end_time),
                'start_time':i.start_time,
                'end_time':i.end_time,
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    # Đã đưa Get danh sách công việc của dự án (ID dự án)
    @api.model
    def get_job_position(self,project_id,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('id','=',project_id)]).hr_job_position_ids:
            data.append(i.read()[0])
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_job_position_detail(self,job_position_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.env['hr.job.position'].search([('id','=',job_position_id)]):
            data.append(i.read()[0])
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa Get danh sách dự án (ID của Employee)
    @api.model
    def get_project_menu(self,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.env['project.member'].search([('employee_id','=',employee_id)]):
            data.append({
                'id': i.id,
                'create_date':i.project_id.create_date,
                'phone': i.project_id.user_id and i.project_id.user_id.partner_id and i.project_id.user_id.partner_id.phone or '',
                'user_name':i.project_id.user_id and i.project_id.user_id.partner_id and i.project_id.user_id.partner_id.name or '',
                'project_id':i.project_id.id,
                'project_name':i.project_id.name,
                'count_project_shiftis_ids':len(i.project_id.project_shiftis_ids and i.project_id.project_shiftis_ids.ids or []),
                'count_project_location_ids':len(i.project_id.project_location_ids and i.project_id.project_location_ids.ids or []),
                'count_project_member_ids':len(i.project_id.project_member_ids and i.project_id.project_member_ids.ids or [])
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa Get thông tin chi tiết của dự án (ID dự án)
    @api.model
    def get_project_detail(self,project_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('id','=',project_id)]):
            tmp = i.read()[0]
            tmp.update({
                'count_job_position':len(i.hr_job_position_ids and i.hr_job_position_ids.ids or []),
                'count_location':len(i.project_location_ids and i.project_location_ids.ids or []),
                'count_shiftis':len(i.project_shiftis_ids and i.project_shiftis_ids.ids or []),
                'count_holidays':len(i.project_holidays_ids and i.project_holidays_ids.ids or []),
                'count_project_member_ids':len(i.project_member_ids and i.project_member_ids.ids or []),
                'count_notification':0,
                'project_manager':i.user_id and i.user_id.name or '',
                'phone': i.user_id and i.user_id.partner_id and i.user_id.partner_id.phone or '',
            })
            data.append(tmp)
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


class hr_employee(models.Model):
    _inherit = 'hr.employee'
    sam_user = fields.Char(string='SAM User')
    sam_password = fields.Char(string='SAM Password')
    sam_role = fields.Selection([
        ('User', 'User'),
        ('Admin', 'Admin'),
        ('Operator', 'Operator'),
    ],default='User', string='Role')




    # Đã đưa Cập nhật thông tin nhân viên (ID Employee, các thông tin của nhân viên)
    @api.model
    def set_employee(self,obj,id=0):
        messages = 'Successful'
        code=200
        data = 0
        if id ==0:
            data = self.create(obj).id
        else:
            data = self.browse(id).write(obj).id

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa
    @api.model
    def get_hr_employee_with_department_list(self,department_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('department_id','in',department_id)]):
            data.append(i.read()[0])
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    # Đã đưa Get danh sách nhân viên theo Department
    @api.model
    def get_employee_list_department(self,department_id):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('department_id','=',department_id)]):
            data.append({
                'id':i.id,
                'name':i.name,
                'city':i.city or '',
                'gender':i.gender or '',
                'employee_code':i.employee_code or '',
                'barcode':i.barcode or '',
                'mobile_phone':i.mobile_phone,
                'work_email':i.work_email or '',
                'work_phone':i.work_phone or '',
                'active':i.active or '',
            })
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)





    # Đã đưa Xử lý đăng nhập (Username, Password)
    @api.model
    def api_login(self,user='',password=''):
        messages = 'Successful'
        code=200
        data={}
        for i in self.search([('sam_user','=',user),('sam_password','=',password)], limit=1):
            data=i.read()[0]

        if data=={}:
            for i in self.env['customer.review.account'].search([('user_login','=',user),('user_password','=',password)], limit=1):
                data={
                    'id':i.id,
                    'name':i.name,
                    'is_customer':True,
                      }
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)




    # Đã đưa Get thông tin chi tiết nhân viên (ID Employee)
    @api.model
    def get_employee_detail(self,employee_id=0):
        messages = 'Successful'
        code=200
        data=[]
        for i in self.search([('id','=',employee_id)]):
            data.append(
                {
                    'id':i.id,
                    'name':i.name,
                    'mobile_phone':i.mobile_phone  or '',
                    'display_name':i.display_name   or '',
                    'barcode':i.barcode   or '',
                    'city':i.city   or '',
                    'birthday':i.birthday   or '01/01/0001',
                    'image':i.image   or '',
                    'active':i.active   or False,
                    'current_add':i.current_add   or '',
                    'identification_id':i.identification_id    or '',
                    'sam_user':i.sam_user    or '',
                    'passport_id':i.passport_id   or '',
                    'sam_role':i.sam_role   or '',
                    'work_email':i.work_email    or '',
                    'work_phone':i.work_phone    or '',
                    'place_of_birth':i.place_of_birth    or '',
                    'religion':i.religion    or '',
                    'date_start':i.date_start   or '01/01/0001',
                    'gender':i.gender     or '',
                    'marital':i.marital     or '',
                    'children':i.children     or '',
                    'permanent_add':i.permanent_add     or '',
                    'remaining_leaves':i.remaining_leaves     or '',
                    'bank_account_number':i.bank_account_number     or '',
                    'address_acc_bank':i.address_acc_bank or '',
                    'city_acc_bank':i.city_acc_bank or '',
                    'worked_years':i.worked_years or '',
                    'place_issue':i.place_issue    or '',
                    'nation_id':i.nation_id and i.nation_id.id    or 0,
                    'nation_name':i.nation_id and i.nation_id.name   or '',
                }
            )
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

    @api.model
    def search_barcode_info(self,employee_code=''):
        messages = 'Successful'
        code=200
        data={}
        for i in self.search([('employee_code','=',employee_code)]):
            data={
                'id':i.id,
                'name':i.name,
                'gender':i.gender or '',
                'mobile_phone':i.mobile_phone or '',
                'work_location':i.work_location or '',
                'work_email':i.work_email or '',
                'work_phone':i.work_phone or '',
                'scanner_code':i.scanner_code or '',
                'employee_type':i.employee_type or '',
                'barcode':i.barcode or '',
                'active':i.active or False,

            }
        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)


    # Đã đưa Đổi mật khẩu đăng nhập (ID Employee, Username, Password)
    @api.model
    def api_change_password(self,user='',old_password='',new_password=''):
        messages = 'Successful'
        code=200
        data={}
        for i in self.search([('sam_user','=',user),('sam_password','=',old_password)], limit=1):
            i.sam_password=new_password

        res = {'code': code, 'messages': messages, 'data': data}
        return json.dumps(res)

