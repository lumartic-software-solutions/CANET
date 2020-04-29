/** -*- coding: utf-8 -*-
 Odoo, Open Source Ballester Screen.
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). 
*/
odoo.define('ballester_screen.screen', function (require) {
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


var BallesterScreen = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
		'click .main': 'main',
		'click .my_profile': 'action_my_profile',
		// ===========  exit Popup ===========
		'click .confirm_exit_popup': 'confirm_exit_popup',
		// ===========  main 1 button ===========
		'click .entry_of_products': 'entry_of_products',
		// ===========  main 2 button ===========
               'click .output_of_products': 'output_of_products',
		// ===========  main 3 button ===========
		'click .warehouse': 'warehouse',
		'click .inventory_adjustments': 'inventory_adjustments',
		'click .internal_transfers': 'internal_transfers',
		// Add an item button
		'click .add_an_item': 'add_an_item',
		// Save Barcode  button
		'click .save_inventory_adjustments': 'save_inventory_adjustments',
		// Edit Barcode  button
		'click .edit_inventory_adjustments': 'edit_inventory_adjustments',
		// delete  button
		'click .create_internal_transfer_button':'create_internal_transfer_button',
		'click .btndelete': 'btndelete',
		// Validate Barcode  button
		'click .validate_barcode': 'validate_barcode',
		// Print Barcode  button
		'click .print_barcode': 'print_barcode',
		// lot details wizard 
		'click .lot_details_wizard': 'lot_details_wizard',
		// ===========  main 4 button =========== 
		'click .generate_barcode': 'generate_barcode',
		'click .generate': 'generate',
		'click .create_destruction_order_confirm':'create_destruction_order_confirm',
		'click .print_generate_barcode': 'print_generate_barcode',
		'click .print_multi_barcode': 'print_multi_barcode',
		'click .create_wash_order': 'create_wash_order',
		'click .save_wash_order' : 'save_wash_order',
		'click .edit_wash_order' :'edit_wash_order',
		'click .onchange_product' :'onchange_product',
		'click .main_button': 'main_button',
		'change #washing_type' : 'washingOnChangeEvent',
		'change #type-select' : 'TypeOrderOnChangeEvent',
		'change #categ_select_id' : 'CategoryOnChangeEvent',
		//'change #my-wash-product' : 'ProductOnChangeEvent',
		'change #barcode_wash' : 'LotOnChangeEvent',
		'change #my-select' : 'LocationOnChangeEvent',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var operation_data = [];
        var self = this;
        if (context.tag == 'ballester_screen_act') {
            self._rpc({
                model: 'operation.dashboard',
                method: 'get_operation_info',
            }, []).then(function(result){
            	self.operation_data = result[0]
                //self.product_list = self.operation_data.product_list
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
       return  self.$el.html(QWeb.render("MainMenu", {widget: self}));       
    },
    reload: function () {
        window.location.href = this.href;
    },
    main: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
        return self.$el.html(QWeb.render("MainMenu", {widget: self}));
    },
    confirm_exit_popup: function (event) {
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.do_action('member_barcode_scanner.member_action_kiosk_mode');
    },
    entry_of_products: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.$el.html(QWeb.render("EntryOfProductsButton", {widget: self}));
    },
    output_of_products: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.$el.html(QWeb.render("OutputOfProductsButton", {widget: self}));
    },
    warehouse: function(event){
        var self = this;
        event.stopPropagation();
        event.preventDefault();
	$('.modal-backdrop').remove();
        return  self.$el.html(QWeb.render("WarehouseButton", {widget: self}));
    },
    generate_barcode: function(event){
    	 var self = this;
         event.stopPropagation();
         event.preventDefault();
         self._rpc({
             model: 'operation.dashboard',
             method: 'get_operation_info',
         }, []).then(function(result){
            self.operation_data = result[0]
            self.product_list = self.operation_data.product_list
//            self.ler_list = self.operation_data.ler_list
            self.barcode_list = self.operation_data.barcode_list
            self.set_unused_barcode_list = self.operation_data.set_unused_barcode_list
            self.unused_barcode_list = self.operation_data.unused_barcode_list
	    self.used_set_barcode_list = self.operation_data.used_set_barcode_list
            self.employee_id = session.employee_id
            self.employee = session.employee 
            self.employee_image_url = session.employee_image_url
         }).done(function(){
        	 self.href = window.location.href;
        	 return  self.$el.html(QWeb.render("GenerateBarcodeButton", {widget: self}));
         });
    },
//  selectign barcode from wash product
    barcode_wash: function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
	   	var number_of_barcode = $("#number_of_barcode").val();
		$('.modal-backdrop').remove();
	   	if (number_of_barcode != ''){	   	
			   	//	 generating barcode
		        self._rpc({
		                model: 'operation.dashboard',
		                method: 'select_barcode',
		                args: [[],number_of_barcode],
		            })
	   		 }
				else{
	    	   self.do_warn(_("Warning"),_("Please Enter the Number First!"));
	       }
	  },

 washingOnChangeEvent: function (event)
    {	
    	console.log("=====this",this);
        var selectedValue = document.getElementById('washing_type').value;
        var ordertype = document.getElementById('type-select').value;
	if (ordertype == ''){
			
		self.do_warn(_("Warning"),_("Please Enter the Order Type First!")); 
	}
    var domain_dp = []
            domain_dp.push(['type_product', '=', ordertype.toLowerCase()])
            domain_dp.push([selectedValue.toLowerCase(), '=', true])
    this._rpc({
            model: 'dangerous.product',
            method: 'search_read',
            domain: domain_dp,
        })
        .then(function (result) {
        	$('#dnproduct_table').remove();
        	var product_table =
			"<div  style='text-align: left; font-size: 15px; margin-top: 20px;margin-left:30px;margin-right:150px'>" + 
			"<table id='dnproduct_table'class='table'>" +
			"<th><span>Product</span></th>" +
			"<th><span>Quantity</span></th>"
        	for(var dnproduct in result){
        		product_table += "<tr><td>"+result[dnproduct]['product_id'][1]+"</td>" +
        				"<td>"+result[dnproduct]['qty']+"</td></tr>" +
        						"</table>"
        	}
		product_table +="</div>"
		$('.modal-backdrop').remove();
        	$("#recyled_product_div").after(product_table);
        });
    },


  LocationOnChangeEvent: function (event)
    {	
       var selectedLOcationValue = document.getElementById('my-select').value;
        var location1 
	var location2 
        var length
	    if (selectedLOcationValue != undefined){

		var first_step = selectedLOcationValue.split("/")
                var obj_len = Object.keys(first_step).length
		      location1 = first_step[0]
		      location2 = first_step[obj_len - 1]
                      length = obj_len
            	
		}
        this._rpc({
            model: 'operation.dashboard',
            method: 'location_data',
            args: [location1,location2,length ],
        })
        .then(function (result) {
		if (result.lot_list){
		var lot = result.lot_list  
		if(lot.length != 0)
		{
		  $('#barcode_wash').select2('val', []);
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
		     $('#barcode_wash').empty();
		}

	}
		  
        });
    },

 CategoryOnChangeEvent: function (event)
    {	
	var self = this;
       var selectedCategoryValue = document.getElementById('categ_select_id').value;
  if (selectedCategoryValue != undefined){

        this._rpc({
            model: 'operation.dashboard',
            method: 'categ_data',
            args: [selectedCategoryValue],
        })
        .then(function (result) {
		if(result.product_selection){
			
			self.product_list = result.product_selection
		
		}
		if(result.cat_product_list){
			
			self.cat_product_list = result.cat_product_list
		
		}
				  
        });

	}
    },


 LotOnChangeEvent: function (event)
    {	
        var selectedlotValue = document.getElementById('barcode_wash').value;
        var domain_dp = []
	    if (selectedlotValue != undefined){

		
            	domain_dp.push(['name', '=', selectedlotValue])
		}
        this._rpc({
            model: 'operation.dashboard',
            method: 'lot_data',
            args: [domain_dp],
        })
        .then(function (result) {
               if (result != undefined){
               if(result.product_name != ''){

		var productvalue = document.getElementById('my-wash-product').value;
		if (productvalue != undefined)
		{
			$('#my-wash-product').append(result.product_name);
		}
		$('#my-wash-product').select2('data', {text: result.product_name});

		}
	       else {
		 $('#my-wash-product').select2('val', []);

		}

		if(result.recycled_product_name != ''){

		$('#my-recycled-product').select2('data', {text: result.recycled_product_name});

		}
	       else {
		 $('#my-recycled-product').select2('val', []);

		}
		  }
        });

},

 /**ProductOnChangeEvent: function (event)
    {	
        var selectedproductValue = document.getElementById('my-wash-product').value;
            console.log("=====selectedValue",selectedproductValue)
        var domain_dp = []
	    if (selectedproductValue != undefined){

		var first_step = selectedproductValue.split("[")
		console.log("<<<<<<<<first_step<<<<<<<<SDCdf", first_step)
		var second_step = first_step[1].split("]")
		console.log("<<<<<<<<seond<<<<<<<<SDCdf", second_step.lenght)
		
		
            	domain_dp.push(['default_code', '=', second_step[0]])
		console.log("%%%%%%%%%domain_dp%%%%%%%%%%",domain_dp )
		}
        this._rpc({
            model: 'operation.dashboard',
            method: 'product_data',
            args: [domain_dp],
        })
        .then(function (result) {
               if(result.product_name != ''){

		    console.log(">>>>>>>>>CDFVFD", result.product_name)
	        //$('#my-recycled-product').val(result.product_name)
               //$('#my-recycled-product').select2().trigger('change');
	    // $('#my-recycled-product').val('Hello').trigger('change');
		$('#my-recycled-product').select2('data', {text: result.product_name});
//$("#my-recycled-product").select2().val(result.product_name);

		}
	       else {
		console.log(">>>>@@@@@@@@@@FD")
		 $('#my-recycled-product').select2('val', []);

		}
		console.log("sssssssssssssssssss", result.lot_list)
		var lot = result.lot_list  
		if(lot.length != 0)
		{
		  $('#barcode_wash').select2('val', []);
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
		console.log("asssssssssssssssss")
		     $('#barcode_wash').empty();
		}
		  
        });

},**/

