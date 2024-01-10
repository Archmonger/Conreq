// TODO: Delete this file after view_to_iframe is fleshed out

window.document.addEventListener(
	"reload-page",
	async function (event) {
		window.location.reload();
	},
	false
);

window.document.addEventListener(
	"generic-toast",
	async function (event) {
		default_params = {
			titleColor: "var(--accent-color)",
			messageColor: "var(--accent-color)",
			iconColor: "var(--accent-color)",
			progressBarColor: "var(--accent-color)",
		};
		iziToast.show({ ...default_params, ...event.detail });
	},
	false
);

window.document.addEventListener(
	"success-toast",
	async function (event) {
		default_params = {
			icon: "fas fa-check-circle",
			title: "Success",
			titleColor: "var(--accent-color)",
			messageColor: "var(--accent-color)",
			iconColor: "var(--accent-color)",
			progressBarColor: "var(--accent-color)",
		};
		iziToast.show({ ...default_params, ...event.detail });
	},
	false
);

window.document.addEventListener(
	"warning-toast",
	async function (event) {
		default_params = {
			icon: "fas fa-exclamation-triangle",
			title: "Warning",
			titleColor: "#9a5c0f",
			messageColor: "#9a5c0f",
			iconColor: "#c57615",
			progressBarColor: "var(--accent-color)",
		};
		iziToast.show({ ...default_params, ...event.detail });
	},
	false
);
