var Fvm;
var fsParent;
var f_api_url = '/api/v1/thef/'

$(document).ready(function(){	

// alert('hi');
// $("#thef-dialog").dialog({ autoOpen: false });

$("#thef-dialog").dialog({ autoOpen: false,
	 					draggable: false,
						modal: true,
						minWidth: 450,
						buttons: { "Send": function() { $(this).dialog('close'); sendFData(); }, "Cancel":function() { $(this).dialog("close"); }  },
					});
					
sendFData = function() {
	// alert('hi');
	Fvm.the_parent(fsParent.attr('id'));
	theviewmodel = ko.mapping.toJSON(VM);
	thefvm= ko.toJSON(Fvm);
	// jsonData = {"feedback": thefvm, "overall": theviewmodel, "parent": = fsParent };
	// jsonData = {"the_data": "somedata"};

	// jsonData = JSON.stringify({"the_data_text" : "somedata"});
	jsonData = JSON.stringify({"the_data_text" : {"feedback": thefvm, "overal-vm": theviewmodel}});

	// console.log(jsonData);
	$.ajax({
				url: f_api_url,
				type: "POST",
				data: jsonData,
				success:function(data) {
					console.log('done');
					// console.log(data);	
					Fvm.choice(null);
					Fvm.was_buggy(null);
					Fvm.like_reason("It allows me to");
					Fvm.dislike_reason("It doesn't allow me to");
					Fvm.the_parent(null);
				},	
			contentType: "application/json",	
		});

}

$(".F").live('click', function(){
	fsParent = $(this).parent();
	$("#thef-dialog").dialog('open');
});


$('.ui-widget-overlay').live('click', function() { 
	$("#thef-dialog").dialog("close"); 
});


Fvm ={
	choice: ko.observable(),
	was_buggy: ko.observable(),
	like_reason: ko.observable("It allows me to"),
	dislike_reason: ko.observable("It doesn't allow me to"),
	the_parent: ko.observable(),
}


ko.applyBindings(Fvm, document.getElementById('thef-dialog'))

}); //end docready
