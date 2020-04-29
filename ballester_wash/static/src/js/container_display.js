/** -*- coding: utf-8 -*-
 Odoo, Open Source Ballester Screen.
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('ballester_wash.container_display', function (require) {
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


var ContainerDisplayScreen = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
//		'click .continue_button': 'continue_button',
		// ===========  main screen ===========
		'click .main': 'main',
		//'click .product_wash' :'product_wash',
		'click .my_profile': 'action_my_profile',
		'click .endemptyingwash_button':'endemptyingwash_button',
		// ===========  exit Popup ===========
		'click .confirm_exit_popup': 'confirm_exit_popup',
		// ===========  main 3 button ===========
		'click .warehouse': 'warehouse',
		// Add an item button
		'click .display_container_detail': 'display_container_detail',
		'change #barcode_number': 'barcode',
		// lot details wizard
		'click .lot_details_wizard': 'lot_details_wizard',
		// ===========  main 4 button ===========
// Create   wash
		'click .create_wash_order': 'create_wash_order',
		'click .save_wash_order' : 'save_wash_order',
		'click .cancel_wash_order' :'cancel_wash_order',
//onchange wash product
		'click .onchange_product' :'onchange_product',
		'click .main_container_screen': 'main_container_screen',
		// create emptying wash order
		'click  .confirm_prewash': 'confirm_prewash',
		'click  .confirm_startwash': 'confirm_startwash',
                'click	.confirm_emptying' : 'confirm_emptying',
		'click .endprewash_button': 'endprewash_button',
		//'click .create_emptying_wash_order' : 'create_emptying_wash_order',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var operation_data = [];
        var self = this;
        if (context.tag == 'ballester_container_display_screen_act') {
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

       return  self.$el.html(QWeb.render("ContainerDisplay", {widget: self}));
    },
    reload: function () {
        window.location.href = this.href;
    },
    main: function (event) {
        var self = this;

        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
         return  self.do_action('ballester_wash.action_ballester_container_display_screen');
    },
    confirm_exit_popup: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.do_action('ballester_wash.action_ballester_washed_container_screen');
    },
    warehouse: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	
        return  self.$el.html(QWeb.render("WarehouseButton", {widget: self}));
    },

    barcode: function(event) {
	      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
                ctx['display_barcode_details']= "True";
	   	var number_of_barcode = $("#barcode_number").val();
		var emp = self.employee_id
		$('.modal-backdrop').remove();
	   	if (number_of_barcode != ''){

			   	//	 generating barcode
		        self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'search_barcode',
				context : ctx,
		                args: [[],number_of_barcode,emp],		            })
			
                              .then(function(result) {
				if (result.success) {
					$('#barcode_number').attr("disabled", true) 
					$("#table_detail").css("display", "none");
				      $("#image_container").css("display", "none");
					
					if (result.wash_order_data){
					if (result.product_img_url != undefined ){
							console.log("<F@@@@@@@@ffffffff",result.product_img_url)
					
						$("#image_container").css("display", "inline");
							document.getElementById('image_container')
								    .setAttribute(
									'src', 'data:image/png;base64,' + result.product_img_url
					    );
							}
					$("#table_detail").css("display", "inline");
	$( "#table_detail").after(

						"<tr id='tr_detail'><td style='width: 250px;font-size:20px; color:blue'>No of Washing Order: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['order_number'] + "</td></tr><tr id='tr1_detail'> <td style='font-size:20px; color:blue'>  Type Of Order:</td><td style='font-size:20px; color:blue'>"+ result.wash_order_data[0]['type_of_order']+
					  "</td></tr> <tr id='tr2_detail'><td style='font-size:20px; color:blue'> Dangerous characteristics: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['dangerous_characteristics'] + "</td></tr> <tr id='tr3_detail'> <td style='font-size:20px; color:blue'>  Variants:</td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['variants'] +  "</td></tr> <tr id='tr4_detail'> <td style='font-size:20px; color:blue'> <b> State:</b></td><td style='font-size:20px; color:blue'>" +  result.wash_order_data[0]['state'] + "</td></tr> <tr id='tr5_detail'> <td style='font-size:20px; color:blue'>   LER: </td><td style='font-size:20px; color:blue'>" +  result.wash_order_data[0]['ler'] +  "</td></tr> <tr id='tr6_detail'> <td style='font-size:20px; color:blue'>  UN code: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['un_code'] + "</td></tr> <tr id='tr7_detail'> <td style='font-size:20px; color:blue'>  Recycled Product: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['recycled_product'] +"</td></tr>" );
				
					if(result.wash_order_data[0]['state'] == 'start_emptying')
					{       
						$("#prewash_wash_order").css("display", "none");
						$("#end_emptying_wash_order").css("display", "inline");
						$("#create_emptying_wash_order").css("display", "none");
						$("#start_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");


					 }
					else if (result.wash_order_data[0]['state'] == 'start_re_wash')
					{
						$("#prewash_wash_order").css("display", "none");
						$("#end_pre_wash_order").css("display", "inline");
						$("#end_emptying_wash_order").css("display", "none");
						$("#start_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");
						}
					else if (result.wash_order_data[0]['state'] == 'draft')
					{
					        $("#prewash_wash_order").css("display", "inline");
						$("#create_emptying_wash_order").css("display", "inline");
						$("#start_wash_order").css("display", "inline");
						$("#cancel_wash_order_button").css("display", "inline");

				
					}
					else if (result.wash_order_data[0]['state'] == 'stop_emptying')
					{
						$("#prewash_wash_order").css("display", "inline");
						$("#create_emptying_wash_order").css("display", "none");
						$("#start_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");
						}
					else if (result.wash_order_data[0]['state'] == 'stop_re_wash')
					{
						$("#prewash_wash_order").css("display", "none");
						$("#create_emptying_wash_order").css("display", "none");
						$("#start_wash_order").css("display", "inline");
						$("#cancel_wash_order_button").css("display", "none");
						}
					else if (result.wash_order_data[0]['state'] == 'start_wash')
					{
					       $("#prewash_wash_order").css("display", "none");
						$("#create_emptying_wash_order").css("display", "none");
						$("#start_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");
					}
                                      
					}
					
					/** $( "#image_div").after(

		"<img   id='image_container' class='image_container' height='250' width='250'>" +result.wash_order_data[0]['state'] + "</img>"
						); **/
					
					

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

