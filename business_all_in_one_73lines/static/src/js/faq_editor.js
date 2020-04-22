odoo.define('business_all_in_one_73lines.s_faq', function (require) {
    'use strict';

    var core = require('web.core');
    var s_animation = require('web_editor.snippets.animation');
    var options = require('web_editor.snippets.options');
    var QWeb = core.qweb;
    options.registry['faq-section'] = options.Class.extend({
    drop_and_build_snippet: function () {
        this.id = "myAccordion" + new Date().getTime();
        this.ids = "toggle" + new Date().getTime();
        this.$target.find(".accordion-toggle").attr("data-parent", "#" + this.id);
        this.$target.find("#myAccordion").attr("id", "#" + this.id);
        this.$target.find(".accordion-toggle").attr("href", "#" + this.ids);
        this.$target.find(".accordion-body").attr("id",this.ids);
    },
    on_clone: function ($clone) {
        $clone.ids = "toggle" + new Date().getTime();
        console.log("ffffffffffffffff",this.$target.find(".accordion-toggle"));
        $clone.find(".accordion-toggle").attr("href", "#" + $clone.ids);
        $clone.find(".accordion-body").attr("id",$clone.ids);
    },
    });
});
