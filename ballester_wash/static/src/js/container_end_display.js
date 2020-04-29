/** -*- coding: utf-8 -*-
 Odoo, Open Source Ballester Screen.
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('ballester_wash.container_end_display', function (require) {
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


var ContainerEndDisplayScreen = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
//		'click .continue_button': 'continue_button',
		// ===========  main screen ===========
		'click .main': 'main',
		//'click .product_wash' :'product_wash',
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
		'click .display_container_detail': 'display_container_detail',
		// Validate Barcode  button
		'click .validate_barcode': 'validate_barcode',
		'change #barcode_number': 'barcode',
		// lot details wizard
		// ===========  main 4 button ===========
// Create   wash
		'click .endwash_button': 'endwash_button',
		'click .destructionwash_button' : 'destructionwash_button',
		'click .backto_wash_button' :'backto_wash_button',
//onchange wash product
		'click .onchange_product' :'onchange_product',
		'click .endemptyingwash_button':'endemptyingwash_button',
		'click .endprewash_button':'endprewash_button',
		'click .main_container_screen': 'main_container_screen',
		//'click .create_emptying_wash_order' : 'create_emptying_wash_order',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var operation_data = [];
        var self = this;
        if (context.tag == 'ballester_container_end_display_screen_act') {
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

       return  self.$el.html(QWeb.render("ContainerEndDisplay", {widget: self}));
    },
    reload: function () {
        window.location.href = this.href;
    },
    main: function (event) {
        var self = this;
      console.log(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

        event.stopPropagation();
	$('.modal-backdrop').remove();
        event.preventDefault();
        return  self.do_action('ballester_wash.action_ballester_container_end_display_screen');
    },
    confirm_exit_popup: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.do_action('ballester_wash.action_ballester_end_washed_container_screen');
    },
    entry_of_products: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return  self.$el.html(QWeb.render("EntryOfProductsButton", {widget: self}));
    },
    output_of_products: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return  self.$el.html(QWeb.render("OutputOfProductsButton", {widget: self}));
    },
    warehouse: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return  self.$el.html(QWeb.render("WarehouseButton", {widget: self}));
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
    display_container_detail: function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
                ctx['display_barcode_details']= "True";
	   	var number_of_barcode = $("#barcode_number").val();
		var emp = self.employee_id
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
				$("#image_container").css("display", "inline");
				document.getElementById('image_container')
					    .setAttribute(
						'src', 'data:image/png;base64,' + result.product_img_url
					    );
					$("#table_detail").css("display", "inline");
					$("#destruction_wash_order").css("display", "inline");
					$("#backto_wash_order").css("display", "inline");
					$("#end_wash_order").css("display", "inline");
					$("#cancel_wash_order_button").css("display", "inline");

					$( "#table_detail").after(

						"<tr id='tr_detail'><td style='width: 250px;font-size:20px; color:blue'>No of Washing Order: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['order_number'] + "</td></tr><tr id='tr1_detail'> <td style='font-size:20px; color:blue'>  Type Of Order:</td><td style='font-size:20px; color:blue'>"+ result.wash_order_data[0]['type_of_order']+
					  "\</td></tr> <tr id='tr2_detail'><td style='font-size:20px; color:blue'> Dangerous characteristics: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['dangerous_characteristics'] + "</td></tr> <tr id='tr3_detail'> <td style='font-size:20px; color:blue'>  Variants:</td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['variants'] +  "</td></tr> <tr id='tr4_detail'> <td style='font-size:20px; color:blue'> <b> State:</b></td><td style='font-size:20px; color:blue'>" +  result.wash_order_data[0]['state'] + "</td></tr> <tr id='tr5_detail'> <td style='font-size:20px; color:blue'>   LER: </td><td style='font-size:20px; color:blue'>" +  result.wash_order_data[0]['ler'] +  "</td></tr> <tr id='tr6_detail'> <td style='font-size:20px; color:blue'>  UN code: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['un_code'] + "</td></tr> <tr id='tr7_detail'> <td style='font-size:20px; color:blue'>  Recycled Product: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['recycled_product'] +"</td></tr>" );
					if(result.wash_order_data[0]['state'] == 'stop_emptying')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");
						
					}
					else if( result.wash_order_data[0]['state'] == 'stop_re_wash')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");					
						
						}
					else if( result.wash_order_data[0]['state'] == 'end_wash')
					{
							$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");	
					}

					else if( result.wash_order_data[0]['state'] == 'start_wash')
					{
						$("#end_wash_order").css("display", "inline");
						$("#backto_wash_order").css("display", "inline");
						$("#destruction_wash_order").css("display", "inline");
						$("#cancel_wash_order_button").css("display", "inline");
						$("#end_emptying_wash_order").css("display", "none");
						$("#end_pre_wash_order").css("display", "none");	
					}
					else if( result.wash_order_data[0]['state'] == 'start_emptying')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#end_emptying_wash_order").css("display", "inline");
						$("#end_pre_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");	
					}
					else if( result.wash_order_data[0]['state'] == 'start_re_wash')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#end_emptying_wash_order").css("display", "none");
						$("#end_pre_wash_order").css("display", "inline");
						$("#destruction_wash_order").css("display", "none");
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

    barcode: function(event) {
      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
                ctx['display_barcode_details']= "True";
		$('.modal-backdrop').remove();
		var emp = self.employee_id
	   	var number_of_barcode = $("#barcode_number").val();
	   	if (number_of_barcode != ''){

			   	//	 generating barcode
		        self._rpc({
		                model: 'operation.wash.dashboard',
		                method: 'search_barcode',
				context : ctx,
		                args: [[],number_of_barcode,emp ],		            })
			
                              .then(function(result) {
				if (result.success) {
					$('#barcode_number').attr("disabled", true) 
					$("#table_detail").css("display", "none");
				      $("#image_container").css("display", "none");
					if (result.wash_order_data){
				$("#image_container").css("display", "inline");
				if(result.product_img_url != undefined)  {
				document.getElementById('image_container')
					    .setAttribute(
						'src', 'data:image/png;base64,' + result.product_img_url
					    );}
					$("#table_detail").css("display", "inline");
					

					$( "#table_detail").after(

						"<tr id='tr_detail'><td style='width: 250px;font-size:20px; color:blue'>No of Washing Order: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['order_number'] + "</td></tr><tr id='tr1_detail'> <td style='font-size:20px; color:blue'>  Type Of Order:</td><td style='font-size:20px; color:blue'>"+ result.wash_order_data[0]['type_of_order']+
					  "</td></tr> <tr id='tr2_detail'><td style='font-size:20px; color:blue'> Dangerous characteristics: </td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['dangerous_characteristics'] + "</td></tr> <tr id='tr3_detail'> <td style='font-size:20px; color:blue'>  Variants:</td><td style='font-size:20px; color:blue'>" + result.wash_order_data[0]['variants'] +  "</td></tr> <tr id='tr4_detail'> <td style='font-size:20px; color:blue'> <b> State:</b></td><td style='font-size:20px; color:blue'>" +  result.wash_order_data[0]['state'] + "</td></tr> <tr id='tr5_detail'> <td style='font-size:20px; color:blue'>   LER: </td><td style='font-size:20px; color:blue'>" +  result.wash_order_data[0]['ler'] +  "</td></tr> <tr id='tr6_detail'> <td style='font-size:20px; color:blue'>  UN code: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['un_code'] + "</td></tr> <tr id='tr7_detail'> <td style='font-size:20px; color:blue'>  Recycled Product: </td><td style='font-size:20px; color:blue'>" 
+ result.wash_order_data[0]['recycled_product'] +"</td></tr>" );

					if(result.wash_order_data[0]['state'] == 'stop_emptying')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");
						
					}
					else if( result.wash_order_data[0]['state'] == 'stop_re_wash')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");					
						
						}
					else if( result.wash_order_data[0]['state'] == 'end_wash')
					{
							$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");	
					}

					else if( result.wash_order_data[0]['state'] == 'start_wash')
					{
						$("#end_wash_order").css("display", "inline");
						$("#backto_wash_order").css("display", "inline");
						$("#destruction_wash_order").css("display", "inline");
						$("#cancel_wash_order_button").css("display", "none");
						$("#end_emptying_wash_order").css("display", "none");
						$("#end_pre_wash_order").css("display", "none");	
					}
					else if( result.wash_order_data[0]['state'] == 'start_emptying')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#end_emptying_wash_order").css("display", "inline");
						$("#end_pre_wash_order").css("display", "none");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");	
					}
					else if( result.wash_order_data[0]['state'] == 'start_re_wash')
					{
						$("#end_wash_order").css("display", "none");
						$("#backto_wash_order").css("display", "none");
						$("#end_emptying_wash_order").css("display", "none");
						$("#end_pre_wash_order").css("display", "inline");
						$("#destruction_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");	
					}

                                      
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



/** create_emptying_wash_order: function(event){
   	 var self = this;
        event.stopPropagation();
        event.preventDefault();
	
       return self.do_action({
	            name: _t("Confirm"),
	            type: 'ir.actions.client',
	            tag: 'ConfirmEmptying',
	            target: 'new'
	          })


    },**/