endprewash_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var barcode = $("#barcode_number").val();
	$('.modal-backdrop').remove();
	var number_of_barcode = ''
        if (barcode != undefined){

		number_of_barcode= barcode
	}
	else{
		number_of_barcode = self.barcode
	
	} 
	var ctx = {};
	ctx['end_prewash_order']= "True";
	var emp = self.employee_id 
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
		if (result.success) {
				/**self.state = "stop_re_wash"
				self.start_pre_wash = false
				self.start_wash =true
				 self.end_prewash = false
				if (result.wash_order_data)
				{
					self.img_url = result.wash_order_data[0]['img_url']
				    self.barcode = result.wash_order_data[0]['barcode']
				    self.order_number = result.wash_order_data[0]['order_number']
				    self.order_type = result.wash_order_data[0]['type_of_order']
				    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
				    self.variants = result.wash_order_data[0]['variants']
				    self.ler = result.wash_order_data[0]['ler']
				    self.un_code = result.wash_order_data[0]['un_code']
				    self.recycled_product_name = result.wash_order_data[0]['recycled_product']
				    self.state = result.wash_order_data[0]['state']
				    self.continue_button = true


				}**/
				

				   self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_washed_container_screen');
			         }, 2000);

				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},


endemptyingwash_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var barcode = $("#barcode_number").val();
	var number_of_barcode = ''
	$('.modal-backdrop').remove();
        if (barcode != undefined){

		number_of_barcode= barcode
	}
	else{
		number_of_barcode = self.barcode
	
	} 
	
	var ctx = {};
	ctx['end_emptying_wash_order']= "True";
	var emp = self.employee_id 
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
		if (result.success) {

				/**self.state = "stop_emptying"
                                self.start_pre_wash = true
				 self.end_emptying = false
				if(result.wash_order_data){
				
				 self.img_url = result.wash_order_data[0]['img_url']
				    self.barcode = result.wash_order_data[0]['barcode']
				    self.order_number = result.wash_order_data[0]['order_number']
				    self.order_type = result.wash_order_data[0]['type_of_order']
				    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
				    self.variants = result.wash_order_data[0]['variants']
				    self.ler = result.wash_order_data[0]['ler']
				    self.un_code = result.wash_order_data[0]['un_code']
				    self.recycled_product_name = result.wash_order_data[0]['recycled_product']
				    self.state = result.wash_order_data[0]['state']
				    self.continue_button = true

				
					}**/
				
				   self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_washed_container_screen');
			         }, 2000);

				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},


