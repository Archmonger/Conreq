$(document).ready(async function () {
	$(".sidebar").trigger("prepare");
	new SimpleBar($("#sidebar")[0]);
	$(".sidebar").trigger("loaded");
});
