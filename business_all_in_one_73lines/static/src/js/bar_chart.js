odoo.define('business_all_in_one_73lines.s_bar_chart', function(require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');
    var s_animation = require('web_editor.snippets.animation');

    var QWeb = core.qweb;
    ajax.loadXML('/business_all_in_one_73lines/static/src/xml/bar_chart.xml',
            core.qweb);

    s_options.registry.js_bar_chart = s_options.Class.extend({
        start : function() {
            var self = this;
        },
        bar_opt : function(type, value, $li) {
            if (type !== 'click')
                return;
            var self = this;
            self.$modal = $(QWeb.render("business_all_in_one_73lines.bar_chart"));
            self.$modal.appendTo('body').modal();
            var field_names = [ 'src' ];
            var event;
            var event_pr;
            var change_color;
            $('.bar_chart').click(function(ev) {
                event = $(ev.target).find('.progress');
                event_pr = $(ev.target).find('.progress_content');
                console.info(event);
            });
            $('.color_active').change(
                function() {
                    change_color = $(this).val();
                    event_pr[0].setAttribute('data-active', change_color);
                    var style = event_pr[0].getAttribute('style');
                    if (style)
                        event_pr[0].setAttribute('style', style
                                        + ' background-color:'
                                        + change_color + ';');
                    else
                        event_pr[0].setAttribute('style',
                                ' background-color:' + change_color + ';');
                });
            $('.color_nonactive').change(
                function() {
                    change_color = $(this).val();
                    var style = event[0].getAttribute('style');
                    if (style)
                        event[0].setAttribute('style', style
                                        + ' background-color:'
                                        + change_color + ';');
                    else
                        event[0].setAttribute('style', ' background-color:'
                                + change_color + ';');
                });
            $(".progress1").on('change', function() {
                var text_box_val = $(this).val();
                if ($(text_box_val.length) != 0) {
                    event_pr[0].setAttribute('aria-valuenow', text_box_val);
                }
            });

        },
    });
});
$(document).ready(function() {
    $(".bar_chart").appear(function() {
        var bar_chart = $(this).find('.progress-bar-striped');
        bar_chart.css({
            'height' : bar_chart.attr('aria-valuenow') + '%',
            'background-color' : bar_chart.attr('data-active')
        });
        $(this).find("#myBar").html(bar_chart.attr('aria-valuenow') + '%')
    });
});