confirm_emptying: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var number_of_barcode = $("#barcode_number").val(); 
	var ctx = {};
	var emp = self.employee_id 
	ctx['emptying_wash_order']= "True";
	$('.modal-backdrop').remove();
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
		if (result.success) {
				
				/**self.start_emptying = true
				if (result.wash_order_data){

			            self.img_url = result.wash_order_data[0]['img_url']
				    self.barcode = result.wash_order_data[0]['barcode']
				    self.order_number = result.wash_order_data[0]['order_number']
				    self.order_type = result.wash_order_data[0]['type_of_order']
				    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
				    self.variants = result.wash_order_data[0]['variants']
				    self.ler = result.wash_order_data[0]['ler']
				    self.un_code = result.wash_order_data[0]['un_code']
				    self.recycled_product_name = result.wash_order_data[0]['recycled_product']
				    self.state = result.wash_order_data[0]['state']
				    self.continue_button = true
				    self.end_emptying = true
                                
				}**/

				
				$('.modal-backdrop').remove();
				//return  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				self.$el.html(QWeb.render("ConfirmWash", {widget: self}));				

				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_washed_container_screen');
			         }, 2000);
				

				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},


confirm_prewash: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var barcode = $("#barcode_number").val();
	var number_of_barcode = ''
        if (barcode != undefined){

		number_of_barcode= barcode
	}
	else{
		number_of_barcode = self.barcode
	
	} 
	var ctx = {};
	ctx['pre_wash_order']= "True";
	$('.modal-backdrop').remove();
	var emp = self.employee_id 
        console.log('ddddddddddd$$$$$$$$$$$$$$$')
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode, emp],
               }) 
		.then(function(result){
		if (result.success) {
			
				/**self.state = 'start_pre_wash'

			     if (result.wash_order_data){

			            self.img_url = result.wash_order_data[0]['img_url']
				    self.barcode = result.wash_order_data[0]['barcode']
				    self.order_number = result.wash_order_data[0]['order_number']
				    self.order_type = result.wash_order_data[0]['type_of_order']
				    self.dangerous_char = result.wash_order_data[0]['dangerous_characteristics']
				    self.variants = result.wash_order_data[0]['variants']
				    self.ler = result.wash_order_data[0]['ler']
				    self.un_code = result.wash_order_data[0]['un_code']
				    self.recycled_product_name = result.wash_order_data[0]['recycled_product']
				    self.state = result.wash_order_data[0]['state']
			            self.end_prewash = true
				    self.end_emptying = false
				   self.start_pre_wash = false
				   self.continue_button = true
                                
				}**/
				$('.modal-backdrop').remove();
				  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));

				
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_washed_container_screen');
			         }, 2000);
				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},