endwash_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var number_of_barcode = $("#barcode_number").val(); 
	var ctx = {};
	$('.modal-backdrop').remove();
	var emp = self.employee_id
	ctx['end_wash_order']= "True";
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
		if (result.success) {
				$('.modal-backdrop').remove();
				  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_end_washed_container_screen');
			         }, 2000);

				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},

endprewash_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var number_of_barcode = $("#barcode_number").val(); 
	var ctx = {};
	$('.modal-backdrop').remove();
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
				$('.modal-backdrop').remove();
				  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_end_washed_container_screen');
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
	$('.modal-backdrop').remove();
	var number_of_barcode = $("#barcode_number").val(); 
	var ctx = {};
	var emp = self.employee_id
	ctx['end_emptying_wash_order']= "True";
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode, emp],
               }) 
		.then(function(result){
		if (result.success) {
				$('.modal-backdrop').remove();
				  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_end_washed_container_screen');
			         }, 2000);
				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},


backto_wash_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var number_of_barcode = $("#barcode_number").val(); 
	var reason_text = $("#backorder_reason").val(); 
	var ctx = {};
	ctx['backto_wash_order']= "True";
	ctx['reason'] = reason_text;
	$('.modal-backdrop').remove();
	var emp = self.employee_id
        console.log('ddddddddddd$$$$$$$$$$$$$$$')
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
		if (result.warning) {
			console.log('>>>>>>>>>>>>>>>>>',result)
			self.do_warn(_("Warning"),_("Please enter reason for back to Wash!"));
			
				}
		if (result.success){
				$('.modal-backdrop').remove();
	            		 self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
				 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_end_washed_container_screen');
			         }, 2000);
	            	}

           
        });

},

