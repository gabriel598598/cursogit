if env.user.id in (9, 8433, 8434, 19):
    AccountMoveLine = record.env['account.move.line']
    excluded_move_ids = []
    if record._context.get('suspense_moves_mode'):
        excluded_move_ids = AccountMoveLine.search(AccountMoveLine._get_suspense_moves_domain() + [('move_id', 'in', record.ids)]).mapped('move_id').ids
    for move in record:
        if move in move.line_ids.mapped('full_reconcile_id.exchange_move_id'):
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de diferencia de tipo de cambio.'))
        if move.tax_cash_basis_rec_id:
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de base de impuestos de efectivo.'))
        if move.restrict_mode_hash_table and move.state == 'posted' and move.id not in excluded_move_ids:
            raise UserError(('No puede modificar un asiento publicado de este diario porque está en modo estricto.'))
        # We remove all the analytics entries for this journal
        move.mapped('line_ids.analytic_line_ids').unlink()
    record.mapped('line_ids').remove_move_reconcile()
    record.write({'state': 'draft', 'is_move_sent': False})
else:
      raise Warning('No tiene permisos')

####------------------------------------------------------
if env.user.id.has_group(276):
    AccountMoveLine = record.env['account.move.line']
    excluded_move_ids = []
    if record._context.get('suspense_moves_mode'):
        excluded_move_ids = AccountMoveLine.search(AccountMoveLine._get_suspense_moves_domain() + [('move_id', 'in', record.ids)]).mapped('move_id').ids
    for move in record:
        if move in move.line_ids.mapped('full_reconcile_id.exchange_move_id'):
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de diferencia de tipo de cambio.'))
        if move.tax_cash_basis_rec_id:
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de base de impuestos de efectivo.'))
        if move.restrict_mode_hash_table and move.state == 'posted' and move.id not in excluded_move_ids:
            raise UserError(('No puede modificar un asiento publicado de este diario porque está en modo estricto.'))
        # We remove all the analytics entries for this journal
        move.mapped('line_ids.analytic_line_ids').unlink()
    record.mapped('line_ids').remove_move_reconcile()
    record.write({'state': 'draft', 'is_move_sent': False})
else:
      raise Warning('No tiene permisos')
#################---
if env.user.id.has_group(276):
    AccountMoveLine = record.env['account.move.line']
    excluded_move_ids = []
    if record._context.get('suspense_moves_mode'):
        excluded_move_ids = AccountMoveLine.search(AccountMoveLine._get_suspense_moves_domain() + [('move_id', 'in', record.ids)]).mapped('move_id').ids
    for move in record:
        if move in move.line_ids.mapped('full_reconcile_id.exchange_move_id'):
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de diferencia de tipo de cambio.'))
        if move.tax_cash_basis_rec_id:
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de base de impuestos de efectivo.'))
        if move.restrict_mode_hash_table and move.state == 'posted' and move.id not in excluded_move_ids:
            raise UserError(('No puede modificar un asiento publicado de este diario porque está en modo estricto.'))
        # We remove all the analytics entries for this journal
        move.mapped('line_ids.analytic_line_ids').unlink()
    record.mapped('line_ids').remove_move_reconcile()
    record.write({'state': 'draft', 'is_move_sent': False})
else:   
      raise Warning('No tiene permisos ')
  #-------------------------------prime-------------------------------------
if env.user.has_group('__export__.res_groups_277_b093c683'):
    AccountMoveLine = record.env['account.move.line']
    excluded_move_ids = []
    if record._context.get('suspense_moves_mode'):
        excluded_move_ids = AccountMoveLine.search(AccountMoveLine._get_suspense_moves_domain() + [('move_id', 'in', record.ids)]).mapped('move_id').ids
    
    for move in record:
        if move in move.line_ids.mapped('full_reconcile_id.exchange_move_id'):
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de diferencia de tipo de cambio.'))
        if move.tax_cash_basis_rec_id:
            raise UserError(('No puedes reestablecer a borrador un asiento de diario de base de impuestos de efectivo.'))
        if move.restrict_mode_hash_table and move.state == 'posted' and move.id not in excluded_move_ids:
           
            raise UserError(('No puede modificar un asiento publicado de este diario porque está en modo estricto.'))
        # We remove all the analytics entries for this journal
        move.mapped('line_ids.analytic_line_ids').unlink()
    record.mapped('line_ids').remove_move_reconcile()
    record.write({'state': 'draft', 'is_move_sent': False})
else:
      raise Warning('No tiene permisos')
