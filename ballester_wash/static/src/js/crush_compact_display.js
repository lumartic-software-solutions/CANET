/** -*- coding: utf-8 -*-
 Odoo, Open Source Ballester Screen.
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('ballester_wash.crush_compact_display', function (require) {
"use strict";

var core = require('web.core');
var Widget = require('web.Widget');
var session = require('web.session');
var ajax = require('web.ajax');
var ActionManager = require('web.ActionManager');
var view_registry = require('web.view_registry');
var QWeb = core.qweb;

var _t = core._t;
var _lt = core._lt;


var CrushCompactDisplayScreen = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
//		'click .continue_button': 'continue_button',
		// ===========  main screen ===========
		'click .main': 'main',
		//'click .product_wash' :'product_wash',
		'change #type-select':'TypeOrderOnChangeEvent',
		'change #my-wash-product' : 'ProductOnChangeEvent',
		'click .my_profile': 'action_my_profile',
		
		// ===========  exit Popup ===========
		'click .confirm_exit_popup': 'confirm_exit_popup',
		// ===========  main 1 button ===========
		'click .entry_of_products': 'entry_of_products',
		// ===========  main 2 button ===========
               'click .output_of_products': 'output_of_products',
		// ===========  main 3 button ===========
		'click .warehouse': 'warehouse',
		// Add an item button
		'click .display_detail': 'display_detail',
		'click .display_crush_order':'display_crush_order',
		'click .display_compact_order' :'display_compact_order',
		// Validate Barcode  button
		'click .validate_barcode': 'validate_barcode',
		'change #barcode_number': 'barcode' ,
		'click .startcrush_button':'startcrush_button',
		'click .transfertocompact_store':'transfertocompact_store',
		'click .stopcompact_button':'stopcompact_button',	
		'click  .startcompact_button':'startcompact_button',
		'click .confirm_create_crush':'confirm_create_crush',
		// lot details wizard
		// ===========  main 4 button ===========
// Create   wash
		'click .crush_wash_order_button':'crush_wash_order_button',
		'click .create_crush_compact_button':'create_crush_compact_button',
		'click .create_crush_button' :'create_crush_button',
		'click .create_compact_button' :'create_compact_button',
		
		'click .compact_wash_order_button' : 'compact_wash_order_button',
		'click .alreday_crush_compact_button':'alreday_crush_compact_button',
		'click .save_crush_order': 'save_crush_order',
//onchange wash product
		//'click .onchange_product' :'onchange_product',
		'click .main_container_screen': 'main_container_screen',
		'click .stopcrush_button':'stopcrush_button',
		'click .transferto_store' :'transferto_store',
		'click .edit_crush_order':'edit_crush_order',
		'click .create_crush':'create_crush',
		'click .create_compact':'create_compact',
		'click .save_compact_order':'save_compact_order',
		'click .edit_compact_order' :'edit_compact_order',
		//'click .create_emptying_wash_order' : 'create_emptying_wash_order',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var operation_data = [];
        var self = this;
        if (context.tag == 'ballester_crush_compact_display_screen_act') {
            self._rpc({
                model: 'operation.wash.dashboard',
                method: 'get_operation_info',
            }, []).then(function(result){

            	self.operation_data = result[0]
                self.product_list = self.operation_data.product_list
                self.barcode_list = self.operation_data.barcode_list
                self.set_unused_barcode_list = self.operation_data.set_unused_barcode_list
                self.unused_barcode_list = self.operation_data.unused_barcode_list
                self.employee_id = session.employee_id
                self.employee = session.employee
		 self.recycled_product = self.operation_data.recycled_product
                self.employee_image_url = session.employee_image_url
            }).done(function(){
            	self.render();
                self.href = window.location.href;

            });
        }
    },
    willStart: function() {
        return $.when(ajax.loadLibs(this), this._super());
    },
    render: function () {
	   var super_render = this._super;
       var self = this;

       return  self.$el.html(QWeb.render("CrushCompactDisplay", {widget: self}));
    },
    reload: function () {
        window.location.href = this.href;
    },
    main: function (event) {
        var self = this;
	$('.modal-backdrop').remove();
        event.stopPropagation();
        event.preventDefault();
        return  self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
    },
    confirm_exit_popup: function (event) {
        var self = this;
        event.stopPropagation();
	$('.modal-backdrop').remove();
        event.preventDefault();
        return  self.do_action('ballester_wash.action_ballester_crush_compact_screen');
    },

    alreday_crush_compact_button: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.$el.html(QWeb.render("SelectCrushCompactTemplate", {widget: self}));
    },

     display_crush_order : function(event) {
      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		$('.modal-backdrop').remove();
		self.type = 'crush'
	 return  self.$el.html(QWeb.render("CrushCompactDisplay1", {widget: self}));	
		
	  },

      display_compact_order : function(event) {
      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		$('.modal-backdrop').remove();
		self.type = 'compact'
		 return  self.$el.html(QWeb.render("CrushCompactDisplaycompact", {widget: self}));
		
	  },

      create_crush_compact_button: function (event) {
        var self = this;
        event.stopPropagation();
	$('.modal-backdrop').remove();
        event.preventDefault();
        return  self.$el.html(QWeb.render("CrushCompactOptionTemplate", {widget: self}));
    },

	
      confirm_create_crush: function (event) {
        var self = this;
        event.stopPropagation();
	$('.modal-backdrop').remove();
        event.preventDefault();
        return  self.$el.html(QWeb.render("CrushCompactDisplay", {widget: self}));
    },

// create crush order

	create_crush : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		$('.modal-backdrop').remove();
		var barcode_list = [];
	   	var location = $("#my-select").val() ;
		var dest_location_id = $("#my-dest-select").val() ;
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
               var barcode_ids =  $("#barcode_wash").attr("ids");
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
	   	var report_data = [];

	   	if (location != undefined &&  product_id != undefined   &&  recycled_product_id != undefined   && dest_location_id != undefined ){	   	
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': 'crush',
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
 				});
			self._rpc({
			        model: 'operation.wash.dashboard',
			        method: 'create_crush_order_method',
			        args: [[],report_data ],
			    })
	            .then(function(result) {
	            	if (result.success) {
				self.type= 'crush'
	            		return self.$el.html(QWeb.render("ConfirmcrushWash", {widget: self}));
	            	}else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
  }
},

// create Compact order

	create_compact : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];
	   	var location = $("#my-select").val() ;
		var dest_location_id = $("#my-dest-select").val() ;
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
               var barcode_ids =  $("#barcode_wash").attr("ids");
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
	   	var report_data = [];
	   	if (location != undefined &&  product_id != undefined   &&  recycled_product_id != undefined   && dest_location_id != undefined ){	   	
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': 'compact',
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
 				});
			self._rpc({
			        model: 'operation.wash.dashboard',
			        method: 'create_compact_order_method',
			        args: [[],report_data ],
			    })
	            .then(function(result) {
	            	if (result.success) {
				self.type= 'compact'
	            		return self.$el.html(QWeb.render("ConfirmcrushWash", {widget: self}));
	            	}else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
  }
},



 save_crush_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
		$('.modal-backdrop').remove();
	   	event.preventDefault();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
	   	var report_data = [];
		var barcode_list = []
		var allow_save = true
	   	if (location == undefined ){
			self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
		}
		if (product_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Wash Product!!"));
		}
		if (recycled_product_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Recycled Product!"));
		}
		if (dest_location_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Destination Location"));
		}
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		self.type= 'crush'
		if (location != undefined &&  product_id != undefined   &&  recycled_product_id != undefined   && dest_location_id != undefined  ) {	   	
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': 'crush',
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list

 				});
			self._rpc({
			        model: 'operation.wash.dashboard',
			        method: 'save_crush_order_method',
			        args: [[],report_data ],
			    })
                    
	            .then(function(result) {

	            	if (result.success) {
	            		self.do_warn(_("Success"),_("Record Saved"));
	            		// hide validate barcode button
	            		$("#edit_crush_order_button").css("display", "inline");
	            		$("#create_destruction_order_button").css("display", "inline");
				$("#create_crush").css("display", "inline");
				$("#save_crush_order_button").css("display", "none");
				$("#type-select").attr("disabled", true);
				$("#my-dest-select").attr("disabled", true);
				$("#my-select").attr("disabled", true);
				$("#my-wash-product").attr("disabled", true);
				$("#my-recycled-product").attr("disabled", true);
				$("#barcode_wash").attr("disabled", true);
	            		// hide delete button
	            	}else{
	            		self.do_warn(_("Warning"),_("Can not save!!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Can not save!!"));
  }
},


save_compact_order : function(event){
	   	var self = this;
		$('.modal-backdrop').remove();
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
	   	var report_data = [];
		var barcode_list = []
		var allow_save = true
	   	if (location == undefined ){
			self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
		}
		if (product_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Wash Product!!"));
		}
		if (recycled_product_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Recycled Product!"));
		}
		if (dest_location_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Destination Location"));
		}
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		self.type= 'crush'
		if (location != undefined &&  product_id != undefined   &&  recycled_product_id != undefined   && dest_location_id != undefined  ) {	   	
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': 'compact',
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list

 				});
			self._rpc({
			        model: 'operation.wash.dashboard',
			        method: 'save_compact_order_method',
			        args: [[],report_data ],
			    })
                    
	            .then(function(result) {

	            	if (result.success) {
	            		self.do_warn(_("Success"),_("Record Saved"));
	            		// hide validate barcode button
	            		$("#edit_compact_order_button").css("display", "inline");
	            		$("#create_destruction_order_button").css("display", "inline");
				$("#create_compact").css("display", "inline");
				$("#save_compact_order_button").css("display", "none");
				$("#type-select").attr("disabled", true);
				$("#my-dest-select").attr("disabled", true);
				$("#my-select").attr("disabled", true);
				$("#my-wash-product").attr("disabled", true);
				$("#my-recycled-product").attr("disabled", true);
				$("#barcode_wash").attr("disabled", true);
	            		// hide delete button
	            	}else{
	            		self.do_warn(_("Warning"),_("Can not save!!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Can not save!!"));
  }
},
TypeOrderOnChangeEvent: function (event)
    {	
        var ordertype = document.getElementById('type-select').value;
            console.log("=====ordertype",ordertype)
	var ctx = {}
	$('.modal-backdrop').remove();
        var product_list = []
	var reproduct_list = []
	if (ordertype == ''){
			
		self.do_warn(_("Warning"),_("Please Enter the Order Type First!")); 
	
	}
	if (ordertype == 'Container'){
		ctx['type_of_order']='container'
	}
	if (ordertype == 'Drum'){
		ctx['type_of_order']='drum'
	}
        this._rpc({
            model: 'product.product',
            method: 'name_search',
	    args: ['', [],'ilike'],
	   context: ctx,
		
        })
        .then(function (result) {

		var size = 0, key;
		    for (key in result) {
			if (result.hasOwnProperty(key)) size++;
		    }
	       for(var i=0 ; i <= size; i++ ){
			var product_info = result[i]
			if (product_info){
					product_list.push({
					'id' : product_info[0],
					'name':product_info[1],
					})
			}
		} 

		/** var product_value =
			"<div class='col-md-3' style='width:350px'>" + 
			"<select class='product_wash'  id='my-wash-product' style='height: 65px;font-size: 22px;margin-top: 20px;'>" **/
		var product_value = ""
		for (var i=0 ; i <= size; i++){
			var product_data = product_list[i]
			
				if (product_data != undefined){
					var name=  product_data['name']
					name = name.replace("''","");
					product_value +=
					"<option  value='"+name + "'"+  "ids='" + product_data['id'] + "'>"  + name + "</option> "

					}
		
			}
		
		$("#my-wash-product").select2({});
		$("#my-wash-product").append( product_value );
		
        });
	
	this._rpc({
            model: 'product.product',
            method: 'name_search',
	    args: ['', [],'ilike'],
		
        })
        .then(function (result) {

		var size = 0, key;
		    for (key in result) {
			if (result.hasOwnProperty(key)) size++;
		    }
	       for(var i=0 ; i <= size; i++ ){
			var product_info = result[i]
			if (product_info){
					reproduct_list.push({
					'id' : product_info[0],
					'name':product_info[1],
					})
			}
		} 

		console.log("reproduct_list", reproduct_list)
		 var recycle_product_value =""
			
		
		for (var i=0 ; i <= size; i++){
			var reproduct_data = reproduct_list[i]
		
		         if (reproduct_data != undefined){
						var name=  reproduct_data['name']
						name = name.replace("''","");
					      recycle_product_value +=
						"<option value='"+name + "' label='"+name+ "' ids='" + reproduct_data['id'] + "'>"  + name + "</option> "
						
						}
		
			}
		
		$("#my-recycled-product").select2({});
		console.log("><<<<<<<<<<DSDssss",recycle_product_value)	
		$("#my-recycled-product").append( recycle_product_value );
		
        });
   },


       edit_crush_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		$('.modal-backdrop').remove();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids"); ;
	   	var report_data = [];
		var barcode_list = [];
		var allow_save = true
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		self._rpc({
		        model: 'operation.wash.dashboard',
		        method: 'edit_crush_order_method',
		        args: [[]],
		    })
                    
	            .then(function(result) {

	            	if (result.success) {
					self.type= 'crush'
	            		// hide validate barcode button
	            		$("#edit_crush_order_button").css("display", "none");
	            		$("#create_destruction_order_button").css("display", "none");
				$("#create_crush").css("display", "none");
				$("#save_crush_order_button").css("display", "inline");
				$("#type-select").attr("disabled", false);
				$("#my-dest-select").attr("disabled", false);
				$("#my-select").attr("disabled", false);
				$("#my-wash-product").attr("disabled", false);
				$("#my-recycled-product").attr("disabled", false);
				$("#barcode_wash").attr("disabled", false);
	            		// hide delete button
			}
	               });
},



       edit_compact_order : function(event){
	   	var self = this;
		$('.modal-backdrop').remove();
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids"); ;
	   	var report_data = [];
		var barcode_list = [];
		var allow_save = true
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		self._rpc({
		        model: 'operation.wash.dashboard',
		        method: 'edit_compact_order_method',
		        args: [[]],
		    })
                    
	            .then(function(result) {

	            	if (result.success) {
					self.type= 'crush'
	            		// hide validate barcode button
	            		$("#edit_compact_order_button").css("display", "none");
	            		$("#create_destruction_order_button").css("display", "none");
				$("#create_compact").css("display", "none");
				$("#save_compact_order_button").css("display", "inline");
				$("#type-select").attr("disabled", false);
				$("#my-dest-select").attr("disabled", false);
				$("#my-select").attr("disabled", false);
				$("#my-wash-product").attr("disabled", false);
				$("#my-recycled-product").attr("disabled", false);
				$("#barcode_wash").attr("disabled", false);
			}
	               });
},


