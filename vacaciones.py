# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
#for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)

def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
#today = '2023-06-03'
for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to','>',today),('employee_id','=',empl_id)])
      dias_vigentes = max_periodo.number_of_days_display
      date_to = (to_cancel.date_to).year
      number_of_days = to_cancel.number_of_days_display
      #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
      record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
      name = to_cancel.employee_id.display_name
      remain = round(record.virtual_remaining_leaves, 2) or 0.0
      total = round(record.max_leaves, 2) or 0.0
      #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
      if remain <= 0:
        continue
      #days_to_cancel = number_of_days-(total-remain)
      days_to_cancel = remain - dias_vigentes
      if days_to_cancel > 0:
          msg += '%s,%s,%s,%s,%s,%s,%s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
          i += 1
          date_from = to_cancel.date_to
          date_to = date_from + datetime.timedelta((days_to_cancel-1))
          while model._check_date(date_from, date_to, employee.id):
              date_from = date_to
              date_to = date_from + datetime.timedelta((days_to_cancel-1))
          vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
          }
          try:
            leave = env['hr.leave'].sudo().create(vals)
          except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel))
          leave._onchange_employee_id()
          leave.action_approve()
          leave.action_validate()
#raise Warning(msg)
#raise Warning(empls)
#---------------------------------------------------------------------------------------------------------------------
# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
#for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)

def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
for employee in employee_ids:
  alloc_ids = model.search([('employee_id','=',employee.id),('parent_id','=',False)])
  if len(alloc_ids) > 1:
    parent_id = min(alloc_ids.ids)
    alloc_ids -= model.browse(parent_id)
    alloc_ids.write({'parent_id':parent_id})
    #raise UserError('alloc_ids: %s, parent_id: %s'%(alloc_ids, parent_id))
  date = employee.cfdi_date_contract.replace(year=today.year)    # 2019-04-30 => 2021-04-30
  if date <= today:
    delta = today.year - employee.cfdi_date_contract.year             
    if env['hr.leave.allocation'].search([('employee_id','=',employee.id),('year','=',delta)]):
      continue
    if not employee.contract_id.date_start:
      continue
    try:
        count = env['hr.leave.allocation'].create_allocation(employee, today, table_ids, period, m=18, count=count)
    except:
        raise UserError('*******\nemployee: %s, today: %s, table_ids: %s, period: %s, count: %s'%(employee, today, table_ids, period, count))
    
    
    #------------------------------------------------27/10/23--------------------------------#
    
    
    # Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#   model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)

def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
#today = '2023-06-03'
for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to','>',today),('employee_id','=',empl_id)])
      dias_vigentes = max_periodo.number_of_days_display
      date_to = (to_cancel.date_to).year
      number_of_days = to_cancel.number_of_days_display
      #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
      record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
      name = to_cancel.employee_id.display_name
      remain = round(record.virtual_remaining_leaves, 2) or 0.0
      total = round(record.max_leaves, 2) or 0.0
      #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
      if remain <= 0:
        continue
      #days_to_cancel = number_of_days-(total-remain)
      days_to_cancel = remain - dias_vigentes
      if days_to_cancel > 0:
          msg += '%s,%s,%s,%s,%s,%s,%s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
          i += 1
          date_from = to_cancel.date_to
          date_to = date_from + datetime.timedelta((days_to_cancel-1))
          while model._check_date(date_from, date_to, employee.id):
              date_from = date_to
              date_to = date_from + datetime.timedelta((days_to_cancel-1))
          vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id':employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
          }
          try:
            leave = env['hr.leave'].sudo().create(vals)
          except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel))
          leave._onchange_employee_id()
          leave.action_approve()
          leave.action_validate()
raise Warning(domain)
#raise Warning(empls)





#---------------------------------------------30/10/23-------------------------------------------------------#

# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#   model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)

