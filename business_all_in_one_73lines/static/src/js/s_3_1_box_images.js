odoo.define('s.three.promo.banner.images.odoo.73lines.editor', function(require) {
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

	options.registry.s_3_1_box_images = options.Class.extend({

		clean_for_save : function() {
			this._super();
			this.$target.find("#ttbanner-img span").addClass("hover");
		},
		start : function() {
			this._super.apply(this, arguments);
			this.$target.find("#ttbanner-img  span").removeClass("hover");
		},
	});
});
