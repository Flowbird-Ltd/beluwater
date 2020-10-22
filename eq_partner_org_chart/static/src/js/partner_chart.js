odoo.define('eq_partner_org_chart.OrgChart', function (require) {
"use strict";

var AbstractField = require('web.AbstractField');
var concurrency = require('web.concurrency');
var core = require('web.core');
var field_registry = require('web.field_registry');
var session = require('web.session');

var QWeb = core.qweb;

var FieldOrgChart = AbstractField.extend({
    events: {
        "click .o_partner_redirect": "_onPartnerRedirect",
        "click .o_partner_sub_redirect": "_onPartnerSubRedirect",
        "click .o_partner_more_managers": "_onPartnerMoreManager"
    },

    init: function (parent, options) {
        this._super.apply(this, arguments);
        this.dm = new concurrency.DropMisordered();
        this.partner = null;
    },

    _getOrgData: function () {
        var self = this;
        return this.dm.add(this._rpc({
            route: '/partner/get_org_chart',
            params: {
                partner_id: this.partner,
                context: session.user_context,
            },
        })).then(function (data) {
            return data;
        });
    },

    _getSubordinatesData: function (parnter_id, type) {
        return this.dm.add(this._rpc({
            route: '/partner/get_subordinates',
            params: {
                partner_id: parnter_id,
                subordinates_type: type,
                context: session.user_context,
            },
        }));
    },

    _render: function () {
        if (!this.recordData.id) {
            return this.$el.html(QWeb.render("contact_org_chart", {
                managers: [],
                children: [],
            }));
        }
        else if (!this.partner) {
            this.partner = this.recordData.id;
        }

        var self = this;
        return this._getOrgData().then(function (orgData) {
            if (_.isEmpty(orgData)) {
                orgData = {
                    managers: [],
                    children: [],
                }
            }
            orgData.view_partner_id = self.recordData.id;
            self.$el.html(QWeb.render("contact_org_chart", orgData));
            self.$('[data-toggle="popover"]').each(function () {
                $(this).popover({
                    html: true,
                    title: function () {
                        var $title = $(QWeb.render('orgchart_contact_popover_title', {
                            partner: {
                                name: $(this).data('part-name'),
                                id: $(this).data('part-id'),
                            },
                        }));
                        $title.on('click',
                            '.o_partner_redirect', _.bind(self._onPartnerRedirect, self));
                        return $title;
                    },
                    container: this,
                    placement: 'left',
                    trigger: 'focus',
                    content: function () {
                        var $content = $(QWeb.render('orgchart_res_partner_popover_content', {
                        	partner: {
                                id: $(this).data('part-id'),
                                name: $(this).data('part-name'),
                                direct_sub_count: parseInt($(this).data('part-dir-subs')),
                                indirect_sub_count: parseInt($(this).data('part-ind-subs')),
                            },
                        }));
                        $content.on('click',
                            '.o_partner_sub_redirect', _.bind(self._onPartnerSubRedirect, self));
                        return $content;
                    },
                    template: QWeb.render('orgchart_res_partner_popover', {}),
                });
            });
        });
    },

    _onPartnerMoreManager: function(event) {
        event.preventDefault();
        this.partner = parseInt($(event.currentTarget).data('partner-id'));
        this._render();
    },

    /**
     * Redirect to the Partner form view.
     */
    _onPartnerRedirect: function (event) {
        var self = this;
        event.preventDefault();
        var partner_id = parseInt($(event.currentTarget).data('partner-id'));
        return this._rpc({
            model: 'res.partner',
            method: 'get_formview_action',
            args: [partner_id],
        }).then(function(action) {
            return self.do_action(action); 
        });
    },

    /**
     * Redirect to the Child partner form view.
     */
    _onPartnerSubRedirect: function (event) {
        event.preventDefault();
        var partner_id = parseInt($(event.currentTarget).data('partner-id'));
        var type = $(event.currentTarget).data('type') || 'direct';
        var self = this;
        if (partner_id) {
            this._getSubordinatesData(partner_id, type).then(function(data) {
                var domain = [['id', 'in', data]];
                return self._rpc({
                    model: 'res.partner',
                    method: 'get_formview_action',
                    args: [partner_id],
                }).then(function(action) {
                    action = _.extend(action, {
                        'view_mode': 'kanban,list,form',
                        'views':  [[false, 'kanban'], [false, 'list'], [false, 'form']],
                        'domain': domain,
                    });
                    return self.do_action(action); 
                });
            });
        }
    },
});

field_registry.add('contact_org_chart', FieldOrgChart);

return FieldOrgChart;

});