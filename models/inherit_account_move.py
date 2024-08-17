# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging

from num2words import num2words


class InheritAccountMove(models.Model):
    _inherit = "account.move"

    def number_to_words(self):
        """ convert a floating-point number to words in French """
        amount_total = float(self.amount_total)
        # Split into whole and fractional parts
        whole_part = int(amount_total)
        fractional_part = round((amount_total - whole_part) * 100)  # Get two decimal places
        # Convert both parts to words
        whole_words = num2words(whole_part, lang='fr')
        if fractional_part != 0:
            fractional_words = num2words(fractional_part, lang='fr')
            return f"{whole_words} et {fractional_words}".upper()
        else:
            return f"{whole_words}".upper()
        
    def get_stock_picking(self):
        """ return invoice stock picking """
        origin_name = self.invoice_origin
        sale_order = self.env['sale.order'].search([('name', '=', str(origin_name).strip())])
        return sale_order.picking_ids.name
    
    def get_payment_mode(self):
        """ return payment mode related to the invoice """
        payments = self.env['account.payment'].search([('ref', '=', self.name)])
        return str(payments.journal_id.name).upper() if payments else ""