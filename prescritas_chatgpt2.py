msg = 'Empleado,Asignación,Vencimiento,Días,Restantes,total,días a cancelar\n'
period, m, count, i, today, empleados = 0, 18, 0, 0, datetime.datetime.today().date(), []
one_age = today - datetime.timedelta(days=365)

def anhos_servicio(emp):
  cfdi_date_start = emp.cfdi_date_contract or today
  cfdi_date_end = emp.cfdi_date_end or today
  return (cfdi_date_end - cfdi_date_start).days / 365

# Se busca la secuencia máxima en la tabla hr.leave.allocation.table
max_seq = max(env['hr.leave.allocation.table'].sudo().search([]).mapped('sequence'))
table_ids = env['hr.leave.allocation.table'].sudo().search([('sequence','=',max_seq)])

# Se crea un dominio de búsqueda para encontrar empleados que cumplan con ciertas condiciones
domain = [
  ('active', '=', True),
  ('contract_id.state', '=', 'open'),
  ('cfdi_date_contract', '!=', False),
  ('cfdi_date_contract', '<', one_age),
]

# Se busca a los empleados que cumplen con el dominio
employee_ids = env['hr.employee'].search(domain)

# Bucle para procesar a los empleados
for employee in employee_ids:
  # Se busca registros de vacaciones que deben cancelarse para el día actual
  to_cancel = model.search([('date_to', '<=', today), ('date_to', '>=', today), ('employee_id', '=', employee.id)])

  if to_cancel:
    empl_id = to_cancel.employee_id.id
    max_periodo = model.search[('date_to', '>', today), ('employee_id', '=', empl_id)]
    
    for max_periodo_record in max_periodo:
      dias_vigentes = max_periodo.number_of_days_display
      date_to = (to_cancel.date_to).year
      number_of_days = to_cancel.number_of_days_display
      record = to_cancel.holiday_status_id.with_context(employee_id=empl_id)
      name = to_cancel.employee_id.display_name
      remain = round(record.virtual_remaining_leaves, 2) or 0.0
      total = round(record.max_leaves, 2) or 0.0
      
      if remain <= 0:
        continue
      
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
          raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel, name))
        
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
#--------------------07/11/2013------------------------------
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
#today = '2023-11-06'
for employee in employee_ids:
  to_cancel = model.search([('date_to','<=',today),('date_to','>=',today),('employee_id','=',employee.id)])
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
        # empls = '%s %s %s %s,\n%s'%(to_cancel.employee_id,number_of_days,total,remain,empls)
        #raise Warning(number_of_days)
        if remain <= 0:
          continue
        #days_to_cancel = number_of_days-(total-remain)
        days_to_cancel = remain - dias_vigentes
        if days_to_cancel > 0:
            #msg += '%s,%s,%s,%s,%s,%s,%s\n'%(employee.cfdi_code_emp, to_cancel.name, to_cancel.date_to.date(), number_of_days, remain, total, days_to_cancel)
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
            raise Warning('%s\n%s\nto_cancel: %s\nremain: %s\ntotal: %s\nnumber_of_days: %s\ndays_to_cancel: %s\nnombre: %s'%(e, employee, i, remain, total, number_of_days, days_to_cancel,name))
        leave._onchange_employee_id()
        leave.action_approve()
        leave.action_validate()
# raise Warning(vals)

#####################################################


