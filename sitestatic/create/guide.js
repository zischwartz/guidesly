var card_api_url='/api/v1/card/';
var staticel_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';
var guide_api_url='/api/v1/guide/';
// var smallcard_api_url='/api/v1/smallcard/';

var VM; //our viewmodel


//connect items with observableArrays
ko.bindingHandlers.sortableList = {
    init: function(element, valueAccessor, allBindingsAccessor, context) {
        $(element).data("sortList", valueAccessor()); //attach meta-data
        $(element).sortable({
			start: function(event, ui){
			var sc_height= $(".smallcardWrapper").outerHeight();
			},
            update: function(event, ui) {
                var item = ui.item.data("sortItem");
                if (item) {
					$(".normal_card_container .cardNumber span").fadeOut(500).fadeIn(500);

					//hacky way to see if it's floating or normal now
					var is_now_normal = ui.item.parent().hasClass("normal_card_container");
                    item.is_floating_card(!is_now_normal);
					// console.log(item);
					//identify parents					
                    var originalParent = ui.item.data("parentList");
                    var newParent = ui.item.parent().data("sortList");
                    //figure out its new position
                    var position = ko.utils.arrayIndexOf(ui.item.parent().children(), ui.item[0]);
                    if (position >= 0) {
                        originalParent.remove(item);
                        newParent.splice(position, 0, item);
                    }
					//my code follows (above is knockmeout guy's)
					new_order = $.map($(".normal_card_container").sortable('toArray'), function(n) {return parseInt(n);}); 
					// console.log(new_order);
					for (i in VM.normal_cards())
						{VM.normal_cards()[i].card_number(parseInt(i)+1);}
						
						var jsonData = ko.mapping.toJSON(VM);
						$.ajax({
							url: VM.resource_uri(),
							type: "PUT",
							data:jsonData,
							//success:function(data) { console.log(data); },
							contentType: "application/json",
							})
                }
            },
            connectWith: '.connectedSortable'
        });
    }
};

//attach meta-data
ko.bindingHandlers.sortableItem = {
    init: function(element, valueAccessor) {
        var options = valueAccessor();
        $(element).data("sortItem", options.item);
        $(element).data("parentList", options.parentList);
    }
};


$(document).ready(function(){	

	$(".uibutton").button();

	
	
	jQuery.easing.def = "easeOutQuart";
	
	initial_guide_object= jQuery.parseJSON(guide_json);

	VM = ko.mapping.fromJS(initial_guide_object);

	VM.normal_cards= ko.observableArray();
	VM.floating_cards= ko.observableArray();
	//divide cards between normal and floating

	for (i in VM.cards())
		{
			if (VM.cards()[i].is_floating_card())
				{VM.floating_cards.push(VM.cards()[i]);}
			else
				{VM.normal_cards.push(VM.cards()[i]);}
		}
	
		
	$( ".normal_card_container, .floating_card_container" ).sortable({
		cursor: 'move',
		revert: 300,
		placeholder: "smallcardWrapperPlaceHolder",
		tolerance: 'pointer',
		items: '.smallcardWrapper',
	}).disableSelection();

	ko.applyBindings(VM);

});