def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
#today = '2023-06-03'
for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to','>',today),('employee_id','=',empl_id)])
      dias_vigentes = max_periodo.number_of_days_display
      date_to = (to_cancel.date_to).year
      number_of_days = to_cancel.number_of_days_display
      #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
      record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
      name = to_cancel.employee_id.display_name
      remain = round(record.virtual_remaining_leaves, 2) or 0.0
      total = round(record.max_leaves, 2) or 0.0
      #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
      if remain <= 0:
        continue
      #days_to_cancel = number_of_days-(total-remain)
      days_to_cancel = remain - dias_vigentes
      if days_to_cancel > 0:
         remaining_days = remain  # Obtén los días restantes de vacaciones
         if days_to_cancel <= remaining_days:
            msg += '%s,%s,%s,%s,%s,%s,%s\n' % (employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            # Restar los días a cancelar de los días restantes
            remain -= days_to_cancel
 
            # Resto de tu código para crear y validar la solicitud de vacaciones
            vals = {
                 'holiday_status_id': record.id,
                 'request_date_from': date_from,
                 'request_date_to': date_to,
                 'date_from': date_from,
                 'date_to': date_to,
                 'name': u'PRESCRITO',
                 'employee_id': employee.id,
                 'number_of_days': days_to_cancel,
                 'state': 'confirm',
                 'mode_company_id': employee.company_id.id
            }
            try:
                leave = env['hr.leave'].sudo().create(vals)
            except Exception as e:
                raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s' % (e, employee, i, remain, total, number_of_days, days_to_cancel))
            leave._onchange_employee_id()
            leave.action_approve()
            leave.action_validate()
         else:
            raise Warning('Los días a cancelar exceden los días restantes de vacaciones.')
        
        #--------------------------------------30/10/23 v2 trae datos  raise ---------#
        
# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)

def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
#today = '2023-06-03'
for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to','>',today),('employee_id','=',empl_id)])
      dias_vigentes = max_periodo.number_of_days_display
      date_to = (to_cancel.date_to).year
      number_of_days = to_cancel.number_of_days_display
      #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
      record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
      name = to_cancel.employee_id.display_name
      remain = round(record.virtual_remaining_leaves, 2) or 0.0
      total = round(record.max_leaves, 2) or 0.0
      #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
      if remain <= 0:
        continue
      #days_to_cancel = number_of_days-(total-remain)
      days_to_cancel = remain - dias_vigentes
      if days_to_cancel > 0:
          msg += '%s,%s,%s,%s,%s,%s,%s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
          i += 1
          date_from = to_cancel.date_to
          date_to = date_from + datetime.timedelta((days_to_cancel-1))
          while model._check_date(date_from, date_to, employee.id):
              date_from = date_to
              date_to = date_from + datetime.timedelta((days_to_cancel-1))
          vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
          }
          try:
            leave = env['hr.leave'].sudo().create(vals)
          except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel))
          leave._onchange_employee_id()
          leave.action_approve()
          leave.action_validate()
raise Warning(name)
#raise Warning(empls)


#-----------------------06/11/2023-----------------------------------------

# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)


def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365
  
           
#def _check_date(self, date_from, date_to, employee_id):
#  domain = [
#  ('date_from', '<', date_to),
#  ('date_to', '>', date_from),
#  ('employee_id', '=', employee_id),
#  ('state', 'not in', ['cancel', 'refuse']),
#]
#  return self.env['hr.leave'].search_count(domain)
 
max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
#today = '2023-06-03'

for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  if to_cancel:
      # debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to', '>', today), ('employee_id', '=', empl_id)])
      for max_periodo_record in max_periodo:
        dias_vigentes = max_periodo.number_of_days_display
        date_to = (to_cancel.date_to).year
        number_of_days = to_cancel.number_of_days_display
        #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
        record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
        name = to_cancel.employee_id.display_name
        remain = round(record.virtual_remaining_leaves, 2) or 0.0
        total = round(record.max_leaves, 2) or 0.0
        # empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        raise Warning(remain)
        if remain <= 0:
          continue
        #days_to_cancel = number_of_days-(total-remain)
        days_to_cancel = remain - dias_vigentes
        if days_to_cancel > 0:
            msg += '%s,%s,%s,%s,%s,%s,%s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            i += 1
            date_from = to_cancel.date_to
            date_to = date_from + datetime.timedelta((days_to_cancel-1))
            #raise Warning(name)
            while model._check_date(date_from, date_to, employee.id):
              date_from = date_to
              date_to = date_from + datetime.timedelta((days_to_cancel-1))
              #raise Warning(msg)
        vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
          }
        try:
            leave = env['hr.leave'].sudo().create(vals)
        except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
        
####-------------------------08/11/2023--------------------------------
###---------------------------ultimate--------------

# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)


def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365
  

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
#today = '2023-11-09'