create_crush_button: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        self._rpc({
            model: 'operation.wash.dashboard',
            method: 'get_crush_compact_info',
        }, []).then(function(result){
           self.barcode_list = result['data']['barcode_list']
           self.employee_id = session.employee_id
           self.location_list = result['data']['location_list']
           self.employee = session.employee 
	   self.washing_type = result['data']['washing_type']
           self.type_of_order = result['data']['type_of_order']
           self.employee_image_url = session.employee_image_url
        }).done(function(){
		self.type= 'crush'
        	self.href = window.location.href;
        return  self.$el.html(QWeb.render("CrushCreateTemplate", {widget: self}));
    });
        
    },

ProductOnChangeEvent: function (event)
    {	
        var selectedproductValue = document.getElementById('my-wash-product').value;
            console.log("=====selectedValue",selectedproductValue)
        var domain_dp = []
	    if (selectedproductValue != undefined){

		var first_step = selectedproductValue.split("[")
		var second_step = first_step[1].split("]")
		
		
            	domain_dp.push(['default_code', '=', second_step[0]])
		}
        this._rpc({
            model: 'operation.wash.dashboard',
            method: 'product_data',
            args: [domain_dp],
        })
        .then(function (result) {
		if(result.lot_list != [])
		{
		   var lot_list = result.lot_list
		   var optionsAsString = "";
	           for(var i = 0; i < Object.keys(lot_list).length  ; i++)
			{

			     var lot_detail = lot_list[i]
                            optionsAsString += "<option value='" + lot_detail['name'] + "'" + "ids='"+ lot_detail['id'] +"'>" + lot_detail['name'] + "</option>";
		            
			}
		$( '#barcode_wash' ).append( optionsAsString );
		}

		else {
		     $('#barcode_wash').val('');
		}

		  
        });

},


create_compact_button: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        self._rpc({
            model: 'operation.wash.dashboard',
            method: 'get_crush_compact_info',
        }, []).then(function(result){
           self.barcode_list = result['data']['barcode_list']
           self.employee_id = session.employee_id
           self.location_list = result['data']['location_list']
           self.employee = session.employee 
	   self.washing_type = result['data']['washing_type']
           self.type_of_order = result['data']['type_of_order']
           self.employee_image_url = session.employee_image_url
        }).done(function(){
		self.type= 'compact'
        	self.href = window.location.href;
        return  self.$el.html(QWeb.render("CompactCreateTemplate", {widget: self}));
    });
        
    },


    
    generate_barcode: function(event){
    	 var self = this;
         event.stopPropagation();
         event.preventDefault();
         self._rpc({
             model: 'operation.wash.dashboard',
             method: 'get_operation_info',
         }, []).then(function(result){
            self.operation_data = result[0]
            self.product_list = self.operation_data.product_list
//            self.ler_list = self.operation_data.ler_list
            self.barcode_list = self.operation_data.barcode_list
            self.set_unused_barcode_list = self.operation_data.set_unused_barcode_list
            self.unused_barcode_list = self.operation_data.unused_barcode_list
            self.employee_id = session.employee_id
            self.employee = session.employee
            self.employee_image_url = session.employee_image_url
         }).done(function(){
        	 self.href = window.location.href;
        	 return  self.$el.html(QWeb.render("GenerateBarcodeButton", {widget: self}));
         });
    },
//  selectign barcode from wash product
    display_detail: function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
		
	   	var number_of_barcode = $("#barcode_number").val();
		var type = self.type
 		if (type == 'crush')
			{
			console.log(">>>>>>>crush>>>>>>>>>>>>")
			ctx['crush_order']= "True";
			ctx['drum_crush'] = true ;
			}
		if (type == 'compact')
			{
			console.log(">>>>>>>>>>>>>>>>>>>")
			ctx['compact_order']= "True";
			ctx['drum_compact'] = true;
			}
		var emp = self.employee_id 
	   	if (number_of_barcode != ''){
				if (event.which === 13) {
			   	//	 generating barcode

				self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'search_barcode',
				context : ctx,
		                args: [[],number_of_barcode,emp],		            })
			
                              .then(function(result) {
					console.log("cccresultcccccccccc",result)
					$('#table_detail').remove()
						 $('#image_container').remove()
						if (result.wash_order_data)


						{
						    self.img_url = result['product_img_url']
						    self.barcode = result.wash_order_data[0]['barcode']
						    self.order_number = result.wash_order_data[0]['order_number']
						    self.order_type = result.wash_order_data[0]['type_of_order']
						    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
						    self.variants = result.wash_order_data[0]['variants']
						    self.state = result.wash_order_data[0]['state']
						    self.ler = result.wash_order_data[0]['ler']
						    self.un_code = result.wash_order_data[0]['un_code']
						    self.recycled_product_list = result.wash_order_data[0]['recycled_product']
						    self.delivery_location = result.wash_order_data[0]['delivery_location']
						    if (self.state == 'draft'){
								self.start_button = true
							  }
						    else if (self.state == 'start_crush'){
									self.stop_button = true 
									self.recycled_product = true
									self.dest_location=true 
								 } 
						    else if (self.state == 'stop_crush'){
									self.transfer_button = true 
									self.recycled_product = true
									self.dest_location=true
									self.qty_visible=true
								 }
							if (type == 'crush'){
						   return  self.$el.html(QWeb.render("CrushDisplayscreen", {widget: self}));}
							else if (type == 'compact'){
						 return  self.$el.html(QWeb.render("CompactDisplayscreen", {widget: self}));

				}

					
						}
					
					else if(result.warning)		{

					return  self.do_warn(_("Warning"),_("Product has already destructed and transfered!"));
}	
		else if(result.warning_crush)		{

					return  self.do_warn(_("Warning"),_("No Crush order for Metal Drum!"));
}	

		else if(result.warning_compact)		{

					return  self.do_warn(_("Warning"),_("NO Compact Order for Plastic Drum!"));
}	

						
							} );
						 
	}
		        
	            }
		else{
	    	   self.do_warn(_("Warning"),_("Please Enter the Number First!"));

	        }
	  },


     
barcode : function(event) {
      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
		$('.modal-backdrop').remove();
	   	var number_of_barcode = $("#barcode_number").val();
		var type = self.type
 		if (type == 'crush')
			{
			ctx['crush_order']= "True";
			ctx['drum_crush'] = true ;
			}
		if (type == 'compact')
			{
			ctx['compact_order']= "True";
			ctx['drum_compact'] = true;
			}
		var emp = self.employee_id 
	   	if (number_of_barcode != ''){
			   	//	 generating barcode

				self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'search_barcode',
				context : ctx,
		                args: [[],number_of_barcode,emp],		            })
			
                              .then(function(result) {
					$('#barcode_number').attr("disabled", true) 
					console.log("cccresultcccccccccc",result)

						if (result.wash_order_data)

					
						{
							if (result.product_img_url){
						    self.img_url = result['product_img_url']

							}
						    self.barcode = result.wash_order_data[0]['barcode']
						    self.order_number = result.wash_order_data[0]['order_number']
						    self.order_type = result.wash_order_data[0]['type_of_order']
						    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
						    self.variants = result.wash_order_data[0]['variants']
						    self.state = result.wash_order_data[0]['state']
						    self.ler = result.wash_order_data[0]['ler']
						    self.un_code = result.wash_order_data[0]['un_code']
						    self.recycled_product_list = result.wash_order_data[0]['recycled_product']
						    self.delivery_location = result.wash_order_data[0]['delivery_location']
						    if (self.state == 'draft'){
							console.log("<><<<<<<<<<<<<<<<<<<<<<<<<",self.state)
								self.start_button = true
							  }
						    else if (self.state == 'start_crush'){
									self.stop_button = true 
									self.recycled_product = true
									self.dest_location=true 
								 } 
						    else if (self.state == 'stop_crush'){
									//self.transfer_button = true 
									self.recycled_product = true
									self.dest_location=true
									self.qty_visible=true
											self.transfer_crush =true
								 }
							if (type == 'crush'){
						   return  self.$el.html(QWeb.render("CrushDisplayscreen", {widget: self}));}
							else if (type == 'compact'){
						 return  self.$el.html(QWeb.render("CompactDisplayscreen", {widget: self}));

							}

					
						}
					
					else if(result.warning)		{

					return  self.do_warn(_("Warning"),_("Product has already destructed and transfered!"));
}	
		else if(result.warning_crush)		{

					return  self.do_warn(_("Warning"),_("No Crush order for Metal Drum!"));
}	

		else if(result.warning_compact)		{

					return  self.do_warn(_("Warning"),_("NO Compact Order for Plastic Drum!"));
}	

						
							} );
						 
	
		        
	            }
		else{
	    	   self.do_warn(_("Warning"),_("Please Enter the Number First!"));

	        }
	  },



   /** barcode : function(event) {
console.log("=================>>>>>>>>>>>>>>>")
      	         var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
                ctx['display_barcode_details']= "True";
	   	var number_of_barcode = $("#barcode_number").val();
	   	if (number_of_barcode != ''){
			console.log("=================>>>>>>>>>>>>>>>")
				
				console.log("***************************")
			   	//	 generating barcode
		        self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'search_barcode',
				context : ctx,
		                args: [[],number_of_barcode],		            })
			
                              .then(function(result) {
				if (result.success) {
					
					if (result.wash_order_data){
				$("#image_container").css("display", "inline");
				document.getElementById('image_container')
					    .setAttribute(
						'src', 'data:image/png;base64,' + result.product_img_url
					    );
					$("#table_detail").css("display", "inline");
					$("#end_wash_order").css("display", "inline");
					$("#compact_wash_order_button").css("display", "inline");
					$("#crush_wash_order_button").css("display", "inline");
					$("#cancel_wash_order_button").css("display", "inline");

					$( "#table_detail").after(

						"<tr id='tr_detail'><td style='width: 250px;font-size:20px; color:blue'>No of Washing Order: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['order_number'] + "</td></tr><tr id='tr1_detail'> <td style='font-size:20px; color:blue'>  Type Of Order:</td><td style='font-size:20px; color:blue'>"+ result.wash_order_data[0]['type_of_order']+
					  "</td></tr> <tr id='tr2_detail'><td style='font-size:20px; color:blue'> Dangerous characteristics: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['dangerous_characteristics'] + "</td></tr> <tr id='tr3_detail'> <td style='font-size:20px; color:blue'>  Variants:</td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['variants'] +  "</td></tr>  <tr id='tr5_detail'> <td style='font-size:20px; color:blue'>   LER: </td><td style='font-size:20px; color:blue'>" +  result.wash_order_data[0]['ler'] +  "</td></tr> <tr id='tr6_detail'> <td style='font-size:20px; color:blue'>  UN code: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['un_code'] + "</td></tr> <tr id='tr7_detail'> <td style='font-size:20px; color:blue'>  Recycled Product: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['recycled_product'] +"</td></tr>" );
                                      
					}

					}
				if (result.warning) {
                                        self.do_warn(_("Warning"),_("'There is no wash order for this barcode! \n Please Enter Valid Number !'"));

					}
					
			} );
	   		 }
		else{
	    	   self.do_warn(_("Warning"),_("Please Enter the Number First!"));
	       }
	  },
**/




crush_wash_order_button: function(event){
	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
                ctx['crush_order']= "True";
		ctx['drum_crush'] = true ;
		var emp = self.employee_id 
                $('.modal-backdrop').remove();
	   	var number_of_barcode = $("#barcode_number").val();
	   	if (number_of_barcode != ''){
			self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'search_barcode',
				context : ctx,
		                args: [[],number_of_barcode,emp],		            })
			
                              .then(function(result) {
					console.log("cccccccccccccccccccccccccc",result)
						if (result.wash_order_data)


						{
						    self.img_url = result['product_img_url']
						    self.barcode = result.wash_order_data[0]['barcode']
						    self.order_number = result.wash_order_data[0]['order_number']
						    self.order_type = result.wash_order_data[0]['type_of_order']
						    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
						    self.variants = result.wash_order_data[0]['variants']
						    self.state = result.wash_order_data[0]['state']
						    self.ler = result.wash_order_data[0]['ler']
						    self.un_code = result.wash_order_data[0]['un_code']
						    self.recycled_product_list = result.wash_order_data[0]['recycled_product']
						    self.delivery_location = result.wash_order_data[0]['delivery_location']
						    if (self.state == 'draft'){
								self.start_button = true
							  }
						    else if (self.state == 'start_crush'){
									self.stop_button = true 
									self.recycled_product = true
									self.dest_location=true 
								 } 
						    else if (self.state == 'stop_crush'){
									self.transfer_button = true 
									self.recycled_product = true
									self.dest_location=true
									self.qty_visible=true
								 }
						   return  self.$el.html(QWeb.render("CrushDisplayscreen", {widget: self}));
						}
					
					else if(result.warning)		{

					return  self.do_warn(_("Warning"),_("Product has already destructed and transfered!"));
}	
		else if(result.warning_crush)		{

					return  self.do_warn(_("Warning"),_("No Crush order for Metal Drum!"));
}	

		else if(result.warning_compact)		{

					return  self.do_warn(_("Warning"),_("NO Compact Order for Plastic Drum!"));
}	

						
							} );
						 
		        
	            }
		else{
	    	   self.do_warn(_("Warning"),_("Please Enter the Number First!"));

	        }
	  },

startcrush_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
	var recycled_product = $("#recycled_product_crush").val(); 
	var dest_location = $("#delivery_location").val();  
        $('.modal-backdrop').remove();
	var ctx = {};
	ctx['start_crush_order']= "True";
	var emp = self.employee_id 
	ctx['recycled_product']= recycled_product;
	ctx['dest_location']=dest_location ;
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
			if (result.warning1)
			{   

			self.do_warn(_("Warning"),_("Recycled Product is Missing!"));
			}
			if (result.warning2)
			{
                        self.do_warn(_("Warning"),_("Destination Product in missing!"));
			}	
			if  (result.wash_order_data)
			{
				self.barcode = result.wash_order_data[0]['barcode']
			    self.order_number = result.wash_order_data[0]['order_number']
			    self.order_type = result.wash_order_data[0]['type_of_order']
			    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
			    self.variants = result.wash_order_data[0]['variants']
			    self.ler = result.wash_order_data[0]['ler']
				self.img_url = result.wash_order_data[0]['img_url']
			    self.un_code = result.wash_order_data[0]['un_code']
			    self.recycled_product_list = result.wash_order_data[0]['recycled_product']
			    self.state = result.wash_order_data[0]['state']
			    self.kilo_qty = result.wash_order_data[0]['kilo_qty']
			    self.delivery_location = dest_location
				self.continue_button = true
				self.dest_location = true
				self.recycled_product = true
				self.stop_crush_wash = true
				self.start_button = false
				console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
				$('.modal-backdrop').remove();
				return  self.$el.html(QWeb.render("CrushDisplayscreen", {widget: self}));
				}
			else{
			return self.do_warn(_("Warning"),_("THere is no crush order for this!"));

			}
	
                 
                });

},

stopcrush_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
	var ctx = {};
	$('.modal-backdrop').remove();
	ctx['stop_crush_order']= "True";
	var emp = self.employee_id 
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
			if  (result.success)
			{
				
				self.barcode = result.wash_order_data[0]['barcode']
			    self.order_number = result.wash_order_data[0]['order_number']
			    self.order_type = result.wash_order_data[0]['type_of_order']
			    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
			    self.variants = result.wash_order_data[0]['variants']
			self.img_url = result.wash_order_data[0]['img_url']
			    self.ler = result.wash_order_data[0]['ler']
			    self.un_code = result.wash_order_data[0]['un_code']
			    
			    self.recycled_product_list = result.wash_order_data[0]['recycled_product']
			    self.state = result.wash_order_data[0]['state']
			   // self.delivery_location = result.wash_order_data[0]['dest_location_id']
				self.continue_button = true
				self.transfer_crush = true
				self.stop_crush_wash = false
				self.qty_visible = true
				$('.modal-backdrop').remove();
				return  self.$el.html(QWeb.render("CrushDisplayscreen", {widget: self}));
				}

				else{
			return self.do_warn(_("Warning"),_("THere is no crush order for this!"));

			}
	
                });

},



transferto_store: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
	var material_qty = $("#qty").val();
        $('.modal-backdrop').remove();
	var ctx = {};
	var emp = self.employee_id 
	ctx['transferto_crush_order'] = "True";
	ctx['material_qty'] = material_qty ;
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
			if  (result.warning)
			{
				self.do_warn(_("Warning"),_("First Please Enter material Quantity In Recycled Product Setting!"));
				}

			if  (result.success)
			{
				$('.modal-backdrop').remove();
				self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
			    }, 2000);
				}
	
                 console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
                });

},