confirm_startwash: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var barcode = $("#barcode_number").val();
	var number_of_barcode = ''
        if (barcode != undefined){

		number_of_barcode= barcode
	}
	else{
		number_of_barcode = self.barcode
	
	} 
	var ctx = {};
	var emp = self.employee_id 
	$('.modal-backdrop').remove();
	ctx['start_wash_order']= "True";
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
		if (result.success) {


				/**self.state = 'start_wash'
				self.continue_button = false
				self.end_prewash = false	
				self.start_wash = false **/
			$('.modal-backdrop').remove();
			
			  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
			
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_washed_container_screen');
			         }, 2000);

				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},


// create wash order

	create_wash_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id = $(".es-list li[value='" + $(".product_wash").val() + "']").attr('ids');
                var recycled_product_id =  $(".es-list li[value='" + $(".product_recycled").val() + "']").attr('ids');
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
		var type_of_order = $(".select").val() ;
               var barcode_ids =  $("#barcode_wash").attr("ids");
		$('.modal-backdrop').remove();
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
	   	var report_data = [];
	   	if (location != undefined &&  product_id != undefined   &&  recycled_product_id != undefined   && dest_location_id != undefined  &&  type_of_order != undefined){
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': type_of_order,
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
 				});
			self._rpc({
			        model: 'operation.wash.dashboard',
			        method: 'create_wash_order_method',
			        args: [[],report_data ],
			    })
	            .then(function(result) {
	            	if (result.success) {
	            		return self.$el.html(QWeb.render("Confirm", {widget: self}));
	            	}else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
  }
},


// Confirm main screen

	main_container_screen : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		$('.modal-backdrop').remove();
	      return  self.do_action('ballester_wash.action_ballester_washed_container_screen');
},


// save wash order

       save_wash_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                var product_id = $(".es-list li[value='" + $(".product_wash").val() + "']").attr('ids');
                var recycled_product_id =  $(".es-list li[value='" + $(".product_recycled").val() + "']").attr('ids');
                var dest_location_id =  $(".es-list li[value='" + $(".dest_locations").val() + "']").attr('ids');
                var barcode_ids =  $("#barcode_wash").attr("ids");
		var type_of_order = $(".select").val() ;
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
		if (type_of_order == undefined ){
			self.do_warn(_("Warning"),_("Please Select Order Type!"));
		}
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		if (location != undefined &&  product_id != undefined   &&  recycled_product_id != undefined   && dest_location_id != undefined  &&  type_of_order != undefined) {
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': type_of_order,
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list

 				});
                        console.log("-----report_data-----------",report_data)
			self._rpc({
			        model: 'operation.wash.dashboard',
			        method: 'save_wash_order_method',
			        args: [[],report_data ],
			    })

	            .then(function(result) {

	            	if (result.success) {
	            		self.do_warn(_("Success"),_("Record Saved"));
	            		// hide validate barcode button
	            		$("#edit_wash_order_button").css("display", "inline");
	            		$("#create_destruction_order_button").css("display", "inline");
				$("#create_wash_order_button").css("display", "inline");
				$("#save_wash_order_button").css("display", "none");
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

// cancel wash order

       cancel_wash_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
    		// cancel all data
    		$("#image_container").css("display", "none");
		$("#table_detail").css("display", "none");
		$("#create_emptying_wash_order").css("display", "none");
		$("#prewash_wash_order").css("display", "none");
		$("#start_wash_order").css("display", "none");
		$("#tr_detail").css("display", "none");
		$("#tr1_detail").css("display", "none");
		$("#tr4_detail").css("display", "none");
		$("#tr2_detail").css("display", "none");
		$("#tr3_detail").css("display", "none");
		$("#tr5_detail").css("display", "none");
		$("#tr6_detail").css("display", "none");
		$("#tr7_detail").css("display", "none");
	},


// onchnage wash product

       onchange_product : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
                var product_id = $(".es-list li[value='" + $(".product_wash").val() + "']").attr('ids');
		var type_of_order = $(".select").val() ;
	   	var report_data = [];
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

	 lot_details_wizard :function(event){
	       var self = this;
	       event.stopPropagation();
	       event.preventDefault();
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
core.action_registry.add('ballester_container_display_screen_act', ContainerDisplayScreen);

return ContainerDisplayScreen;

});