for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  #raise Warning(to_cancel)
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to', '>', today), ('employee_id', '=', empl_id)])
      for max_periodo_record in max_periodo:
        dias_vigentes = max_periodo.number_of_days_display
        date_to = (to_cancel.date_to).year
        number_of_days = to_cancel.number_of_days_display
        #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
        record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
        name = to_cancel.employee_id.display_name
        remain = round(record.virtual_remaining_leaves, 2) or 0.0
        total = round(record.max_leaves, 2) or 0.0
        #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        #raise Warning(to_cancel)
        if remain <= 0:
          continue
        #days_to_cancel = number_of_days-(total-remain)
        days_to_cancel = remain - dias_vigentes
        #raise Warning(days_to_cancel)
        if days_to_cancel > 0:
            msg += '%s,%s,%s,%s,%s,%s,%s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            i += 1
            date_from = to_cancel.date_to
            date_to = date_from + datetime.timedelta((days_to_cancel-1))
            #raise Warning()
            while model._check_date(date_from, date_to, employee.id):
              date_from = date_to
              date_to = date_from + datetime.timedelta((days_to_cancel-1))
              #raise Warning(g)
            vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
             }
            #raise Warning(employee.id)            
        try:
            leave = env['hr.leave'].sudo().create(vals)
        except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
# raise Warning(vals)

#-----------------------------15/11/2023------------------------
# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)


def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365
raise Warning( anhos_servicio)

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
today = '2023-11-16'

for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  #to_cancel = model.search([('date_to','=',today),('employee_id','=',employee.id)])
  #raise Warning(employee.id)
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to', '>', today), ('employee_id', '=', empl_id)])
      for max_periodo_record in max_periodo:
        dias_vigentes = max_periodo.number_of_days_display
        date_to = (to_cancel.date_to).year
        number_of_days = to_cancel.number_of_days_display
        #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
        record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
        name = to_cancel.employee_id.display_name
        remain = round(record.virtual_remaining_leaves, 2) or 0.0
        total = round(record.max_leaves, 2) or 0.0
        empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        raise Warning(empls)
        if remain <= 0:
          continue
        #days_to_cancel = number_of_days-(total-remain)
        days_to_cancel = remain - dias_vigentes
        #raise Warning(days_to_cancel)
        if days_to_cancel > 0:
            msg += '%s, %s, %s,  %s,  %s,  %s, %s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            i += 1
            date_from = to_cancel.date_to
            date_to = date_from + datetime.timedelta((days_to_cancel-1))
            #raise Warning(msg)
            while model._check_date(date_from, date_to, employee.id):
              date_from = date_to
              date_to = date_from + datetime.timedelta((days_to_cancel-1))
              #raise Warning(employee.id)
            vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
             }
            #raise Warning(employee.id)            
        try:
            leave = env['hr.leave'].sudo().create(vals)
        except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
# raise Warning(vals)

#------------------17-11-2023---------------------------------------------------
# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
# msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
# period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
# one_age = today - datetime.timedelta(days=365)

msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today(), []
one_age = today - datetime.timedelta(days=365)


def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365
#raise Warning( anhos_servicio)

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),

]
employee_ids = env['hr.employee'].search(domain)
#raise Warning(employee_ids)
today = '2023-11-01'

for employee in employee_ids:
  #to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  to_cancel = model.search([('date_to','=',today),('employee_id','=',employee.id)])
  #raise Warning(to_cancel)
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to', '>', today), ('employee_id', '=', empl_id)])
      #raise Warning(max_periodo)
      for max_periodo_record in max_periodo:
        dias_vigentes = max_periodo.number_of_days_display
        date_to = (to_cancel.date_to).year
        number_of_days = to_cancel.number_of_days_display
        #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
        record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
        name = to_cancel.employee_id.display_name
        remain = round(record.virtual_remaining_leaves, 2) or 0.0
        total = round(record.max_leaves, 2) or 0.0
        #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        #raise Warning(name)
        if remain <= 0:
          continue
        #days_to_cancel = number_of_days-(total-remain)
        days_to_cancel = remain - dias_vigentes
        #raise Warning(days_to_cancel)
        if days_to_cancel > 0:
            msg += '%s, %s, %s,  %s,  %s,  %s, %s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            i += 1
            date_from = to_cancel.date_to
            date_to = date_from + datetime.timedelta((days_to_cancel-1))
            #raise Warning(msg)
            while model._check_date(date_from, date_to, employee.id):
              date_from = date_to
              date_to = date_from + datetime.timedelta((days_to_cancel-1))
              #raise Warning(employee.id)
            vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
             }
            #raise Warning(employee.id)            
        try:
            leave = env['hr.leave'].sudo().create(vals)
        except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
