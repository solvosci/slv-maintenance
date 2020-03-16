from odoo import _, api, SUPERUSER_ID
from datetime import datetime, timedelta


def post_init_hook(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        MaintenanceRequest = env['maintenance.request']
        rec_in_progress = MaintenanceRequest.search([
            ('stage_id.in_progress', '=', True)])
        rec_done = MaintenanceRequest.search([
            ('stage_id.done', '=', True)])
        for req in (rec_in_progress | rec_done):
            # compute start_request_datetime
            start_dt = (req.schedule_date
                        or (datetime.combine(req.request_date,
                                             req.create_date.time())
                            if req.request_date else None)
                        or req.create_date)
            if start_dt.hour == 0 \
                    and start_dt.minute == 0 \
                    and start_dt.second == 0 \
                    and req.create_date:
                # if has no time we put the create_date time
                start_dt = start_dt.replace(
                    hour=req.create_date.hour,
                    minute=req.create_date.minute,
                    second=req.create_date.second)
            # compute end_request_datetime
            end_dt = None
            if req.stage_id.done:
                theo_end_dt = (start_dt + timedelta(hours=req.duration)) \
                    if req.duration else req.write_date
                end_dt = datetime.combine(req.close_date,
                                          theo_end_dt.time())\
                    if req.close_date else theo_end_dt
                # End dt cannot be prior to Start dt
                if end_dt < start_dt:
                    end_dt = (start_dt + timedelta(hours=req.duration)) \
                        if req.duration else start_dt
            req.write({
                'start_request_datetime': start_dt,
                'end_request_datetime': end_dt,
            })
