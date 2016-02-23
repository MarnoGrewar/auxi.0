#!/usr/bin/env python3
"""
This module provides class and functions for basic business activities.

that provides the most basic functionality:
periodically create a transaction between two specified accounts.
"""

from datetime import datetime

from auxi.modelling.financial.des import TransactionTemplate
from auxi.modelling.business.structure import Activity

__version__ = '0.2.0rc4'
__license__ = 'LGPL v3'
__copyright__ = 'Copyright 2016, Ex Mente Technologies (Pty) Ltd'
__author__ = 'Christoff Kok, Johan Zietsman'
__credits__ = ['Christoff Kok', 'Johan Zietsman']
__maintainer__ = 'Christoff Kok'
__email__ = 'christoff.kok@ex-mente.co.za'
__status__ = 'Planning'


class BasicActivity(Activity):
    """
    Represents an basic activity class that provides the most basic activity
    functionality:
    periodically create a transaction between two specified accounts.

    :param name: The name.
    :param description: The description.
    :param start: The datetime the activity should be started.
    :param end: The datetime the activity should be run until.
    :param interval: The interval of the activity.
    :param amount: The amount of an activity.
    :param tx_template: The template for the transaction.
    """

    def __init__(self, name, description=None,
                 start=datetime.min,
                 end=datetime.max,
                 interval=1,
                 amount=1000,
                 tx_template=TransactionTemplate("Unknown")):
        """
        """
        super().__init__(name,
                         description=description,
                         start=start,
                         end=end,
                         interval=interval)
        self.start_datetime = start
        self.end_datetime = end
        self.interval = interval
        self.amount = amount
        self.tx_template = tx_template

    def _meet_execution_criteria(self, ix_period):
        return super()._meet_execution_criteria(ix_period) and self.amount > 0

    def run(self, clock, generalLedger):
        """
        Execute the activity at the current clock cycle.

        :param clock: The clock containing the current execution time and
          period information.
        :param generalLedger: The general ledger into which to create the
          transactions.
        """
        if not self._meet_execution_criteria(clock.timestep_ix):
            return

        generalLedger.create_transaction(
            self.tx_template.name,
            description=self.tx_template.description,
            tx_datetime=clock.get_datetime(),
            dt_account=self.tx_template.dt_account,
            cr_account=self.tx_template.cr_account,
            source=self.path,
            amount=self.amount)

if __name__ == "__main__":
    import unittest
    from auxi.modelling.business.basic_test import BasicActivityUnitTester
    unittest.main()