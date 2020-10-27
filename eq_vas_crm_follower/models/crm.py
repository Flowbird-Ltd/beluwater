# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################

from odoo import api, fields, models, _


class crm_lead(models.Model):
    _inherit = 'crm.lead'

    def write(self, vals):
        return super(crm_lead, self.with_context(mail_auto_subscribe_no_notify=True)).write(vals)

    @api.returns('mail.message', lambda value: value.id)
    def message_post(self, **kwargs):
        ctx = {'mail_post_autofollow': False,
               'from_crm_auto_not_send_mail': True}
        res = super(crm_lead, self.with_context(ctx)).message_post(**kwargs)
        return res


class mail_compose_message(models.TransientModel):
    _inherit = 'mail.compose.message'

    @api.model
    def default_get(self, field_lst):
        res = super(mail_compose_message, self).default_get(field_lst)
        if res.get('model') == 'crm.lead' and res.get('res_id'):
            res.update({'partner_ids': [(6, 0, [])]})
        return res


class mail_message(models.Model):
    _inherit = 'mail.message'

    def update_crm_msg_mail_data(self):
        if self.env.context.get('dont_send_mail_to_follower'):
            for each in self:
                if each.model == 'crm.lead' and each.message_type == 'comment':
                    all_partner = each.notified_partner_ids
                    for partner_id in all_partner:
                        if partner_id not in each.partner_ids:
                            each.notified_partner_ids -= partner_id
                            self._cr.execute("""delete from mail_message_res_partner_needaction_rel where
                                res_partner_id = %s 
                                and mail_message_id = %s 
                            """ % (partner_id.id, each.id))
                            self._cr.commit()
                    for each_mail in each.mail_ids:
                        each_mail.write({'recipient_ids': [(6, 0, each.partner_ids.ids)]})


class Followers(models.Model):
    _inherit = 'mail.followers'

    def _get_recipient_data(self, records, message_type, subtype_id, pids=None, cids=None):
        if self.env.context.get('from_crm_auto_not_send_mail'):
            subtype_id = False
        res = super(Followers, self)._get_recipient_data(records=records, message_type=message_type, subtype_id=subtype_id, pids=pids, cids=cids)
        return res