# raise Warning(vals)

#----------------------------2023/11/22-------------------------------------------

# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)


def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365
#raise Warning( anhos_servicio)

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
]
employee_ids = env['hr.employee'].search(domain)
today = '2023-11-01'
#today = datetime.datetime(2023, 11, 1, 11, 0, 4)
#raise Warning (employee_ids)

for employee in employee_ids:
  #to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  #to_cancel = model.search([('date_to': "2022-05-01",'=',datetime.datetime(2023, 11, 1, 0, 0, 0)),('date_to': "2023-11-01",'>=',datetime.datetime(2023, 11, 1, 0, 0, 0)),('employee_id','=',employee.id)])
  to_cancel = model.search([('date_to','=',today),('employee_id','=',employee.id)])
  raise Warning( employee_ids)
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to', '>', today), ('employee_id', '=', empl_id)])
      #raise Warning(date_to)
      for max_periodo_record in max_periodo:
        dias_vigentes = max_periodo.number_of_days_display
        date_to = (to_cancel.date_to).year
        number_of_days = to_cancel.number_of_days_display
        #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
        record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
        name = to_cancel.employee_id.display_name
        remain = round(record.virtual_remaining_leaves, 2) or 0.0
        total = round(record.max_leaves, 2) or 0.0
        #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        raise Warning(name)
        if remain <= 0:
          continue
        #days_to_cancel = number_of_days-(total-remain)
        days_to_cancel = remain - dias_vigentes
        #raise Warning(days_to_cancel)
        if days_to_cancel > 0:
            msg += '%s, %s, %s,  %s,  %s,  %s, %s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            i += 1
            date_from = to_cancel.date_to
            date_to = date_from + datetime.timedelta((days_to_cancel-1))
            while model._check_date(date_from, date_to, employee.id):
                date_from = date_to
                date_to = date_from + datetime.timedelta((days_to_cancel-1))
            vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
             }
            #raise Warning(employee.id)            
        try:
            leave = env['hr.leave'].sudo().create(vals)
        except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
        
#--------------------------------------------24/11/2023 viernes------------------------
# Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)


def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365
#raise Warning( anhos_servicio)

def _check_date(self, date_from, date_to, employee_id):
  domain = [
  ('date_from', '<', date_to),
  ('date_to', '>', date_from),
  ('employee_id', '=', employee_id),
  ('state', 'not in', ['cancel', 'refuse']),
]
  return self.env['hr.leave'].search_count(domain)

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
  
]
employee_ids = env['hr.employee'].search(domain)
today = '2023-11-01'
#today = datetime.datetime(2023, 11, 1, 11, 0, 4)
#raise Warning (employee_ids)


for employee in employee_ids:
  #to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  #to_cancel = model.search([('date_to': "2022-05-01",'=',datetime.datetime(2023, 11, 1, 0, 0, 0)),('date_to': "2023-11-01",'>=',datetime.datetime(2023, 11, 1, 0, 0, 0)),('employee_id','=',employee.id)])
  to_cancel = model.search([('date_to','=',today),('employee_id','=',employee.id)])
  #raise Warning( employee_ids)
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to', '>', today),('employee_id', '=', empl_id)])
      #raise Warning(empl_id)
      for max_periodo_record in max_periodo:
        dias_vigentes = max_periodo.number_of_days_display
        date_to = (to_cancel.date_to).year
        number_of_days = to_cancel.number_of_days_display
        #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
        record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
        name = to_cancel.employee_id.display_name
        remain = round(record.virtual_remaining_leaves, 2) or 0.0
        total = round(record.max_leaves, 2) or 0.0
        #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        #raise Warning(empl_id)
        if remain <= 0:
          continue
        days_to_cancel = remain - dias_vigentes
        #raise Warning(days_to_cancel)
        if days_to_cancel > 0:
            msg += '%s, %s, %s,  %s,  %s,  %s, %s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            i += 1
            date_from = to_cancel.date_to
            date_to = date_from + datetime.timedelta((days_to_cancel-1))
            #raise Warning(to_cancel.name)
            while model._check_date(date_from, date_to, employee.id):
                date_from = date_to
                date_to = date_from + datetime.timedelta((days_to_cancel-1)) 
            # while model._check_date(date_from, date_to, employee.id):
            #     date_from = date_to + datetime.timedelta(1)
            #     date_to = date_from + datetime.timedelta((days_to_cancel-1))
            # while model._check_date(date_from, date_to, employee.id) > 0 and model.state == 'draft':
            #       date_from = date_to + datetime.timedelta(1)
            #       date_to = date_to + datetime.timedelta((days_to_cancel-1))
            vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
             }
            #raise Warning(record.id)            
        try:
            leave = env['hr.leave'].sudo().create(vals)
        except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
        
        #####.-----------------------------------------
        # Asignación inicial de allocation
