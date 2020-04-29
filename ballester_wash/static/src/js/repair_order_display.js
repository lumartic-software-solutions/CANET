/** -*- coding: utf-8 -*-
 Odoo, Open Source Ballester Screen.
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('ballester_wash.repair_order_display', function (require) {
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


var REpairOrderDisplay = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
//		'click .continue_button': 'continue_button',
		// ===========  main screen ===========
		'click .main': 'main',
		//'click .product_wash' :'product_wash',
		'click .my_profile': 'action_my_profile',
		// ===========  exit Popup ===========
		'click .confirm_exit_popup': 'confirm_exit_popup',
		'click .add_repair_part':'add_repair_part',
		// Add an item button
		'click .display_container_detail': 'display_container_detail',
		'change #barcode_number': 'barcode',
		// lot details wizard
		'click .lot_details_wizard': 'lot_details_wizard',
		// ===========  main 4 button ===========
// Create   wash
		'click .create_wash_order': 'create_wash_order',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var operation_data = [];
        var self = this;
        if (context.tag == 'ballester_repair_order_act') {
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

       return  self.$el.html(QWeb.render("RepairOrderDisplay", {widget: self}));
    },
    reload: function () {
        window.location.href = this.href;
    },
    main: function (event) {
        var self = this;
    $('.modal-backdrop').remove();

        event.stopPropagation();
        event.preventDefault();
        return self.$el.html(QWeb.render("RepairOrderDisplay", {widget: self}));
    },
    confirm_exit_popup: function (event) {
        var self = this;
        event.stopPropagation();
	$('.modal-backdrop').remove();
        event.preventDefault();
        return  self.do_action('ballester_wash.action_ballester_container_drying_display_screen');
    },

    barcode: function(event) {
	      	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
		var ctx = {};
		$('.modal-backdrop').remove();
                ctx['display_barcode_details']= "True";
		var emp = self.employee_id 
	   	var number_of_barcode = $("#barcode_number").val();
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
						$("#create_emptying_wash_order").css("display", "none");
						$("#start_wash_order").css("display", "none");
						$("#cancel_wash_order_button").css("display", "none");


					 }
					else if (result.wash_order_data[0]['state'] == 'start_re_wash')
					{
						$("#prewash_wash_order").css("display", "none");
						$("#create_emptying_wash_order").css("display", "none");
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

add_repair_part: function(event){
	var self = this; 
       event.stopPropagation();
       event.preventDefault();
	var repair_order = self.repair_order;
	var number_of_barcode = self.barcode; 
	var ctx = {};
	ctx['add_repiar_parts']= "True";
	var table = document.getElementById("repair_parts_table");    
        var table_row = document.getElementById("repair_parts_table").rows;
	$('.modal-backdrop').remove();
	 self._rpc({
                model: 'operation.wash.dashboard',
                method: 'get_repair_data',
		context : ctx,
                args: [[],repair_order],
               }) 
		.then(function(result){
		if (result.success) {
			
     	if (table_row.length > 2){
		    	   $( "#repair_parts_table tr:nth-last-child(2)").after("<tr class='active'>"+
		    			   "<td style='width: 25%;' >"+ result.product_list + "</td>"+
		    			   "<td style='width: 15%; position:absolute;'> <input type='text' name='product_description' id='product_description_id' readonly='readonly' /></td>"+
		    			   "<td style='width: 15%;' id='barcode'>"+result.barcode_list+"</td>"+
		    			  
		    			   "<td style='width: 15%;'>"+ result.location_list +  "</td>"+
		    			   "<td style='width: 15%;'>"+ result.location_list + "</td>" +
					 "<td style='width: 10%; position:absolute;'> <input type='number' name='qty' class='product_qty' value=1.0/></td>"+
		    			  
		    			   "<td style='width: 5%;'><button class='fa fa-trash-o btndelete' name='delete' aria-hidden='true'/></td>"+
		    			   "</tr>");
		       }
			else{
			$( '#repair_parts_table').prepend("<tr class='active'>"+
		    			   "<td style='width: 25%;' >"+result.product_list+"</td>"+
		    			   "<td style='width: 15%; position:absolute;'> <input type='text' name='product_description' id='product_description_id' readonly='readonly' /></td>"+
		    			   "<td style='width: 15%;' id='barcode'>"+result.barcode_list+"</td>"+
		    			  
		    			   "<td style='width: 15%;'>"+ result.location_list +  "</td>"+
		    			   "<td style='width: 15%;'>"+ result.location_list + "</td>" +
					 "<td style='width: 10%; position:absolute;'> <input type='number' name='qty' class='product_qty' value=1.0/></td>"+
		    			   
		    			   "<td style='width: 5%;'><button class='fa fa-trash-o btndelete' name='delete' aria-hidden='true'/></td>"+
		    			   "</tr>");


			}
			
			$(".locations").editableSelect();
		       $(".barcodes").editableSelect();
		       $('.products')
		       .editableSelect()
		       .on('select.editable-select', function (e, li) {
		           var product_description = li.attr('product_description');
		           var product_id = li.text();
		           var row_ids = $('.products').closest('tr')
		           row_ids.each(function(i){
		           var current_product_id = $(this).find('.products').val();
			           if(current_product_id === product_id){
			        	   $(this).find('td #product_description').val(product_description)
			           }
		           })
		       });
		       
		}
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
core.action_registry.add('ballester_repair_order_act', REpairOrderDisplay);

return REpairOrderDisplay;

});
