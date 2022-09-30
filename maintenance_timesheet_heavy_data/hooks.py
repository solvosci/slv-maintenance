# © 2022 Solvos Consultoría Informática (<https://www.solvos.es>)
# License AGPL-3.0 (https://www.gnu.org/licenses/agpl-3.0.html)

import logging

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    """Speed up the installation of the module on an existing Odoo instance"""
    cr.execute(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='maintenance_request' AND
        column_name='timesheet_total_hours'
    """
    )
    if not cr.fetchone():
        _logger.info("Creating field timesheet_total_hours on maintenance_request")
        cr.execute(
            """
            ALTER TABLE maintenance_request
                ADD COLUMN timesheet_total_hours double precision NOT NULL DEFAULT 0.0;
        """
        )
        _logger.info("Filling timesheet_total_hours on maintenance_request start...")
        cr.execute(
            """
                UPDATE maintenance_request
                SET timesheet_total_hours=coalesce(tt.total_unit_amount, 0.0)
                FROM (
                    SELECT mr.id, SUM(aal.unit_amount) total_unit_amount
                    FROM maintenance_request mr
                    LEFT JOIN account_analytic_line aal ON aal.maintenance_request_id = mr.id
                    GROUP BY mr.id
                ) AS tt
                WHERE maintenance_request.id = tt.id
        """
        )
        _logger.info("Filling timesheet_total_hours on maintenance_request finished!")
