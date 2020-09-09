/** -*- coding: utf-8 -*-
 Odoo, Open Source Ballester Screen.
 License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
*/
odoo.define('canet_screen.screen', function (require) {
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


var CanetScreen = Widget.extend({
	events: _.extend({}, Widget.prototype.events, {
		'click .main': 'main',
		'click .my_profile': 'action_my_profile',
		// ===========  exit Popup ===========
		'click .confirm_exit_popup': 'confirm_exit_popup',
		// ===========  main 1 button ===========
		'click .warehouse': 'warehouse',
		'click .inventory_adjustments': 'inventory_adjustments',
		'click .internal_transfers': 'internal_transfers',
		'click .equipment_delivery': 'equipment_delivery',
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
		'click .print_generate_barcode': 'print_generate_barcode',
		'click .print_multi_barcode': 'print_multi_barcode',
		'click .transfer_to_task': 'transfer_to_task',
		'click .transfer_to_task_delivery': 'transfer_to_task_delivery_button',
		'click .edit_delivery_return_button': 'edit_delivery_return_button',
		'click .save_internal_transfer' : 'save_internal_transfer',
		'click .return_to_task_button' : 'return_to_task_button',
		//save_delivery_return_button
		'click .save_delivery_return_button' :'save_delivery_return_button',
		'click .edit_delivery_return_button' :'edit_delivery_return_button',
		'click .onchange_product' :'onchange_product',
		'click .main_button': 'main_button',

		'change #type-select' : 'TypeOrderOnChangeEvent',
		'change #categ_select_id' : 'CategoryOnChangeEvent',
		//'change #my-wash-product' : 'ProductOnChangeEvent',
		'change #barcode_product' : 'LotOnChangeEvent',
		'change #barcode_equ' : 'LotequOnChangeEvent',
		'change #my-select' : 'LocationOnChangeEvent',
	}),
	init: function(parent, context) {
        this._super(parent, context);
        var operation_data = [];
        var self = this;
        var user = session.uid
        if (context.tag == 'canet_screen_act') {

            self._rpc({
                model: 'operation.dashboard',
                method: 'get_operation_info',
            }, []).then(function(result){
            	self.operation_data = result[0]
                self.product_list = self.operation_data.product_list
                self.barcode_list = self.operation_data.barcode_list
                self.set_unused_barcode_list = self.operation_data.set_unused_barcode_list
                self.unused_barcode_list = self.operation_data.unused_barcode_list
		        self.recycled_product = self.operation_data.recycled_product
		        self.user_name =  self.operation_data.user_name
		        self.user_image_url = self.operation_data.user_image_url

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
        return  self.do_action('canet_screen.action_canet_screen');
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
		$('#barcode_product').empty();
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

                    $( '#barcode_product' ).append( optionsAsString );
                    }

                else {
                     $('#barcode_product').empty();
                }

        }
            if (result.product_list){
            var product = result.product_list
                if(product.length != 0)
                {
                  $('#my-canet-product').select2('val', []);
                   var product_list = result.product_list
                   var optionsProduct = "";
                       for(var i = 0; i < Object.keys(product_list).length  ; i++)
                    {

                         var product_detail = product_list[i]
                                    optionsProduct += "<option value='" + product_detail['name'] + "'" + "ids='"+ product_detail['id'] +"'>" + product_detail['name'] + "</option>";

			            }

                    $( '#my-canet-product' ).append( optionsProduct );
                    }

                else {
                     $('#my-canet-product').empty();
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
        console.log("+++++++++++++++++++++++++++++++")
//        var selectedlotValue = document.getElementById('barcode_product').value;
           var selectedlotValue = $("#barcode_product").val();


        var domain_dp = []
	    if (selectedlotValue != undefined){
            domain_dp.push(['name', 'in', selectedlotValue])
		}
        this._rpc({
            model: 'operation.dashboard',
            method: 'lot_data',
            args: [domain_dp],
        })
        .then(function (result) {
               if (result != undefined){
               if(result.product_name != ''){

//                    var productvalue = document.getElementById('my-canet-product').value;


//                        if (productvalue   )
//
//                        {
//                            console.log("*********result.product_name********",result.product_name )
//                            productvalue.push(result.product_name);
//                        }


                          console.log("*********elseeeee****",result.product_name )
                          $('#my-canet-product').select2('val',  result.product_name);

                    }
                else {
                  console.log("_____________")
                        $('#my-canet-product').select2('val', []);

                }

		  }
        });

},

LotequOnChangeEvent: function (event)

    {
//        var selectedlotValue = document.getElementById('barcode_equ').value;
        var selectedlotValue = $("#barcode_equ").val();
        var domain_dp = []
        var ctx = {}
        ctx ['equipment_lot'] = true
	    if (selectedlotValue != undefined){
            domain_dp.push(['barcode', 'in', selectedlotValue])
		}

        this._rpc({
            model: 'operation.dashboard',
            method: 'lot_equ_data',
            args: [domain_dp],ctx
        })
        .then(function (result) {
               if (result != undefined){
               if(result.product_name != ''){
                    console.log("________result.product_name _______", result.product_name )
//                    var productvalue = document.getElementById('my-canet-product').value;
//
//
//                        if (productvalue   )
//
//                        {
//
//                            productvalue.push(result.product_name);
//                        }



                          $('#my-canet-equ').select2('val',  result.product_name);

                    }
                else {
                        $('#my-canet-equ').select2('val', []);

                }

                if(result.maintenance_team != 'False'){

                     document.getElementById('team_list').value =  result.maintenance_team;

                }
                if(result.operation_type != 'False'){

                     document.getElementById('operation_type').value =  result.operation_type;
                      if(result.operation_type == 'Return'){
                             $("#return_to_task_button").css("display", "inline");
                             $("#transfer_to_task_button").css("display", "none");
                      }
                }
                if(result.technician != 'False'){
                     document.getElementById('technician_list').value =  result.technician;

                }
                if(result.task_number != ''){
                    document.getElementById('type-select').value =  'Proyecto';
                    document.getElementById('task_number').value =  result.task_number;
                    $("#task_div").css('display','inline');
                    $("#task_value_div").css('display','inline');
                    $("#maintenance_div").css('display','none');
                    $("#maintenance_value_div").css('display','none');


                }
                if(result.maintenance_number != ''){
                    document.getElementById('type-select').value =  'Mantenimiento';
                    document.getElementById('maintenance_number').value =  result.maintenance_number;
                    $("#task_div").css('display','none');
                    $("#task_value_div").css('display','none');
                    $("#maintenance_div").css('display','inline');
                    $("#maintenance_value_div").css('display','inline');

                }
                if(result.qty != ''){

                     document.getElementById('quantity').value =  result.qty;


                }


		  }
        });

},


TypeOrderOnChangeEvent: function (event)
    {
        var ordertype = document.getElementById('type-select').value;
            console.log("=====ordertype",ordertype)
	    var ctx = {}
        var product_list = []

	if (ordertype == ''){

		self.do_warn(_("Warning"),_("Please Enter the Order Type First!"));

	}
	console.log("________888",ordertype)
	if (ordertype == 'Transferencia interna'){
		ctx['type_of_order']='internal_transfer'
		 $("#task_div").css('display','none');

        $("#task_value_div").css('display','none');
        $("#maintenance_div").css('display','none');
        $("#maintenance_value_div").css('display','none');
	}
	if (ordertype == 'Proyecto'){
		ctx['type_of_order']='project'

		$("#transfer_to_task_button").html('Transfer To Task');
		 $("#task_div").css('display','inline');
        $("#task_value_div").css('display','inline');
         $("#maintenance_div").css('display','none');
        $("#maintenance_value_div").css('display','none');
	}
//	if (ordertype == 'Assign to Employee'){
//		ctx['type_of_order']='assign_employee'
//
//
//		 $("#task_div").css('display','none');
//        $("#task_value_div").css('display','none');
//         $("#maintenance_div").css('display','none');
//        $("#maintenance_value_div").css('display','none');
//	}
	if (ordertype == 'Mantenimiento'){
		ctx['type_of_order']='maintenance'

		 $("#task_div").css('display','none');

		  $("#transfer_to_task_button").html('Transfer To Maintenance');
        $("#task_value_div").css('display','none');
         $("#maintenance_div").css('display','inline');
        $("#maintenance_value_div").css('display','inline');
	}


        $("#my-canet-product").select2({});

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
			                        report_name: "canet_screen.report_barcode",
			                        report_file: "canet_screen.report_barcode",
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
			                        report_name: "canet_screen.report_barcode",
			                        report_file: "canet_screen.report_barcode",
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
			                        report_name: "canet_screen.report_barcode",
			                        report_file: "canet_screen.report_barcode",
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
		    			   "<td style='width: 27%;' >"+self.product_list+"</td>"+
		    			   "<td style='width: 17%; '> <input type='text' name='product_unit' id='product_unit' style='height:40px'/></td>"+
		    			   "<td style='width: 22%;' >"+self.barcode_list+"</td>"+
		    			   "<td style='width: 22%; '> <input type='text' name='life_date' class='life_datetimepicker' /></td>"+
		    			   "<td style='width: 7%;'> <input type='hidden' name='line_id'  value='none' /> </td>"+
		    			   "<td style='width: 5%;'><button class='fa fa-trash-o btndelete' name='delete' aria-hidden='true'/></td>"+
//		    			   "<td style='width: 5%; display:none;'></td>"+
//		    			   "<td style='width: 5%;' class='set_lot_details_ids'><button id='lot_details_id' class='fa fa-bars lot_details_wizard'  aria-hidden='true'></button></td>"+
		    			   "</tr>");
		       }else{
		           console.log("===-0-00-0-000inventory_adjustments_table00000000000")
		    	   $('#inventory_adjustments_table').prepend("<tr class='active'>"+
		    			   "<td style='width: 27%;'>"+self.product_list+"</td>" +
		    			   "<td style='width: 17%; '> <input type='text' name='product_unit' id='product_unit' style='height:40px'/></td>"+
		    			   "<td style='width: 22%;' >"+self.barcode_list+"</td>"+
		    			   "<td style='width: 22%; '> <input type='text' name='life_date' class='life_datetimepicker' /></td>"+
		    			   "<td style='width: 7%;'> <input type='hidden' name='line_id' value='none' /></td>"+
		    			   "<td style='width: 5%;'><button class='fa fa-trash-o btndelete' name='delete' aria-hidden='true'/></td>"+
//		    			   "<td style='width: 5%; display:none;'></td>"+
//		    			   "<td style='width: 5%;' class='set_lot_details_ids'><button id='lot_details_id' class='fa fa-bars lot_details_wizard'  aria-hidden='true'></button></td>"+
		    			   "</tr>");
		       }
		       $(".barcodes").editableSelect();
		       $('.products').editableSelect();
//		       .on('select.editable-select', function (e, li) {
//		           var ler_code = li.attr('product_ler_code');
//                           console.log("&**************ler_code*****",ler_code )
//		           var product_id = li.text();
//                           console.log("*66666666product_id66666",product_id)
//		           var row_ids = $('.products').closest('tr')
//		           row_ids.each(function(i){
//		           var current_product_id = $(this).find('.products').val();
//				console.log("=current_product_id=============",current_product_id )
//			           if(current_product_id === product_id){
//			        	   $(this).find('td #ler_code_id').val(ler_code)
//			           }
//		           })
//		       });
		        var today = new Date();
		        var deafult_date = new Date(today.getFullYear() + 1,  today.getMonth(),today.getDate(),today.getHours(),today.getMinutes(),today.getSeconds())
		       $('.life_datetimepicker').datetimepicker({format: 'MM/DD/YYYY hh:mm:ss',
		    	   locale:  moment.locale('es'),
		    	   defaultDate: deafult_date,
		    	   icons: {
                    time: "fa fa-clock-o",
                    date: "fa fa-calendar",
                    up: "fa fa-arrow-up",
                    down: "fa fa-arrow-down"
                                },
		    	   widgetPositioning:{ horizontal: 'left',vertical: 'bottom' },
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
		  		var units = $(this).find('td #product_unit')
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
		  		if(units.val()  == ''){
		  			units.css('border-bottom-color','red');
		  			allow_save = false
		  		}else{
		  			units.css('border-bottom-color','#ccc');
		  		}
	   		})
	   		if (allow_save == true){
	   		    var count_lines = 0
			  	$('#inventory_adjustments_table tr.active').each(function(){
			  		count_lines += 1;
			  			var product_ids = $(".es-list li[value='" + $(this).find('td .products').val() + "']").attr('ids');
				  		var barcode_ids = $(".es-list li[value='" + $(this).find('td .barcodes').val() + "']").attr('value');
				  		var units = $(this).find('td #product_unit').val()
				  		var life_date = $(this).find('td .life_datetimepicker').val();
				  		var line_ids = $(this).find('td #created_line_id');
				  		console.log("=============product_ids===============",product_ids, units ,barcode_ids,life_date,line_ids)
			   	    	if (line_ids.length > 0){
			   	    		if (life_date != undefined  && product_ids != undefined && barcode_ids != undefined){
			   	    			record_data.push({
				   	    		    'product': product_ids,
				   	    		    'barcode': barcode_ids,
                                    'units' : units,
				   	    		    'line_id' : line_ids.attr('line_id'),
				   	    		    'life_date' : life_date
				   	    		});
				   	    	}
			   	    	}else{
			   	    		if (life_date != undefined  &&  product_ids != undefined && barcode_ids != undefined){
				   	    		record_data.push({
				   	    		    'product': product_ids,
				   	    		    'barcode': barcode_ids,
				   	    		    'units' : units,
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
			                args: [[],record_data,location,created_inventory_id],
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
			        						"<td style='width: 15%;'  class='set_unit'><span id='unit_value'>"+  result.inventory_adjustment_table[i]['units']+"</span></td>"+
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
		   	    console.log("^^^^^^^^^^^^^^^^^^^^^^")
     			var product = $(this).find('td.set_product_ids');
     			var units =  $(this).find('td.set_unit');
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
				          product_list += '<option selected="true" label="'+self.cat_product_list[line]['default_code'] + '" ids="' +self.cat_product_list[line]['id']+'"'+ ' value="'+self.cat_product_list[line]['name']+'">' +self.cat_product_list[line]['name']+'</option>'
				    	  }else{
				    		 product_list += '<option label="'+self.cat_product_list[line]['default_code'] + '" ids="' +self.cat_product_list[line]['id']+'"'+ ' value="'+self.cat_product_list[line]['name'] +'">' +self.cat_product_list[line]['name']+'</option>'
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
			        console.log("==========units===========",units.text())
	              var data = "<tr class='active'>"+
	                         "<td style='width: 25%;' class='set_product_ids'>"+ product_list+"</td>"+
	                         "<td style='width: 15%; position:absolute;'  class='set_unit'> <input type='text' style='height:40px' name='units' id='product_unit' value='"+units.text() +"'/></td>"+
	                         "<td style='width: 20%;' class='set_barcode_ids'>"+ barcode_list+"</td>"+
	                         "<td style='width: 20%; position:absolute;'> <input type='text' name='life_date' class='life_datetimepicker' value='"+life_date.text() +"'/></td>"+
	                         "<td style='width: 5%;'  class='set_line_ids'>"+ line_ids.html()+"</td>"+
	                         "<td style='width: 5%;'  class='set_delete_ids'>"+delete_line.html()+"</td>"+
	                         "<td style='width: 5%; display:none;' class='set_print_ids'>"+print_line.html() +"</td>"+
	                         "<td style='width: 5%;' class='set_lot_details_ids'>"+lot_details_ids.html()+"</td>"+
	                         "</tr>"
	              $(this).replaceWith(data);
		   	})
		   	$(".barcodes").editableSelect();
		   	$('.products').editableSelect();

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


    inventory_adjustments: function(event){
   	 var self = this;
        event.stopPropagation();
        event.preventDefault();
        self._rpc({
            model: 'operation.dashboard',
            method: 'get_inventory_adjustment_info',
        }, []).then(function(result){
            //self.operation_data = result[0]
           self.barcode_list =  result['data']['barcode_list']
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
           self.barcode_list = result['data']['barcode_list']
           self.location_list = result['data']['location_list']
	       self.task_list = result['data']['task_list']
	       self.maintenance_list = result['data']['maintenance_list']
           self.type_of_order = result['data']['type_of_order']
        }).done(function(){
        	self.href = window.location.href;
        	return  self.$el.html(QWeb.render("InternaltransferButton", {widget: self}));
        });

    },

    equipment_delivery: function(event){
   	 var self = this;
        event.stopPropagation();
        event.preventDefault();
        self._rpc({
            model: 'operation.dashboard',
            method: 'get_equipment_delivery_return_info',
        }, []).then(function(result){
          self.equipment_list =result['data']['equipment_list']
           self.barcode_list = result['data']['barcode_list']
	       self.task_list = result['data']['task_list']
	       self.maintenance_list = result['data']['maintenance_list']
           self.technician_list = result['data']['technician_list']
           self.maintenance_team = result['data']['maintenance_team']
           self.type_of_order = result['data']['type_of_order']
           self.operation_type = result['data']['operation_type']

        }).done(function(){
        	self.href = window.location.href;
        	return  self.$el.html(QWeb.render("EquipmentDeliveryandReturnButton", {widget: self}));
        });

    },


    product_wash: function(event){
   	$(".product_wash").chosen();
    },


// create inernal transfer order

	create_internal_transfer_button : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];
	   	var location = $("#my-select").val() ;
        var product_id =document.getElementById('my-canet-product').value;
        var dest_location_id =  $("#my-dest-select").val() ;
        var barcode_ids =  $("#barcode_product").attr("ids");
		var type_of_order = document.getElementById("type-select").value;
		if (type_of_order != 'Transferencia interna' ){
                self.do_warn(_("Warning"),_("Please select Internal Transfer!"));
		      }
		$("#barcode_product :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
	   	var report_data = [];
	   	if (location != undefined &&  dest_location_id != undefined ){
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'type_of_order': type_of_order,
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
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

transfer_to_task : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	var ctx = {};
		var barcode_list = [];
	   	var location = $("#my-select").val() ;
        var product_id =document.getElementById('my-canet-product').value;
        var dest_location_id =  $("#my-dest-select").val() ;
        var task_number =  $("#task_number").val() ;
        var maintenance_number =  $("#maintenance_number").val() ;
        var barcode_ids =  $("#barcode_product").attr("ids");
		var type_of_order = document.getElementById("type-select").value;
		if (type_of_order == 'Transferencia interna' ){
                self.do_warn(_("Warning"),_("You can not Transfer to Task, Please change the Type!"));
		      }
		$("#barcode_product :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
        ctx['internal'] = true;
	   	var report_data = [];
	   	if (location != undefined &&  dest_location_id != undefined ){
		   	report_data.push({
				'location': location,
				'product_id': product_id,
				'task_number': task_number,
				'maintenance_number':maintenance_number,
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
 				});
			self._rpc({
			        model: 'operation.dashboard',
			        method: 'update_task',
			        args: [[],report_data,ctx ],
			    })
	            .then(function(result) {
	                console.log("________result________",result)
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

transfer_to_task_delivery_button : function(event){
	   	var self = this;
	   	var ctx  = {};
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];

        var task_number =  $("#task_number").val() ;
        var quantity =  $("#quantity").val() ;
        var operation_type =  document.getElementById("operation_type").value;
        var maintenance_number =  $("#maintenance_number").val() ;
        var barcode_ids =  $("#barcode_equ").attr("ids");
		var type_of_order = document.getElementById("type-select").value;
        var responsible = document.getElementById("technician_list").value;
		var team = document.getElementById("team_list").value;
		$("#barcode_equ :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		ctx['delivery'] = true
	   	var report_data = [];
	   	if ( quantity && operation_type && responsible && team){
		   	report_data.push({
				'quantity': quantity,
				'responsible': responsible,
				'operation_type': operation_type,
				'maintenance_number':maintenance_number,
				'task_number':task_number,
				'team': team,
				'barcode_ids' :barcode_list,
 				});
			self._rpc({
			        model: 'operation.dashboard',
			        method: 'update_task',
			        args: [[],report_data ,ctx],
			    })
	            .then(function(result) {
	            	if (result.success) {
	            		return self.$el.html(QWeb.render("Confirm", {widget: self}));
	            	}
	            	else if(result.delivery_warning){

                            self.do_warn(_("Warning"),_("Equipment has already delivered!"));
	            	}
	            	else if(result.return_warning){
                            self.do_warn(_("Warning"),_("Equipment has already returned!"));
	            	}
	            	else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Something Wrong!! Please check selected Data!"));
  }
},

return_to_task_button : function(event){
	   	var self = this;
	   	var ctx  = {};
	   	event.stopPropagation();
	   	event.preventDefault();
		var barcode_list = [];

        var task_number =  $("#task_number").val() ;
        var quantity =  $("#quantity").val() ;
        var operation_type =  document.getElementById("operation_type").value;
        var maintenance_number =  $("#maintenance_number").val() ;
        var barcode_ids =  $("#barcode_equ").attr("ids");
		var type_of_order = document.getElementById("type-select").value;
        var responsible = document.getElementById("technician_list").value;
		var team = document.getElementById("team_list").value;
		$("#barcode_equ :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		ctx['delivery'] = true
	   	var report_data = [];
	   	if ( quantity && operation_type && responsible && team){
		   	report_data.push({
				'quantity': quantity,
				'responsible': responsible,
				'operation_type': operation_type,
				'maintenance_number':maintenance_number,
				'task_number':task_number,
				'team': team,
				'barcode_ids' :barcode_list,
 				});
			self._rpc({
			        model: 'operation.dashboard',
			        method: 'update_task',
			        args: [[],report_data ,ctx],
			    })
	            .then(function(result) {
	            	if (result.success) {
	            		return self.$el.html(QWeb.render("Confirm", {widget: self}));
	            	}
	            	else if(result.delivery_warning){

                            self.do_warn(_("Warning"),_("Equipment has already delivered!"));
	            	}
	            	else if(result.return_warning){
                            self.do_warn(_("Warning"),_("Equipment has already returned!"));
	            	}
	            	else{
	            		self.do_warn(_("Warning"),_("No Data Found!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Something Wrong!! Please check selected Data!"));
  }
},



// Confirm main screen

	main_button : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();

	    return self.$el.html(QWeb.render("WarehouseButton", {widget: self}));
},


// save internal Transfer

       save_internal_transfer : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();
	   	//var location = $(".es-list li[value='" + document.getElementById("my-select").val() + "']").attr('ids');
            var location = $("#my-select").val() ;

            var dest_location_id =  $("#my-dest-select").val() ;
            var barcode_ids =  $("#barcode_product").attr("ids");
         var product_id = $("#my-canet-product").val();
         console.log("_--------product_id-------------",product_id)
		var type_of_order = document.getElementById("type-select").value;
		var task_number = $("#task_number").val() ;
		var maintenance_number =  $("#maintenance_number").val() ;
	   	var report_data = [];
		var barcode_list = []
		var allow_save = true
	   	if (location == undefined ){
			self.do_warn(_("Warning"),_("Please Select Inventoried Location First!"));
		}
		if (product_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Product!!"));
		}
		if (dest_location_id == undefined ){
			self.do_warn(_("Warning"),_("Please Select Destination Location"));
		}
		if (type_of_order == undefined ){
			self.do_warn(_("Warning"),_("Please Select Order Type!"));
		}
		if (type_of_order != undefined ){
		      if (type_of_order == 'Proyecto' ){
		            $("#transfer_to_task_button").css("display", "inline");
                    if (task_number == undefined ){
                        self.do_warn(_("Warning"),_("Please Select Task Number!"));

                    }
		      }
		      if (type_of_order == 'Mantenimiento' ){
		            $("#transfer_to_task_button").css("display", "inline");
                    if (maintenance_number == undefined ){
                        self.do_warn(_("Warning"),_("Please Select Maintenance Number!"));

                    }
		      }
		      if (type_of_order == 'Transferencia interna' ){
		            $("#create_internal_transfer_button").css("display", "inline");
		      }
		}


		$("#barcode_product :selected").each(function(){
			barcode_list.push(parseInt($(this).attr("ids")))
		    });
		if (location != undefined &&  product_id != undefined   && dest_location_id != undefined  &&  type_of_order != undefined) {
		   	report_data.push({
				'location': location,

				'type_of_order': type_of_order,
				'dest_location_id': dest_location_id,
				'barcode_ids' :barcode_list,
 				});
			self._rpc({
			        model: 'operation.dashboard',
			        method: 'save_internal_transfer_method',
			        args: [[],report_data ],
			    })

	            .then(function(result) {

	            	if (result.success) {
	            		self.do_warn(_("Success"),_("Record Saved"));
	            		// hide validate barcode button
	            		$("#edit_internal_transfer_button").css("display", "inline");

				$("#save_internal_transfer_button").css("display", "none");
				$("#type-select").attr("disabled", true);
				$("#my-dest-select").attr("disabled", true);
				$("#my-select").attr("disabled", true);
				$("#my-canet-product").attr("disabled", true);
				$("#barcode_product").attr("disabled", true);
				$("#maintenance_number").attr("disabled", true);
				$("#task_number").attr("disabled", true);
	            		// hide delete button
	            	}else{
	            		self.do_warn(_("Warning"),_("Can not save!!"));
	            	}
	               });
        }else{
              self.do_warn(_("Warning"),_("Can not save!!"));
  }
},

//save_delivery_return_button

  save_delivery_return_button : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();

        var equipment_id =document.getElementById('my-canet-equ').value;
        var barcode_ids =  document.getElementById('barcode_equ').value;
        var quantity =  $("#quantity").val() ;
		var type_of_order = document.getElementById("type-select").value;
		var responsible = document.getElementById("technician_list").value;
		var team = document.getElementById("team_list").value;
		var task_number = $("#task_number").val() ;
		var maintenance_number =  $("#maintenance_number").val() ;
	   	var report_data = [];
		var barcode_list = []
		var allow_save = true
		if (equipment_id == undefined || equipment_id ==''){
			self.do_warn(_("Warning"),_("Please Select equipment!!"));
		}
		if (barcode_ids == undefined ||  barcode_ids == '' ){
		    console.log("___________________")
			self.do_warn(_("Warning"),_("Please Select equipment!!"));
		}
		if (responsible == undefined  || responsible == ''){
			self.do_warn(_("Warning"),_("Please Select Responsible !!"));
		}
		if (team == undefined || team == ''){
			self.do_warn(_("Warning"),_("Please Select Team !!"));
		}
		if (type_of_order == undefined || type_of_order == ''){
			self.do_warn(_("Warning"),_("Please Select Order Type!"));
		}
		if (quantity == undefined ||  quantity == ''){
			self.do_warn(_("Warning"),_("Please Add Quantity!"));
		}
		if (type_of_order != undefined ){
		      if (type_of_order == 'Proyecto' ){
		            console.log("+_____________________")
//		            $("#transfer_to_task_delivery_button").css("display", "inline");
                    if (task_number == undefined ){
                        self.do_warn(_("Warning"),_("Please Select Task Number!"));

                    }
		      }
		      if (type_of_order == 'Mantenimiento' ){
//		            $("#transfer_to_task_delivery_button").css("display", "inline");
                    if (maintenance_number == undefined ){
                        self.do_warn(_("Warning"),_("Please Select Maintenance Number!"));

                    }
		      }

		}


            if(equipment_id && barcode_ids && quantity && type_of_order && responsible && team ) {
	            $("#edit_delivery_return_button").css("display", "inline");
                $("#transfer_to_task_button").css("display", "inline");
                $("#return_to_task_button").css("display", "none");
				$("#save_delivery_return_button").css("display", "none");
				$("#type-select").attr("disabled", true);
				$("#task_number").attr("disabled", true);
				$("#maintenance_number").attr("disabled", true);
				$("#technician_list").attr("disabled", true);
				$("#team_list").attr("disabled", true);
				$("#quantity").attr("disabled", true);
				$("#operation_type").attr("disabled", true);
				$("#lot_selection").attr("disabled", true);
				$("#barcode_equ").attr("disabled", true);
				$("#my-canet-equ").attr("disabled", true);
	            		// hide delete button

	        self.do_warn(_("Success"),_("Record Saved"));
        }
},




// edit delivery return

       edit_delivery_return_button : function(event){
	   	var self = this;
	   	event.stopPropagation();
	   	event.preventDefault();

                // hide validate barcode button
               $("#edit_delivery_return_button").css("display", "none");
                $("#transfer_to_task_button").css("display", "none");
                $("#return_to_task_button").css("display", "none");
				$("#save_delivery_return_button").css("display", "inline");
				$("#type-select").attr("disabled", false);
				$("#task_number").attr("disabled", false);
				$("#maintenance_number").attr("disabled", false);
				$("#technician_list").attr("disabled", false);
				$("#team_list").attr("disabled", false);
				$("#quantity").attr("disabled", false);
				$("#operation_type").attr("disabled", false);
				$("#lot_selection").attr("disabled", false);
				$("#barcode_equ").attr("disabled", false);
				$("#my-canet-equ").attr("disabled", false);

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
core.action_registry.add('canet_screen_act', CanetScreen);

return CanetScreen;

});