# period: el periódo anterior de allocation
# m: los meses de duración del período
# for period in [0]:
#    model.process_initial_allocation(period, m=18, limit=500)
# Asignación de Vacaciones
msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)


def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365
#raise Warning( anhos_servicio)

# def _check_date(self, date_from, date_to, employee_id):
#   domain = [
#   ('date_from', '<', date_to),
#   ('date_to', '>', date_from),
#   ('employee_id', '=', employee_id),
#   ('state', 'not in', ['cancel', 'refuse']),
# ]
#   return self.env['hr.leave'].search_count(domain)

max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])
domain = [
  ('active','=',True),
  ('contract_id.state','=','open'),
  ('cfdi_date_contract','!=',False),
  ('cfdi_date_contract','<',one_age),
  
]
employee_ids = env['hr.employee'].search(domain)
today = '2023-11-01'
#today = datetime.datetime(2023, 11, 1, 11, 0, 4)
#raise Warning (employee_ids)


for employee in employee_ids:
  #to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
  #to_cancel = model.search([('date_to': "2022-05-01",'=',datetime.datetime(2023, 11, 1, 0, 0, 0)),('date_to': "2023-11-01",'>=',datetime.datetime(2023, 11, 1, 0, 0, 0)),('employee_id','=',employee.id)])
  to_cancel = model.search([('date_to','=',today),('employee_id','=',employee.id)])
  #raise Warning( employee_ids)
  if to_cancel:
      #debug = '%s,%s,%s,%s,%s\n'%(to_cancel.employee_id.name, to_cancel.date_to, to_cancel.date_from, to_cancel.duration_display, to_cancel.number_of_days_display)
      empl_id = to_cancel.employee_id.id
      max_periodo = model.search([('date_to', '>', today),('employee_id', '=', empl_id)])
      #raise Warning(empl_id)
      for max_periodo_record in max_periodo:
        dias_vigentes = max_periodo.number_of_days_display
        date_to = (to_cancel.date_to).year
        number_of_days = to_cancel.number_of_days_display
        #record = to_cancel.holiday_status_id.with_context(employee_id=employee.id)
        record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
        name = to_cancel.employee_id.display_name
        remain = round(record.virtual_remaining_leaves, 2) or 0.0
        total = round(record.max_leaves, 2) or 0.0
        #empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        #raise Warning(empl_id)
        if remain <= 0:
          continue
        days_to_cancel = remain - dias_vigentes
        
        #raise Warning(days_to_cancel)
        if days_to_cancel > 0:
            msg += '%s, %s, %s,  %s,  %s,  %s, %s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
            i += 1
            date_from = to_cancel.date_to
            date_to = date_from + datetime.timedelta((days_to_cancel-1))
            #raise Warning(to_cancel.name)
            while model._check_date(date_from, date_to, employee.id):
                date_from = date_to
                date_to = date_from + datetime.timedelta((days_to_cancel-1)) 
            # while model._check_date(date_from, date_to, employee.id):
            #     date_from = date_to + datetime.timedelta(1)
            #     date_to = date_from + datetime.timedelta((days_to_cancel-1))
            # while model._check_date(date_from, date_to, employee.id) > 0 and model.state == 'draft':
            #       date_from = date_to + datetime.timedelta(1)
            #       date_to = date_to + datetime.timedelta((days_to_cancel-1))
            vals = {
              'holiday_status_id': record.id,
              'request_date_from': date_from,
              'request_date_to': date_to,
              'date_from': date_from,
              'date_to': date_to,
              'name': u'PRESCRITO',
              'employee_id': employee.id,
              'number_of_days': days_to_cancel,
              'state': 'confirm',
              'mode_company_id': employee.company_id.id
             }
            #raise Warning(record.id)            
        try:
            leave = env['hr.leave'].sudo().create(vals)
        except Exception as e:
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()