TypeOrderOnChangeEvent: function (event)
    {	
        var ordertype = document.getElementById('type-select').value;
            console.log("=====ordertype",ordertype)
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
		
		$("#my-wash-product").select2({});
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

    generate: function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var product_data = [];
	   	var number_of_barcode = $("#number_of_barcode").val();
	   	if (number_of_barcode != ''){	   	
			   	//	 generating barcode
		        self._rpc({
		                model: 'operation.dashboard',
		                method: 'create_barcode',
		                args: [[],number_of_barcode],
		            })
		            .then(function(result) {
		            	if (result.success) {
		            		self.do_warn(_("Success"),_("Successfully Generate the Barcode!"));
		            		// readonly number_of_barcode      
		            		var barcode_list =''
		            		for(var line in result.created_barcode_data){
						    	   barcode_list += '<span> ('+result.created_barcode_data[line]['count']+')</span>  <span>'+result.created_barcode_data[line]['barcode'] +'</span><br/> '
					    	}
		            		$("#display_generate_barcode").append(barcode_list);
		            		$('#barcode').JsBarcode('501234567890', {format: "ean13"});
		                    $('#barcode').css({
		                    	"width": "1000px",
						        "height":"50px",
						        "margin-top":"20px"
		                    });
		            		$("#display_generate_barcode").addClass("scrolllist");
		            		var number_of_barcode_html = $('#number_of_barcode').html()
		            		var number_of_barcode_span = $("<span id='set_number_of_barcode' ids='"+result.created_barcode_ids+"'>" +number_of_barcode + "</span>");
		            		$('#number_of_barcode').replaceWith(number_of_barcode_span);
		            		// display print button
		            		$("#print_generate_barcode_button").css("display", "inline");
		            		// hide generate button
		            		$("#generate_button").css("display", "none");
		            	}else{
		            		self.do_warn(_("Warning"),result.warning);
		            	}
		            });
	    }else{
	    	   self.do_warn(_("Warning"),_("Please Enter the Number First!"));
	       }
	  },
	  print_generate_barcode: function(event){
		   	var self = this;
		   	event.stopPropagation();
		   	event.preventDefault();
//		   	var barcode_data = []
		   	var barcode_ids = $("#set_number_of_barcode").attr("ids");
		   	var barcode_data = barcode_ids.split(",");
	   	   // append barcode to print report
   	    	if (barcode_ids != undefined ){
   	    		barcode_data.push(parseInt(barcode_ids));
               //printing barcode
   	    		self._rpc({
	                model: 'operation.dashboard',
	                method: 'print_generate_barcode',
	                args: [[],barcode_data],
			
	            })
	            .then(function(result) {
	            	if (result.warning) {
	            		self.do_warn(_("Warning"),result.warning);
	            	}else{
	            		if (session.receipt_to_printer){
	            			//printer barcode
	            			var receipt = QWeb.render('Barcodeticketreceipt',{'data': result.data});
	            			var barcode = $('#barcode').parent().html();
	            			receipt = receipt.split('<img id="barcode"/>');
			                receipt[0] = receipt[0] + barcode + '</img>';
			                receipt = receipt.join('');
	            			return session.proxy_device.print_receipt(receipt);
//	            			var report = self.$el.html(QWeb.render("Barcodeticketreceipt", {'data': result.data}));
//	            			return self.$el.html(receipt);;
	        	        }else{
	        	        	//print pdf barcode
	        	        	var action = {
			                        type: 'ir.actions.report',
			                        report_type: 'qweb-pdf',
			                        report_name: "ballester_screen.report_barcode",
			                        report_file: "ballester_screen.report_barcode",
			                        data: result.data,
			                    };
				            return self.do_action(action);
	        	        }
	            	}
	            });
   	    	}
	 },
	 print_multi_barcode: function(event){
		   	var self = this;
		   	event.stopPropagation();
		   	event.preventDefault();
		   	var barcode_data = []
			var used_barcode_data = []
		    $("#my-select :selected").each(function(){
		        barcode_data.push(parseInt($(this).attr("ids")));
		    });
		    $("#my-used-select :selected").each(function(){
		        used_barcode_data.push(parseInt($(this).attr("ids")));
		    });
	   	   // append barcode to print report
	    	if (barcode_data.length > 0  ){
            //printing barcode
	    		self._rpc({
	                model: 'operation.dashboard',
	                method: 'print_generate_barcode',
	                args: [[],barcode_data],
	            })
	            .then(function(result) {
	            	if (result.warning) {
	            		self.do_warn(_("Warning"),result.warning);
	            	}else{
	            		if (session.receipt_to_printer){
	            			//printer barcode
	            			var receipt = QWeb.render('Barcodeticketreceipt',{'data': result.data});
	            			return session.proxy_device.print_receipt(receipt);
//	            			var report = self.$el.html(QWeb.render("Barcodeticketreceipt", {'data': result.data}));
//	            			return self.$el.html(receipt);;
	        	        }else{
	        	        	//print pdf barcode
	        	        	var action = {
			                        type: 'ir.actions.report',
			                        report_type: 'qweb-pdf',
			                        report_name: "ballester_screen.report_barcode",
			                        report_file: "ballester_screen.report_barcode",
			                        data: result.data,
			                    };
				            return self.do_action(action);
	        	        }
	            	}
	            });
	    	}else{
	    		self.do_warn(_("Warning"),_("Please Select Barcode !"));
	    	}
		if (used_barcode_data.length > 0  ){
            //printing barcode
	    		self._rpc({
	                model: 'operation.dashboard',
	                method: 'print_generate_barcode',
	                args: [[],used_barcode_data],
	            })
	            .then(function(result) {
	            	if (result.warning) {
	            		self.do_warn(_("Warning"),result.warning);
	            	}else{
	            		if (session.receipt_to_printer){
	            			//printer barcode
	            			var receipt = QWeb.render('Barcodeticketreceipt',{'data': result.data});
	            			return session.proxy_device.print_receipt(receipt);
//	            			var report = self.$el.html(QWeb.render("Barcodeticketreceipt", {'data': result.data}));
//	            			return self.$el.html(receipt);;
	        	        }else{
	        	        	//print pdf barcode
	        	        	var action = {
			                        type: 'ir.actions.report',
			                        report_type: 'qweb-pdf',
			                        report_name: "ballester_screen.report_barcode",
			                        report_file: "ballester_screen.report_barcode",
			                        data: result.data,
			                    };
				            return self.do_action(action);
	        	        }
	            	}
	            });
	    	}else{
	    		self.do_warn(_("Warning"),_("Please Select Barcode !"));
	    	}
	 },

