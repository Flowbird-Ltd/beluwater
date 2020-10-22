# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import api, fields, models


class res_partner(models.Model):
    _inherit = 'res.partner'

    child_all_count = fields.Integer(
        'Indirect Surbordinates Count',
        compute='_compute_subordinates', store=False,
        compute_sudo=True)

    def _get_subordinates(self, parents=None):
        """
        Helper function to compute subordinates_ids.
        Get all subordinates (direct and indirect) of an partner.
        """
        if not parents:
            parents = self.env[self._name]

        indirect_subordinates = self.env[self._name]
        parents |= self
        direct_subordinates = self.child_ids - parents
        for child in direct_subordinates:
            child_subordinate = child._get_subordinates(parents=parents)
            indirect_subordinates |= child_subordinate
        return indirect_subordinates | direct_subordinates

    @api.depends('child_ids', 'child_ids.child_all_count')
    def _compute_subordinates(self):
        for partner in self:
            partner.subordinate_ids = partner._get_subordinates()
            partner.child_all_count = len(partner.subordinate_ids)

    subordinate_ids = fields.One2many('res.partner', 'parent_id', string='Subordinates',
                                      domain=[('active', '=', True)],
                                      compute_sudo=True, compute='_compute_subordinates')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: