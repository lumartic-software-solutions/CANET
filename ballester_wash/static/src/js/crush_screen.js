/** -*- coding: utf-8 -*-
 Odoo, Open Source Ballester Screen.
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('ballester_wash.crush_screen', function (require) {
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


var CrushCompactScreen = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
//		'click .continue_button': 'continue_button',
		// ===========  main screen ===========
		'click .main': 'main',
		//'click .product_wash' :'product_wash',
		'click .my_profile': 'action_my_profile',
		'change #my-wash-product' : 'ProductOnChangeEvent',
'click .save_compact_order':'save_compact_order',
		// ===========  exit Popup ===========
		'click .confirm_exit_popup': 'confirm_exit_popup',
		// ===========  main 1 button ===========
		'click .entry_of_products': 'entry_of_products',
		// ===========  main 2 button ===========
               'click .output_of_products': 'output_of_products',
		// ===========  main 3 button ===========
		// Add an item button
		'click .display_detail': 'display_detail',
		'click .display_crush_order':'display_crush_order',
		'click .display_compact_order' :'display_compact_order',
		'click .create_compact':'create_compact',
		'change #type-select':'TypeOrderOnChangeEvent',
		// Validate Barcode  button
		'click .validate_barcode': 'validate_barcode',
		'change #barcode_number': 'barcode' ,
		'click .startcrush_button':'startcrush_button',
		'click .transfertocompact_store':'transfertocompact_store',
		'click .stopcompact_button':'stopcompact_button',	
		'click  .startcompact_button':'startcompact_button',
		'click .confirm_create_crush':'confirm_create_crush',
		'click .edit_compact_order' :'edit_compact_order',
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
		// lot details wizard
		// ===========  main 4 button ===========
// Create   wash
		//'click .create_emptying_wash_order' : 'create_emptying_wash_order',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var operation_data = [];
        var self = this;
        if (context.tag == 'ballester_crush_contine_screen_act') {
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
      console.log(">>dxddddd>>>>>>>>>>>>>>>>>>>>>>>>>>>")

       return  self.$el.html(QWeb.render("CrushCompactDisplay1", {widget: self}));
    },
    reload: function () {
        window.location.href = this.href;
    },
    main: function (event) {
        var self = this;
      console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
	$('.modal-backdrop').remove();
        event.stopPropagation();
        event.preventDefault();
        return  self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
    },
    confirm_exit_popup: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
      return self.$el.html(QWeb.render("CrushCompactDisplay", {widget: self}));
    },

save_compact_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
	   	var report_data = [];
		var barcode_list = [];
		$('.modal-backdrop').remove();
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
                        console.log("-----report_data-----------",report_data)
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


       edit_compact_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = $("#my-select").val() ;
		var dest_location_id = $("my-dest-select").val() ;
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                
                var barcode_ids =  $("#barcode_wash").attr("ids"); ;
	   	var report_data = [];
		var barcode_list = [];
		$('.modal-backdrop').remove();
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
	            		// hide delete button
			}
	               });
},
// create Compact order

	create_compact : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];
		$('.modal-backdrop').remove();
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
			console.log(">>>>aseff>>>>>",location,product_id )
		        console.log(">>>>>report_data>>>>>",report_data)
			self._rpc({
			        model: 'operation.wash.dashboard',
			        method: 'create_crush_order_method',
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


transferto_store: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
	var material_qty = $("#qty").val();
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
				self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
			setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
			    }, 2000);
				}
	
                });

},
TypeOrderOnChangeEvent: function (event)
    {	
        var ordertype = document.getElementById('type-select').value;
            $('.modal-backdrop').remove();
	var ctx = {}
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
		
		$("#my-wash-product").select2();
		console.log("><<<<<<<<<<DSDssss",product_value)	
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
create_crush_button: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        self._rpc({
            model: 'operation.wash.dashboard',
            method: 'get_crush_compact_info',
        }, []).then(function(result){
	console.log("ffffffffffffffffffff", result)
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
		$('.modal-backdrop').remove();
		if(result.lot_list != [])
		{
                  console.log("OOOOOOOresult.lot_list OOOOO",result.lot_list )
		   var lot_list = result.lot_list
                   console.log("OOOOOOOrelot_listOOOOO",Object.keys(lot_list).length)
		   var optionsAsString = "";
	           for(var i = 0; i < Object.keys(lot_list).length  ; i++)
			{
                            console.log(">>>>>lot_list>>>>>>>>>>>", lot_list[i])

			     var lot_detail = lot_list[i]
                            console.log(">>>>>lot_list>>>>>>>>>>>", lot_detail['name'] )
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
		self.type= 'compact'
        	self.href = window.location.href;
        return  self.$el.html(QWeb.render("CompactCreateTemplate", {widget: self}));
    });
        
    },


alreday_crush_compact_button: function (event) {
        var self = this;
        event.stopPropagation();
	$('.modal-backdrop').remove();
        event.preventDefault();
        return  self.$el.html(QWeb.render("SelectCrushCompactTemplate", {widget: self}));
    },

     display_crush_order : function(event) {
      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		self.type = 'crush'
	$('.modal-backdrop').remove();
	 return  self.$el.html(QWeb.render("CrushCompactDisplay1", {widget: self}));	
		
	  },

      display_compact_order : function(event) {
      	var self = this;
	   	event.stopPropagation();
		$('.modal-backdrop').remove();
	   	event.preventDefault();
		self.type = 'compact'
		 return  self.$el.html(QWeb.render("CrushCompactDisplay2", {widget: self}));
		
	  },

      create_crush_compact_button: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.$el.html(QWeb.render("CrushCompactOptionTemplate", {widget: self}));
    },

	
      confirm_create_crush: function (event) {
        var self = this;
	$('.modal-backdrop').remove();
        event.stopPropagation();
        event.preventDefault();
        return  self.$el.html(QWeb.render("CrushCompactDisplay", {widget: self}));
    },

// create CRUSH order

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
			console.log(">>>>aseff>>>>>",location,product_id )
		        console.log(">>>>>report_data>>>>>",report_data)
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



 save_crush_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
              var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
	   	var report_data = [];
		var barcode_list = []
		$('.modal-backdrop').remove();
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
                        console.log("-----report_data-----------",report_data)
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



       edit_crush_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids"); ;
	   	var report_data = [];
		$('.modal-backdrop').remove();
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

startcrush_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
        console.log("cccccccUUUUUUUUUUUUUUUUUUnumber_of_barcodeUUUUUUUU",self.barcode)
	var recycled_product = $("#recycled_product_crush").val(); 
	var dest_location = $("#delivery_location").val();  
	var ctx = {};
	ctx['start_crush_order']= "True";
	
	ctx['recycled_product']= recycled_product;
	ctx['dest_location']=dest_location ;
	var emp = self.employee_id 
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
			if  (result.success)
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
				return  self.$el.html(QWeb.render("CrushDisplayscreen", {widget: self}));
				}
	
                 console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
                });

},
stopcrush_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
       $('.modal-backdrop').remove();
	var ctx = {};
	var emp = self.employee_id 
	ctx['stop_crush_order']= "True";
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
			    self.ler = result.wash_order_data[0]['ler']
			self.img_url = result.wash_order_data[0]['img_url']
			    self.un_code = result.wash_order_data[0]['un_code']
			     self.recycled_product_list = result.wash_order_data[0]['recycled_product']
			    self.state = result.wash_order_data[0]['state']
			   // self.delivery_location = result.wash_order_data[0]['dest_location_id']
				self.continue_button = true
				self.transfer_crush = true
				self.qty_visible = true
				self.stop_crush_wash = false
				return  self.$el.html(QWeb.render("CrushDisplayscreen", {widget: self}));
				}
	
                 console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
                });

},


//  selectign barcode from wash product
    display_detail: function(event){
	console.log("dfddddddddddddddddddddd")
      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		$('.modal-backdrop').remove();
		var ctx = {};
		console.log(">>>>>>>>>>>>>>>ASseldlseld" ,self) 
		ctx['crush_order']= "True";
	        ctx['drum_crush'] = true ;
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
					$('#table_detail').remove()
						 $('#image_container').remove()
					console.log("ccccccccccccccccccccctxcccccc",ctx)
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
		ctx['crush_order']= "True";
	        ctx['drum_crush'] = true ;
	   	var number_of_barcode = $("#barcode_number").val();
		var type = self.type
		$('.modal-backdrop').remove();
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
						if (result.wash_order_data)
						{

							if (result.product_img_url) {
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
									self.transfer_crush =true
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
	
// Confirm main screen

	main_container_screen : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		$('.modal-backdrop').remove();

	    session.employee_id = this.employee_id;
		 session.employee = this.employee; 
		session.employee_image_url = this.employee_image_url ;
		var type = self.type
               return  self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
},

compact_wash_order_button: function(event){
	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
		$('.modal-backdrop').remove();
		ctx['drum_compact'] = true;
                ctx['compact_order']= "True";
		var emp = self.employee_id 
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
	$('.modal-backdrop').remove();
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
        console.log("cccc-----------------------------UU",self.barcode)
	var recycled_product = $("#recycled_product_crush").val(); 
	var dest_location = $("#delivery_location").val();  
	var ctx = {};
	ctx['start_compact_order']= "True";
	ctx['recycled_product']= recycled_product;
	ctx['dest_location']=dest_location ;
	var emp = self.employee_id 
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
			if  (result.success)
			{
				self.barcode = result.wash_order_data[0]['barcode']
			  self.kilo_qty = result.wash_order_data[0]['kilo_qty']
			    self.order_number = result.wash_order_data[0]['order_number']
			    self.order_type = result.wash_order_data[0]['type_of_order']
			    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
			    self.variants = result.wash_order_data[0]['variants']
			    self.ler = result.wash_order_data[0]['ler']
			self.img_url = result.wash_order_data[0]['img_url']
			    self.un_code = result.wash_order_data[0]['un_code']
			     self.recycled_product_list = result.wash_order_data[0]['recycled_product']
			    self.state = result.wash_order_data[0]['state']
			    self.delivery_location =dest_location
				self.continue_button = true
				self.start_button = false
				self.stop_crush_wash = true
				self.dest_location = true
				self.recycled_product = true
				return  self.$el.html(QWeb.render("CompactDisplayscreen", {widget: self}));
				}
	
                 console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
                });

},


stopcompact_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
        console.log("cccccccUUUU----er_of_barcodeUUUUUUUU",self.barcode)
	var ctx = {};
	ctx['stop_compact_order']= "True";
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
				self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
			    }, 2000);
				}
	
                 console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
                });

},



transfertocompact_store: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
	//var number_of_barcode = $("#barcode_number").val();
        var number_of_barcode = self.barcode
	var material_qty = $("#qty").val();
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
				self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_crush_compact_display_screen');
			    }, 2000);
				}
	
                 console.log(">>>>>>>>>>>>>>result>>>>>>>>>>>>>>>>>>",result)
                });

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
core.action_registry.add('ballester_crush_contine_screen_act', CrushCompactScreen);

return CrushCompactScreen;

});
