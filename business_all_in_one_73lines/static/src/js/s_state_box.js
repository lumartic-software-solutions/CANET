odoo.define('business_all_in_one_73lines.s_counter_text', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');
    var s_animation = require('web_editor.snippets.animation');

    var QWeb = core.qweb;

    ajax.loadXML('/business_all_in_one_73lines/static/src/xml/s_state_counter_setting.xml', core.qweb);

    s_options.registry.js_state_section = s_options.Class.extend({
        start: function(){
            var self = this;
        },
        state_opt: function (type, value, $li) {
            if (type !== 'click')  return;
            var self = this;
            self.$modal = $(QWeb.render("business_all_in_one_73lines.s_counter_text"));
            self.$modal.appendTo('body').modal();

            var event;
            $( '.state_text' ).click(function(ev) {
                event = $(ev.target).find('.odometer')[0];
            });
            $(".number_st").on('change',function(){
                var text_box_val = $(this).val();
                event.setAttribute("data-number", text_box_val);
            });
            $(".duration_st").on('change',function(){
                var text_box_val = $(this).val();
                event.setAttribute("data-duration", text_box_val);
            });
        },
    });
});
