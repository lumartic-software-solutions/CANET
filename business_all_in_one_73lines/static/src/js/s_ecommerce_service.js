odoo.define('s.ecommerce.service.73lines.editor', function(require) {
    'use strict';

    var ajax = require("web.ajax");
    var core = require("web.core");
    var Dialog = require("web.Dialog");
    var Model = require("web.Model");
    var editor = require("web_editor.editor");
    var animation = require('web_editor.snippets.animation');
    var options = require('web_editor.snippets.options');
    var snippet_editor = require('web_editor.snippet.editor');
    var website = require('website.website');
    var QWeb = core.qweb;

    var _t = core._t;

    options.registry.js_s_ecommerce_service = options.Class.extend({

        view_type : function(type, value) {
            if (type !== "click")
                return;
            var self = this;
            if (value == 'h') {
                self.$target.find(".ttcontent_inner").addClass('col-md-3');
                self.$target.find(".ttcontent_inner").removeClass('col-md-12');
                self.$target.find(".ttcontent_inner").css({
                    'border' : '1px solid #f0f0f0',
                    'padding' : '10px'
                });
                self.$target.find(".block_content > div").css({
                    'border-bottom' : '0px',
                    'float' : 'unset',
                    'padding' : '0'
                });
            }
            if (value == 'v') {
                self.$target.find(".ttcontent_inner").addClass('col-md-12');
                self.$target.find(".ttcontent_inner").removeClass('col-md-3');
                self.$target.find(".block_content > div").css({
                    'border-bottom' : '1px solid #f0f0f0',
                    'float' : 'left',
                    'padding' : '20px 0'
                });
                self.$target.find(".ttcontent_inner").css({
                    'border' : '0px',
                    'padding' : '0px'
                });
            }
        },

    });
});
