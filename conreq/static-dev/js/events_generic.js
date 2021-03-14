$(".viewport-container").on("prepare", async function () {
	if ($("table").length) {
		$("table").bootstrapTable();
	}
});

$(".viewport-container").on("destroy", async function () {
	if ($("table").length) {
		$("table").bootstrapTable("destroy");
	}
});