compact_wash_order_button: function(event){
	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
		ctx['drum_compact'] = true;
		var emp = self.employee_id 
                ctx['compact_order']= "True";
                $('.modal-backdrop').remove();
	   	var number_of_barcode = $("#barcode_number").val();
	   	if (number_of_barcode != ''){
			self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'search_barcode',
				context : ctx,
		                args: [[],number_of_barcode,emp],		            })
			
                              .then(function(result) {
						if (result.wash_order_data)

						{
						    self.img_url = result['product_img_url']
						    self.barcode = result.wash_order_data[0]['barcode']
						    self.order_number = result.wash_order_data[0]['order_number']
						    self.order_type = result.wash_order_data[0]['type_of_order']
						    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
						    self.variants = result.wash_order_data[0]['variants']
						    self.state = result.wash_order_data[0]['state']
						    self.ler = result.wash_order_data[0]['ler']
						    self.un_code = result.wash_order_data[0]['un_code']
						    self.recycled_product_list = result.wash_order_data[0]['recycled_product']
						    self.delivery_location = result.wash_order_data[0]['delivery_location']
						    if (self.state == 'draft'){
								self.start_button = true
							  }
						    else if (self.state == 'start_crush'){
									self.stop_button = true 
									self.recycled_product = true
									self.dest_location=true 
								 } 
						    else if (self.state == 'stop_crush'){
									self.transfer_button = true 
									self.recycled_product = true
									self.dest_location=true
									self.qty_visible=true
								 }
						$('.modal-backdrop').remove();
						   return  self.$el.html(QWeb.render("CompactDisplayscreen", {widget: self}));
						}
					
					else if(result.warning)		{

					return  self.do_warn(_("Warning"),_("Product has already destructed and transfered!"));
}	

						
							} );
						 
		        
	            }
		else{
	    	   self.do_warn(_("Warning"),_("Please Enter the Number First!"));

	        }
	  },

startcompact_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
	var recycled_product = $("#recycled_product_crush").val(); 
	var dest_location = $("#delivery_location").val();  
	var ctx = {};
	ctx['start_compact_order']= "True";
	ctx['recycled_product']= recycled_product;
	var emp = self.employee_id 
	$('.modal-backdrop').remove();
	ctx['dest_location']=dest_location ;
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
			if (result.warning1)
			{   

			self.do_warn(_("Warning"),_("Recycled Product is Missing!"));
			}
			if (result.warning2)
			{
                        self.do_warn(_("Warning"),_("Destination Product in missing!"));
			}	
			if  (result.wash_order_data)
			{
				self.barcode = result.wash_order_data[0]['barcode']
			    self.order_number = result.wash_order_data[0]['order_number']
			    self.order_type = result.wash_order_data[0]['type_of_order']
			    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
			    self.variants = result.wash_order_data[0]['variants']
			    self.ler = result.wash_order_data[0]['ler']
			self.img_url = result.wash_order_data[0]['img_url']
			    self.un_code = result.wash_order_data[0]['un_code']
			     self.recycled_product_list = result.wash_order_data[0]['recycled_product']
			    self.state = result.wash_order_data[0]['state']
			self.kilo_qty = result.wash_order_data[0]['kilo_qty']
			    self.delivery_location = dest_location
				self.continue_button = true
				self.start_button = false
				self.stop_crush_wash = true
				self.dest_location = true
				self.recycled_product = true
				$('.modal-backdrop').remove();
				return  self.$el.html(QWeb.render("CompactDisplayscreen", {widget: self}));
				}
			else{
			return self.do_warn(_("Warning"),_("THere is no crush order for this!"));

			}
	
	
                 console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
                });

},

stopcompact_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
        console.log("cccccccUUUU----er_of_barcodeUUUUUUUU",self.barcode)
	var ctx = {};
	$('.modal-backdrop').remove();
	var emp = self.employee_id 
	ctx['stop_compact_order']= "True";
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
			if  (result.wash_order_data)
			{

		            self.barcode = result.wash_order_data[0]['barcode']
			    self.order_number = result.wash_order_data[0]['order_number']
			    self.order_type = result.wash_order_data[0]['type_of_order']
			    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
			    self.variants = result.wash_order_data[0]['variants']
			    self.ler = result.wash_order_data[0]['ler']
			    self.img_url = result.wash_order_data[0]['img_url']
			    self.un_code = result.wash_order_data[0]['un_code']
			    self.recycled_product_list = result.wash_order_data[0]['recycled_product']
			    self.state = result.wash_order_data[0]['state']
			   // self.delivery_location = result.wash_order_data[0]['dest_location_id']
			self.continue_button = true
			self.transfer_crush = true
			self.stop_crush_wash = false

				self.qty_visible = true
				$('.modal-backdrop').remove();
				return  self.$el.html(QWeb.render("CompactDisplayscreen", {widget: self}));
				}
			else {
				return self.do_warn(_("Warning"),_("THere is no crush order for this!"));
				}
	
                });

},



transfertocompact_store: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
	var material_qty = $("#qty").val();
        $('.modal-backdrop').remove();
	var ctx = {};
	var emp = self.employee_id 
	ctx['transferto_compact_order'] = "True";
	ctx['material_qty'] = material_qty ;
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
			console.log("ddddddresultdddd",result)
			if  (result.warning)
			{
				self.do_warn(_("Warning"),_("First Please Enter material Quantity!"));
				}

			if  (result.success)
			{
			$('.modal-backdrop').remove();
				  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
			    }, 2000);
				}
	
                });

},


// Confirm main screen

	main_container_screen : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();

	    session.employee_id = this.employee_id;
		 session.employee = this.employee; 
		session.employee_image_url = this.employee_image_url ;
		var type = self.type
		$('.modal-backdrop').remove();
                return  self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
},



// cancel wash order

       cancel_wash_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
    		// cancel all data
    		$("#image_container").css("display", "none");
		$("#table_detail").css("display", "none");
		$("#crush_wash_order_button").css("display", "none");
		$("#compact_wash_order_button").css("display", "none");
		$("#recycled_product_crush").css("display", "none");
		$("#tr_detail").css("display", "none");
		$("#tr1_detail").css("display", "none");
		$("#tr4_detail").css("display", "none");
		$("#tr2_detail").css("display", "none");
		$("#tr3_detail").css("display", "none");
		$("#tr5_detail").css("display", "none");
		$("#tr6_detail").css("display", "none");
		$("#tr7_detail").css("display", "none");
		$("#tr8_detail").css("display", "none");
	},


