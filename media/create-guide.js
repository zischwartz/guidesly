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
					just_floating_list= $.map($(".floating_card_container").sortable('toArray'), function(n) {return parseInt(n);});
					VM.card_order(new_order);
					VM.floating_list(just_floating_list);
					// console.log(new_order);
					for (i in VM.normal_cards())
						{VM.normal_cards()[i].card_number(parseInt(i)+1);}
					
					// This is good code, for the future, but with readonly true on cards in the api, not neccesary
					// var cards = ko.toJS(VM.cards);
					// var mapped_cards = ko.utils.arrayMap(cards, function(card) {
					//     delete card.absolute_url;
					//     delete card.edit_url;
					//     delete card.primary_media;
					//     delete card.resource_uri;
					//     return card;
					// });
					// VM.cards(mapped_cards) ;
					// console.log(just_floating)
					// VM.just_floating_cards(just_floating);
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

var deleteCard= function(event)
{
	// console.log(event.target.parents(".smallcardWrapper"));
	$.ajax({
		url: this.resource_uri(),
		type: "DELETE",
		success:function(data) { console.log(data); },
		contentType: "application/json",
	});
	
	console.log($(this));
	
	VM.cards.remove(this);
	if (VM.floating_cards.indexOf(this)!=-1)
		VM.floating_cards.remove(this);
		
	if (VM.normal_cards.indexOf(this)!=-1)
		VM.normal_cards.remove(this);

};


// DOCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCREADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYYYYYY
// DOCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCREADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDYYYYYY

$(document).ready(function(){	

	// $(".uibutton").button();
	
	$(".delete_link").live('click',function(event){
		$(this).parent().addClass('confirm_delete');
		event.preventDefault();
		
	});
	

	
	
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
		handle: '.cardNumber, .smallcard',
	}).disableSelection();

// Publishing Options

VM.private_guide = ko.observable();


//autocomplete for tags
function split( val ) {
    return val.split( /,\s*/ );
}
function extractLast( term ) {
    return split( term ).pop();
}

$("#id_tags").autocomplete({
		delay: 500,
		autoFocus: true,
		source: function(request, response){
			$.getJSON(tag_api_url, {
				term: extractLast(request.term)
			}, response);
		},
		search: function(){
			var term = extractLast(this.value);
			if (term.length < 1) {
				return false;
			}
		},
		focus: function(){
			// prevent value inserted on focus
			return false;
		},
		select: function(event, ui){
			var terms = split(this.value);
			// remove the current input
			terms.pop();
			// add the selected item
			terms.push(ui.item.value);
			// add placeholder to get the comma-and-space at the end
			terms.push("");
			this.value = terms.join(", ");
			return false;
		}
		
		});
		
		




	ko.applyBindings(VM);

});
//end docready


