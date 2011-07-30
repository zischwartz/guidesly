var card_api_url='/api/v1/card/';
var staticel_api_url='/api/v1/mediaelement/';
var input_api_url='/api/v1/inputelement/';
var action_api_url='/api/v1/action/';
var file_api_url='/api/v1/userfile/';
var guide_api_url='/api/v1/guide/';
// var smallcard_api_url='/api/v1/smallcard/';

var VM; //our viewmodel




$(document).ready(function(){

$(".uibutton").button();

jQuery.easing.def = "easeOutQuart";
console.log('hi');
	
initial_guide_object= jQuery.parseJSON(guide_json);


VM = ko.mapping.fromJS(initial_guide_object);//, mapping);
// console.log(VM);

ko.applyBindings(VM);

});