// onchnage wash product

       onchange_product : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
                var product_id = $(".es-list li[value='" + $(".product_wash").val() + "']").attr('ids');
		var type_of_order = $(".select").val() ;
	   	var report_data = [];
		$('.modal-backdrop').remove();
		var barcode_list = [];
		console.log("-----report_dproduct_idata-----------",product_id)
		var ctx = {};
		if ( product_id != undefined  ) {
			ctx['product_id']= product_id,
			ctx['type_of_order']=type_of_order
                        console.log("-----report_data-----------", ctx)
			self._rpc({
			         model: 'operation.wash.dashboard',
                                method: 'get_operation_info',
				 context : ctx,
				args :[]
                        })

	            .then(function(result) {
	               });
           }else{
              self.do_warn(_("Warning"),_("Please add wash product!!"));
  }
},



      validate_barcode: function(event){
			   	var self = this;
			   	event.stopPropagation();
			   	event.preventDefault();
			   	var location = $("#set_loction_id").attr('ids');
			   	var inventory_data = [];
				$('.modal-backdrop').remove();
			   	if (location != undefined){
				   	//	 append inventory id to validate barcode
				   	inventory_data.push(document.getElementById("created_inventory_id").value);
				   	//	 validating inventory adjustments
			        self._rpc({
			                model: 'operation.wash.dashboard',
			                method: 'validate_inventory_adjustments',
			                args: [[],inventory_data],
			            })
			            .then(function(result) {
			            	if (result.success) {
			            		self.do_warn(_("Success"),_("Successfully Validate the Barcode!"));
			            		// hide validate barcode button
			            		$("#edit_inventory_adjustments_button").css("display", "none");
			            		$("#validate_barcode_button").css("display", "none");
			            		// hide delete button
			            		$('#inventory_adjustments_table .btndelete').remove();
			            	}else{
			            		self.do_warn(_("Warning"),_("No Data Found!"));
			            	}
			            });
			    }else{
			    	   self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
			       }
	    },
 	 btndelete: function(event){
		       var self = this;
		       event.stopPropagation();
		       event.preventDefault();
		       var inventory_data = [] ;
	    	   var inventory_ids = event.target.getAttribute("inventory");
	    	   if (inventory_ids != undefined ){
	    		   inventory_data.push(inventory_ids);
		    	   self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'delete_inventory_adjustments',
		                args: [[],inventory_data],
		            })
		            .then(function(result) {
		            	if (result.success) {
		            		 event.target.closest('tr').remove();
		            		self.do_warn(_("Success"),result.success);
		            	}else if (result.warning) {
		            		self.do_warn(_("Warning"),result.warning);
		            	}else{
		            		alert("Error")
		            	}
		            });
	    	   }else if(inventory_ids == null ){
	    		   event.target.closest('tr').remove();
	    	   }else{
	    		   alert("error")
	    	   }

	 },
	 lot_details_wizard :function(event){
	       var self = this;
	       event.stopPropagation();
	       event.preventDefault();
		$('.modal-backdrop').remove();
	       var  product = $(event.target).closest('tr').find('.products')
	       var product_id = $(".es-list li[value='" + product.val() + "']").attr('ids');
	       $(event.target).attr("product_id", product_id);
	       var  barcode = $(event.target).closest('tr').find('.barcodes');
	       var barcode_id = $(".es-list li[value='" + barcode.val() + "']").attr('ids');
	       $(event.target).attr("barcode_id", barcode_id);
	       if (product.val() == '') {
	    	   self.do_warn(_("Warning"),_("Product is Required!"));
	       }
	       else if (barcode.val() == '') {
	    	   self.do_warn(_("Warning"),_("Barcode is Required!"));
			}
	       else {
	    	   var line_id = event.target.getAttribute("line_id");
	    	   var lot_id = event.target.getAttribute("lot_id");
	    	   var product_id = event.target.getAttribute("product_id");
	    	   var barcode_id = event.target.getAttribute("barcode_id");
	    	   self.do_action({
	            name: _t("Lots/Serial Number Details"),
	            type: 'ir.actions.act_window',
	            res_model: 'lot.details.wizard',
	            view_mode: 'form',
	            view_type: 'form',
	            views: [[false, 'form']],
	            context: {
	                    'lot_id': lot_id,
	                    'line_id':line_id,
	                    'product_ids': product_id,
	                    'barcode_ids' : barcode_id
	                    },
	            target: 'new'
	          })
	       }
     },
	   action_my_profile: function(event) {
	       var self = this;
	       event.stopPropagation();
	       event.preventDefault();
	       this.do_action({
	           name: _t("My Profile"),
	           type: 'ir.actions.act_window',
	           res_model: 'hr.employee',
	           res_id: self.employee_id,
	           view_mode: 'form',
	           view_type: 'form',
	           views: [[false, 'form']],
	           context: {},
	           domain: [],
	           target: 'inline'
	       },{on_reverse_breadcrumb: function(){ return self.reload();}})
	   },
});
core.action_registry.add('ballester_crush_compact_display_screen_act', CrushCompactDisplayScreen);

return CrushCompactDisplayScreen;

});