destructionwash_button: function(event){
	var self = this;
        event.stopPropagation();
        event.preventDefault();
	var number_of_barcode = $("#barcode_number").val(); 
	var ctx = {};
	$('.modal-backdrop').remove();
	ctx['destruction_wash_order']= "True";
       var emp = self.employee_id
     	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'search_barcode',
		context : ctx,
                args: [[],number_of_barcode,emp],
               }) 
		.then(function(result){
		if (result.success) {
			$('.modal-backdrop').remove();
			  self.$el.html(QWeb.render("ConfirmWash", {widget: self}));
			 setTimeout(function () {
				self.do_action('ballester_wash.action_ballester_end_washed_container_screen');
			         }, 2000);

				}
		else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}

           
        });

},



    product_wash: function(event){
   	 var self = this;
        event.stopPropagation();
        event.preventDefault();
	var ctx = {};
        console.log(">>>>>>>sssssssssssss>>>>>>>>>>>>>",self)
	var product_id = $(".es-list li[value='" + $(".product_wash").val() + "']").attr('ids');
	var recycled_product_id = $(".es-list li[value='" + $(".product_recycled").val() + "']").attr('ids');
	console.log(">>>>>>>sssssssssssss>>>>>>>>>>>>>",product_id,recycled_product_id)
	var type_of_order = $(".select").val() ;
	ctx['product_id']= product_id
	$('.modal-backdrop').remove();
	if (recycled_product_id == undefined){
	$(".product_recycled").editableSelect();
     $('#my-wash-product')
		       .editableSelect()
		       .on('select.editable-select', function (e, li) {
		    	   var recycled_pro = event.target.getAttribute("recycled_product_id");
				console.log(">>>>>>>recycled_pro>>>>>>>>>>>>>",recycled_pro)
		           var product_id =  $(".es-list li[value='" + $(".product_wash").val() + "']").attr('ids');

		           var current_product_id = $(this).find('#my-wash-product').val();
			           if(current_product_id === product_id){
			        	   $(this).find('#my-recycled-product').val(recycled_pro)
		           }
})
                 $("#recycled").after(" <div class='col-md-3' style='width:350px'>"+ self.recycled_product + "</div>"

		);}
    },

    add_an_item: function(event){
	       var self = this;
	       event.stopPropagation();
		$('.modal-backdrop').remove();
	       event.preventDefault();
	       var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
		   if (location == undefined){
		   		if ($("#set_loction_id").length > 0){
		   			location = $("#set_loction_id").text()
		   		}
		   	}
	       if (location != undefined){
		       var table = document.getElementById("inventory_adjustments_table");
		       var table_row = document.getElementById("inventory_adjustments_table").rows;
		       if (table_row.length > 2){
		    	   $( "#inventory_adjustments_table tr:nth-last-child(2)").after("<tr class='active'>"+
		    			   "<td style='width: 25%;' >"+self.product_list+"</td>"+
		    			   "<td style='width: 15%; position:absolute;'> <input type='text' name='ler_code_txt' id='ler_code_id' readonly='readonly' /></td>"+
		    			   "<td style='width: 20%;' id='barcode'>"+self.barcode_list+"</td>"+
		    			   "<td style='width: 20%; position:absolute;'> <input type='text' name='life_date' class='life_datetimepicker' /></td>"+
		    			   "<td style='width: 5%;'> <input type='hidden' name='line_id'  value='none' /> </td>"+
		    			   "<td style='width: 5%;'><button class='fa fa-trash-o btndelete' name='delete' aria-hidden='true'/></td>"+
		    			   "<td style='width: 5%; display:none;'></td>"+
		    			   "<td style='width: 5%;' class='set_lot_details_ids'><button id='lot_details_id' class='fa fa-bars lot_details_wizard'  aria-hidden='true'></button></td>"+
		    			   "</tr>");
		       }else{
		    	   $('#inventory_adjustments_table').prepend("<tr class='active'>"+
		    			   "<td style='width: 25%;'>"+self.product_list+"</td>" +
		    			   "<td style='width: 15%; position:absolute;'> <input type='text' name='ler_code_txt' id='ler_code_id'  readonly='readonly'/></td>"+
		    			   "<td style='width: 20%;' id='barcode'>"+self.barcode_list+"</td>"+
		    			   "<td style='width: 20%; position:absolute;'> <input type='text' name='life_date' class='life_datetimepicker' /></td>"+
		    			   "<td style='width: 5%;'> <input type='hidden' name='line_id' value='none' /></td>"+
		    			   "<td style='width: 5%;'><button class='fa fa-trash-o btndelete' name='delete' aria-hidden='true'/></td>"+
		    			   "<td style='width: 5%; display:none;'></td>"+
		    			   "<td style='width: 5%;' class='set_lot_details_ids'><button id='lot_details_id' class='fa fa-bars lot_details_wizard'  aria-hidden='true'></button></td>"+
		    			   "</tr>");
		       }
		       $(".barcodes").editableSelect();
		       $('.products')
		       .editableSelect()
		       .on('select.editable-select', function (e, li) {
		           var ler_code = li.attr('product_ler_code');
		           var product_id = li.text();
		           var row_ids = $('.products').closest('tr')
		           row_ids.each(function(i){
		           var current_product_id = $(this).find('.products').val();
			           if(current_product_id === product_id){
			        	   $(this).find('td #ler_code_id').val(ler_code)
			           }
		           })
		       });
		        var today = new Date();
		        var deafult_date = new Date(today.getFullYear() + 1,  today.getMonth(),today.getDate(),today.getHours(),today.getMinutes(),today.getSeconds())
		       $('.life_datetimepicker').datetimepicker({format: 'MM/DD/YYYY hh:mm:ss',
		    	   locale:  moment.locale('es'),
		    	   defaultDate: deafult_date,
		    	   widgetPositioning:{ horizontal: 'auto',vertical: 'bottom' },
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
	    return  self.do_action('ballester_wash.action_ballester_end_washed_container_screen');
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
core.action_registry.add('ballester_container_end_display_screen_act', ContainerEndDisplayScreen);

return ContainerEndDisplayScreen;

});
