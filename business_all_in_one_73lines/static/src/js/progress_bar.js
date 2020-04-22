odoo.define('business_all_in_one_73lines.s_progress_bar', function (require) {
    'use strict';
    var ajax = require('web.ajax');
    var core = require('web.core');
    var s_options = require('web_editor.snippets.options');
    var s_animation = require('web_editor.snippets.animation');

    var QWeb = core.qweb;
    ajax.loadXML('/business_all_in_one_73lines/static/src/xml/progress_bar.xml', core.qweb);

    s_options.registry.js_progress_bar = s_options.Class.extend({
        start: function(){
            var self = this;
        },
        progress_opt: function (type, value, $li) {
            if (type !== 'click')  return;
            var self = this;
            self.$modal = $(QWeb.render("business_all_in_one_73lines.progress_bar"));
            self.$modal.appendTo('body').modal();

            var field_names = ['src'];
            var event;
            var event_pr;
            var change_color;
            $( '.progress_bars' ).click(function(ev) {
                event = $(ev.target).find('.progress_bar_1');
                event_pr = $(ev.target).find('.progress_content');
            });
            $('.color_active').change(function() {
                change_color=$(this).val();
                event_pr[0].setAttribute('data-active', change_color);
            });
            $('.color_nonactive').change(function() {
                change_color=$(this).val();
                event_pr[0].setAttribute('data-nonactive', change_color);
            });
            $(".progress1").on('change',function(){
                var text_box_val = $(this).val();
                if ($(text_box_val.length) != 0){
                    event_pr[0].setAttribute('data-percentage', text_box_val);
                    event.html(text_box_val);
                }
            });

        },
    });
});