add_an_item: function(event){
	       var self = this; 
	       event.stopPropagation();
	       event.preventDefault();
		
	       var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
              console.log(">>>>>>>>>>>>>>@@>>>>>>.",location)
	       if (location != undefined){
		       var table_row = document.getElementById("inventory_adjustments_table").rows;
		       if (table_row.length > 2){
		    	   $( "#inventory_adjustments_table tr:nth-last-child(2)").after("<tr class='active'>"+
		    			   "<td style='width: 25%;' >"+self.product_list+"</td>"+
		    			   "<td style='width: 15%; '> <input type='text' name='ler_code_txt' id='ler_code_id' readonly='readonly' /></td>"+
		    			   "<td style='width: 20%;' id='barcode'>"+self.barcode_list+"</td>"+
		    			   "<td style='width: 20%; '> <input type='text' name='life_date' class='life_datetimepicker' /></td>"+
		    			   "<td style='width: 5%;'> <input type='hidden' name='line_id'  value='none' /> </td>"+
		    			   "<td style='width: 5%;'><button class='fa fa-trash-o btndelete' name='delete' aria-hidden='true'/></td>"+
		    			   "<td style='width: 5%; display:none;'></td>"+
		    			   "<td style='width: 5%;' class='set_lot_details_ids'><button id='lot_details_id' class='fa fa-bars lot_details_wizard'  aria-hidden='true'></button></td>"+
		    			   "</tr>");
		       }else{
		    	   $('#inventory_adjustments_table').prepend("<tr class='active'>"+
		    			   "<td style='width: 25%;'>"+self.product_list+"</td>" +
		    			   "<td style='width: 15%; '> <input type='text' name='ler_code_txt' id='ler_code_id'  readonly='readonly'/></td>"+
		    			   "<td style='width: 20%;' id='barcode'>"+self.barcode_list+"</td>"+
		    			   "<td style='width: 20%; '> <input type='text' name='life_date' class='life_datetimepicker' /></td>"+
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
                           console.log("&**************ler_code*****",ler_code )
		           var product_id = li.text();
                           console.log("*66666666product_id66666",product_id)
		           var row_ids = $('.products').closest('tr')
		           row_ids.each(function(i){
		           var current_product_id = $(this).find('.products').val();
				console.log("=current_product_id=============",current_product_id )
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

		 if (location == undefined){	  
		   		if ($("#set_loction_id").length > 0){
		   			location = $("#set_loction_id").text()
		   		}
		   	}
    },



    save_inventory_adjustments: function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_data = [];
		var record_data= [];
	   	var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
	   	var location_val = $(".locations").val() 
                console.log("^^^^^^^^^^^^^^^session.employee_id^^^^^^^", session.employee_id)
	   	if (location == undefined){	  
	   		if ($("#set_loction_id").length > 0){
	   			location = $("#set_loction_id").text()
	   			location_val = $("#set_loction_id").text()
	   		}
	   	}
	   	if (location != undefined){	   	
			    //	 append product to create barcode
	   		var allow_save = true;
	   		$('#inventory_adjustments_table tr.active').each(function(){
		  		var product = $(this).find('td .products')
		  		var barcode = $(this).find('td .barcodes')
		  		var life_date = $(this).find('td .life_datetimepicker')
		  		if (product.val() == ''){
		  			product.css('border-bottom-color','red');
		  			allow_save = false
		  		}else{
		  			product.css('border-bottom-color','#ccc');
		  		}
		  		if(barcode.val() == ''){
		  			barcode.css('border-bottom-color','red');
		  			allow_save = false
		  		}else{
		  			barcode.css('border-bottom-color','#ccc');
		  		}
		  		if(life_date.val()  == ''){
		  			life_date.css('border-bottom-color','red');
		  			allow_save = false
		  		}else{
		  			life_date.css('border-bottom-color','#ccc');
		  		}
	   		})
	   		if (allow_save == true){
	   		    var count_lines = 0
			  	$('#inventory_adjustments_table tr.active').each(function(){
			  		count_lines += 1;
			  			var product_ids = $(".es-list li[value='" + $(this).find('td .products').val() + "']").attr('ids');
				  		var barcode_ids = $(".es-list li[value='" + $(this).find('td .barcodes').val() + "']").attr('value');
				  		var life_date = $(this).find('td .life_datetimepicker').val();
				  		var line_ids = $(this).find('td #created_line_id');
			   	    	if (line_ids.length > 0){
			   	    		if (life_date != undefined  && product_ids != undefined && barcode_ids != undefined){
			   	    			record_data.push({
				   	    		    'product': product_ids,
				   	    		    'barcode': barcode_ids,
				   	    		    'line_id' : line_ids.attr('line_id'),
				   	    		    'life_date' : life_date
				   	    		});
				   	    	}
			   	    	}else{
			   	    		if (life_date != undefined  &&  product_ids != undefined && barcode_ids != undefined){
				   	    		record_data.push({
				   	    		    'product': product_ids,
				   	    		    'barcode': barcode_ids,
				   	    		    'life_date' : life_date
				   	    		});
				   	    	}
			   	    	}
			   	})
			   if  (count_lines == record_data.length) {
				   var created_inventory_id =document.getElementById("created_inventory_id").value 	//	 createing barcode
				   self._rpc({
			                model: 'operation.dashboard',
			                method: 'save_inventory_adjustments',
			                args: [[],record_data,location,created_inventory_id,self.employee_id],
			            })
			            .then(function(result) {
			            	if (result.success) {
			            		// readonly location           		
			            		/**var location_html = $('#location_data').html();
			            		var location_span = $("<div class='col-md-5' id='location_data'><h2 id='set_loction_id' ids='" + location +"'>" + location_val + "</h2></div>");
			            		$('#location_data').replaceWith(location_span);**/
			            		// readonly additem tr  , added delete and print button
			            		$('#inventory_adjustments_table tr.active').each(function(i){
			            			 var html = $(this).html();
			        				 var span = $("<tr class='active'>"+
			        						"<td style='width: 25%;'  class='set_product_ids'><span id='product_value'>"+ result.inventory_adjustment_table[i]['name'] +"</span></td>"+
			        						"<td style='width: 15%;'  class='set_ler_code_ids'><span id='ler_code_value'>"+  result.inventory_adjustment_table[i]['ler_code']+"</span></td>"+
			        						"<td style='width: 20%;' lines='"+ result.inventory_adjustment_table[i]['id'] +"' class='set_barcode_ids' >"+ result.inventory_adjustment_table[i]['prod_lot_id'] +"</td>" +
			        						"<td style='width: 20%;' life_date='"+result.inventory_adjustment_table[i]['life_date'] +"' class='set_life_date' >"+ result.inventory_adjustment_table[i]['life_date'] +"</td>"+
			        						"<td style='width: 5%;'class='set_line_ids'><input type='hidden' name='line_id' value='"+ result.inventory_adjustment_table[i]['id']+ "'id='created_line_id' line_id='"+ result.inventory_adjustment_table[i]['id'] +"' /> </td>"+
			        						"<td style='width: 5%;' class='set_delete_ids' ><button class='fa fa-trash-o btndelete' inventory='"+ result.inventory_adjustment_table[i]['id'] +"' name='delete' aria-hidden='true'/></td>" +
			        				 		"<td style='width: 5%;' class='set_print_ids' ><button id='print_barcode_id' class='btn btn-xs btn-default pull-right print_barcode' line_id='"+ result.inventory_adjustment_table[i]['id'] +"' barcode_id='" + result.inventory_adjustment_table[i]['prod_lot_id'] +"'>Print</button></td>"+
			        				        
			            		            "</tr>"


				);
			                         $(this).replaceWith(span);
							   	})
							   	document.getElementById("created_inventory_id").value = result.id;
							   	// hide generate barcode button
			            		 $("#save_inventory_adjustments_button").css("display", "none");
			            		// display validate barcode button
			            		 $("#validate_barcode_button").css("display", "inline");
			            		// display edit barcode button
			            		 $("#edit_inventory_adjustments_button").css("display", "inline");
			            		// remove add an item
			            		$('#inventory_adjustments_table #add_an_item').remove();
						$('#categ_select_id').attr("disabled", true)
						$('.locations').attr("disabled", true)
			            		self.do_warn(_("Success"),result.success);
						
			            		
			            	}else{
			            		self.do_warn(_("Warning"),result.warning);
			            	}
		             });
			   }
	   		}else{
	   		 self.do_warn(_("Warning"),_("Please fill in all the required fields !"));
	   		}
	   		  
	    }else{
	    	   self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
	       }
	  },



	  edit_inventory_adjustments: function(event){
		   	var self = this;
		   	event.stopPropagation();
		   	event.preventDefault();
		   	var barcode_data = []
                    //edit inventory adjustments
		   	$('#inventory_adjustments_table tr.active').each(function(i){
     			var product = $(this).find('td.set_product_ids');
     			var ler = $(this).find('td.set_ler_code_ids');
			   	var barcode = $(this).find('td.set_barcode_ids');
			   	var delete_line = $(this).find('td.set_delete_ids');
			   	var print_line = $(this).find('td.set_print_ids');
			   	var lot_details_ids = $(this).find('td.set_lot_details_ids');
			   	var line_ids = $(this).find('td.set_line_ids');
				$('#categ_select_id').attr("disabled", false)
				$('.locations').attr("disabled", false)
			   	var life_date = $(this).find('td.set_life_date');
		  		/**if (self.operation_data.set_product_list.length > 0){
		  			var product_list = '<select class="products" style="overflow-y: auto!important; font-size: 18px;">'
			    	   for(var line in self.operation_data.set_product_list){
				    	 if (self.operation_data.set_product_list[line]['name'] == product.text()){
				    		 product_list += '<option selected="true" label="'+self.operation_data.set_product_list[line]['default_code'] + '" ids="' +self.operation_data.set_product_list[line]['id']+'"'+ ' value="'+self.operation_data.set_product_list[line]['name']+'" product_ler_code="'+ler.text()+'">' +self.operation_data.set_product_list[line]['name']+'</option>'  
				    	  }else{
				    		 product_list += '<option label="'+self.operation_data.set_product_list[line]['default_code'] + '" ids="' +self.operation_data.set_product_list[line]['id']+'"'+ ' value="'+self.operation_data.set_product_list[line]['name']+'" product_ler_code="'+self.operation_data.set_product_list[line]['ler_code']+'">' +self.operation_data.set_product_list[line]['name']+'</option>'
				    	  }
			    	   }
			    		   product_list += '</select>'
			        }else{
			    	   product_list = '<select class="products" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found !</option> </select>'
			       }**/
	
				if (self.cat_product_list.length > 0){
		  	           var product_list = '<select class="products" style="overflow-y: auto!important; font-size: 18px;">'
			    	   for(var line in self.cat_product_list){
					var product_name = product.text()
				
					 var correct_product_name = ''
					if (product_name.includes("''")){
						correct_product_name = product_name.replace("''", "*");
					}
					else{
					correct_product_name = product_name.replace('"', "*");
					
				       }

				    	 if (self.cat_product_list[line]['name'] == correct_product_name){
                                                console.log("JJJJJJJJJJJJJJJJJJJJJJJJ")
				          product_list += '<option selected="true" label="'+self.cat_product_list[line]['default_code'] + '" ids="' +self.cat_product_list[line]['id']+'"'+ ' value="'+self.cat_product_list[line]['name']+'" product_ler_code="'+ler.text()+'">' +self.cat_product_list[line]['name']+'</option>'  
				    	  }else{
				    		 product_list += '<option label="'+self.cat_product_list[line]['default_code'] + '" ids="' +self.cat_product_list[line]['id']+'"'+ ' value="'+self.cat_product_list[line]['name']+'" product_ler_code="'+self.cat_product_list[line]['ler_code']+'">' +self.cat_product_list[line]['name']+'</option>'
				    	  }
					 
			    	   }
			    		product_list += '</select>'  
			        }else{
			    	   product_list = '<select class="products" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found !</option> </select>'
			       }


			       if (self.operation_data.set_barcode_list.length > 0){
			    	   var barcode_list = '<select class="barcodes" style="overflow-y: auto!important; font-size: 18px;">'
			    	   for(var line in self.operation_data.set_barcode_list){
			    		   if (self.operation_data.set_barcode_list[line]['barcode'] == barcode.text()){
			    			  barcode_list += '<option  selected="selected"  ids="' +self.operation_data.set_barcode_list[line]['id']+'"'+ ' value="'+self.operation_data.set_barcode_list[line]['barcode']+'">' +self.operation_data.set_barcode_list[line]['barcode']+'</option>'
			    		  }else{
			    			 barcode_list += '<option ids="' +self.operation_data.set_barcode_list[line]['id']+'"'+ ' value="'+self.operation_data.set_barcode_list[line]['barcode']+'">' +self.operation_data.set_barcode_list[line]['barcode']+'</option>'
			    		  }
			    	    }
			    	   barcode_list += '</select>'
			        }else{
			        	barcode_list = '<select class="barcodes" style="overflow-y: auto!important; font-size: 18px;"><option> No Data Found ! </option> </select>'
			        } 
	              var data = "<tr class='active'>"+
	                         "<td style='width: 25%;' class='set_product_ids'>"+product_list+"</td>"+
	                         "<td style='width: 15%; position:absolute;' > <input type='text' name='ler_code_txt' id='ler_code_id'  readonly='readonly' value='"+ler.text() +"'/></td>"+
	                         "<td style='width: 20%;' class='set_barcode_ids'>"+barcode_list+"</td>"+
	                         "<td style='width: 20%; position:absolute;'> <input type='text' name='life_date' class='life_datetimepicker' value='"+life_date.text() +"'/></td>"+
	                         "<td style='width: 5%;'  class='set_line_ids'>"+ line_ids.html()+"</td>"+
	                         "<td style='width: 5%;'  class='set_delete_ids'>"+delete_line.html()+"</td>"+
	                         "<td style='width: 5%; display:none;' class='set_print_ids'>"+print_line.html() +"</td>"+
	                         "<td style='width: 5%;' class='set_lot_details_ids'>"+lot_details_ids.html()+"</td>"+
	                         "</tr>"
	              $(this).replaceWith(data);
		   	})
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
	        $("#inventory_adjustments_table tbody").append("<tr id='add_an_item'>" +
                    "<td colspan='4' class='o_field_x2many_list_row_add add_an_item'>" +
                    "<a href='#'>Add an item</a>" +
                    "</td></tr>")
            // hide validate button 
            $("#validate_barcode_button").css("display", "none");
	        // hide edit button
	        $("#edit_inventory_adjustments_button").css("display", "none");
	        // visible save button
	        $("#save_inventory_adjustments_button").css("display", "inline");
 	  },
    /**inventory_adjustments: function(event){
   	 var self = this;
        event.stopPropagation();
        event.preventDefault();
        self._rpc({
            model: 'operation.dashboard',
            method: 'get_operation_info',
        }, []).then(function(result){
            self.operation_data = result[0]
           
           self.product_list = self.operation_data.product_list
//           self.ler_list = self.operation_data.ler_list
           self.barcode_list = self.operation_data.barcode_list
           self.employee_id = session.employee_id
           self.employee = session.employee 
           self.employee_image_url = session.employee_image_url
        }).done(function(){
        	self.href = window.location.href;
        	return  self.$el.html(QWeb.render("InventoryAdjustmentsButton", {widget: self}));
        });
        
    },**/

    inventory_adjustments: function(event){
   	 var self = this;
        event.stopPropagation();
        event.preventDefault();
        self._rpc({
            model: 'operation.dashboard',
            method: 'get_inventory_adjustment_info',
        }, []).then(function(result){
            //self.operation_data = result[0]
           self.employee_id = session.employee_id
           self.location_list = result['data']['location_list']
           self.category_list = result['data']['category_list']
           self.employee = session.employee 
           self.employee_image_url = session.employee_image_url
        }).done(function(){
        	self.href = window.location.href;
        	return  self.$el.html(QWeb.render("InventoryAdjustmentsButton", {widget: self}));
        });
        
    },


    internal_transfers: function(event){
   	 var self = this;
        event.stopPropagation();
        event.preventDefault();
        self._rpc({
            model: 'operation.dashboard',
            method: 'get_internal_transfer_info',
        }, []).then(function(result){
          self.product_list = ''
//           self.ler_list = self.operation_data.ler_list
           self.barcode_list = result['data']['barcode_list']
           self.employee_id = session.employee_id
           self.location_list = result['data']['location_list']
           self.employee = session.employee 
	   self.washing_type = result['data']['washing_type']
           self.type_of_order = result['data']['type_of_order']
           self.employee_image_url = session.employee_image_url

        }).done(function(){
        	self.href = window.location.href;
        	return  self.$el.html(QWeb.render("InternaltransferButton", {widget: self}));
        });
        
    },




    product_wash: function(event){
   	$(".product_wash").chosen();
    },


// create wash order

	create_wash_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];
	   	var location = $("#my-select").val() ;
                var product_id =document.getElementById('my-wash-product').value;
               // var recycled_product_id = document.getElementById('my-recycled-product').value;
		var recycled_product_id= $("#my-recycled-product").select2('data')['text'] ;
                var dest_location_id =  $("#my-dest-select").val() ;
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
		var type_of_order = document.getElementById("type-select").value;
		var washing_type = $("#washing_type").val() ;
		$("#barcode_wash :selected").each(function(){
			
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
	   	var report_data = [];
	   	if (location != undefined &&  dest_location_id != undefined  &&  type_of_order != undefined){	   	
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': type_of_order,
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
				'washing_type' :washing_type,
 				});
			self._rpc({
			        model: 'operation.dashboard',
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




// create inernal transfer order

	create_internal_transfer_button : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];
	   	var location = $("#my-select").val() ;
                var product_id =document.getElementById('my-wash-product').value;
               // var recycled_product_id = document.getElementById('my-recycled-product').value;
		var recycled_product_id= $("#my-recycled-product").select2('data')['text'] ;
                var dest_location_id =  $("#my-dest-select").val() ;
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
		var type_of_order = document.getElementById("type-select").value;
		var washing_type = $("#washing_type").val() ;
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
	   	var report_data = [];
	   	if (location != undefined &&   dest_location_id != undefined  &&  type_of_order != undefined){	
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'recycled_product_id': recycled_product_id,
				'type_of_order': type_of_order,
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
				'washing_type' :washing_type,
 				});
			self._rpc({
			        model: 'operation.dashboard',
			        method: 'create_internal_transfer_method',
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




create_destruction_order_confirm: function(event){
   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];
	   	var location = $("#my-select").val() ;
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $("#my-dest-select").val() ;
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
		var type_of_order = document.getElementById("type-select").value;
		var washing_type = $("#washing_type").val() ;
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
			console.log(">>>>aseff>>>>>",location,product_id )
		        console.log(">>>>>report_data>>>>>",report_data)
			self._rpc({
			        model: 'operation.dashboard',
			        method: 'create_destruction_method',
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

	main_button : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		
	    return self.$el.html(QWeb.render("WarehouseButton", {widget: self}));
},


// save wash order

       save_wash_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	//var location = $(".es-list li[value='" + document.getElementById("my-select").val() + "']").attr('ids');
                var location = $("#my-select").val() ;
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =  $("#my-dest-select").val() ;
                var barcode_ids =  $("#barcode_wash").attr("ids"); 
		var type_of_order = document.getElementById("type-select").value;
		var washing_type = $("#washing_type").val() ;
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
				'barcode_ids' :barcode_list,
				'washing_type':washing_type,

 				});
			self._rpc({
			        model: 'operation.dashboard',
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
				$("#create_internal_transfer_button").css("display", "inline");
				$("#save_wash_order_button").css("display", "none");
				$("#type-select").attr("disabled", true);
				$("#my-dest-select").attr("disabled", true);
				$("#my-select").attr("disabled", true);
				$("#my-wash-product").attr("disabled", true);
				$("#my-recycled-product").attr("disabled", true);
				$("#barcode_wash").attr("disabled", true);
				$("#washing_type").attr("disabled", true);
				$("#destruction_wash_order").attr("display", "inline");
	            		// hide delete button
	            	}else{
	            		self.do_warn(_("Warning"),_("Can not save!!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Can not save!!"));
  }
},

// edit wash order

       edit_wash_order : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var location = document.getElementById("my-select").value;
                var product_id =document.getElementById('my-wash-product').value;
                var recycled_product_id = document.getElementById('my-recycled-product').value;
                var dest_location_id =   document.getElementById("my-dest-select").value;
                var barcode_ids =  $("#barcode_wash").attr("ids"); ;
		var type_of_order = $("#type-select").val() ;
		var washing_type = $("#washing_type").val() ;
	   	var report_data = [];
		var barcode_list = [];
		var allow_save = true
		$("#barcode_wash :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		self._rpc({
		        model: 'operation.dashboard',
		        method: 'edit_wash_order_method',
		        args: [[]],
		    })
                    
	            .then(function(result) {

	            	if (result.success) {
	            		// hide validate barcode button
	            		$("#edit_wash_order_button").css("display", "none");
	            		$("#create_destruction_order_button").css("display", "none");
				$("#create_wash_order_button").css("display", "none");
				$("#create_internal_transfer_button").css("display", "none");
				$("#save_wash_order_button").css("display", "inline");
				$("#type-select").attr("disabled", false);
				$("#my-dest-select").attr("disabled", false);
				$("#my-select").attr("disabled", false);
				$("#my-wash-product").attr("disabled", false);
				$("#my-recycled-product").attr("disabled", false);
				$("#barcode_wash").attr("disabled", false);
				$("#washing_type").attr("disabled", false);
				$("#destruction_wash_order").attr("display", "none");
			}
		
	               });
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
			         model: 'operation.dashboard',
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
			   	//var location = $("#set_loction_id").attr('ids');
                                var location = $(".es-list li[value='" + $(".locations").val() + "']").attr('ids');
                                console.log("&&&&&&&&&&&&location&&&",location)
	   	               // var location_val = $(".locations").val() 
			   	var inventory_data = [];
			   	if (location != undefined){	   	
				   	//	 append inventory id to validate barcode
				   	inventory_data.push(document.getElementById("created_inventory_id").value);
				   	//	 validating inventory adjustments
			        self._rpc({
			                model: 'operation.dashboard',
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
	   	print_barcode: function(event){
		   	var self = this;
		   	event.stopPropagation();
		   	event.preventDefault();
		   	var barcode_data = []
	   	   // append barcode to print report
		   	var barcode_ids = event.target.getAttribute("line_id")
	   	    	if (barcode_ids != undefined ){
	   	    		barcode_data.push(parseInt(barcode_ids));
                   //printing barcode
	   	    		self._rpc({
		                model: 'operation.dashboard',
		                method: 'print_barcode',
		                args: [[],barcode_data],
		            })
		            .then(function(result) {
		            	if (result.warning) {
		            		self.do_warn(_("Warning"),result.warning);
		            	}else{
		            		if (session.receipt_to_printer){
		        	        	var report = QWeb.render("Barcodeticketreceipt", {'data': result.data});
//		        	        	self.$el.html(QWeb.render("Barcodeticketreceipt", {'data': result.data}));
		        	        	return session.proxy_device.print_receipt(report);
		        	        }else{
			            		var action = {
			                        type: 'ir.actions.report',
			                        report_type: 'qweb-pdf',
			                        report_name: "ballester_screen.report_barcode",
			                        report_file: "ballester_screen.report_barcode",
			                        data: result.data,
			                    };
				                return self.do_action(action);
		        	        }
		            	}
		            });
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
		                model: 'operation.dashboard',
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
core.action_registry.add('ballester_screen_act', BallesterScreen);

return BallesterScreen;

});
