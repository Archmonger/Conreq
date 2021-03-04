let current_tab_num = 0; // Current tab is set to be the first tab (0)
let all_tabs = document.getElementsByClassName("tab");
let all_step_indicators = document.getElementsByClassName("step");
let last_tab_num = all_tabs.length - 1;
let password = document.getElementById("password");
let confirm_password = document.getElementById("confirm_password");

let show_tab = function () {
	// Display the current tab
	let all_tabs = document.getElementsByClassName("tab");
	all_tabs[current_tab_num].style.display = "flex";

	// Change the string in the buttons if needed
	if (current_tab_num == last_tab_num) {
		document.getElementById("nextBtn").innerHTML = "Submit";
	} else {
		document.getElementById("nextBtn").innerHTML = "Next";
	}

	// Hide/show the previous button depending on what page we are on
	if (current_tab_num == 0) {
		document.getElementById("prevBtn").style.visibility = "hidden";
	} else {
		document.getElementById("prevBtn").style.visibility = "visible";
	}
};

let next_tab = function () {
	// Exit the function if any field in the current tab is invalid
	if (!validate_tab()) {
		console.log("tab not valid");
		return false;
	}

	// if you have reached the end of the form, submit it
	if (current_tab_num == last_tab_num) {
		document.getElementById("initialization-form").submit();
		return false;
	}

	// Hide the current tab:
	all_tabs[current_tab_num].style.display = "none";

	// Otherwise, display the correct tab:
	current_tab_num += 1;
	show_tab();
	next_step_indicator();
};

let previous_tab = function () {
	// Hide the current tab:
	all_tabs[current_tab_num].style.display = "none";

	// Otherwise, display the correct tab:
	current_tab_num -= 1;
	show_tab();
	previous_step_indicator();
};

let validate_tab = function () {
	let input_valid = true;
	let required_inputs = all_tabs[current_tab_num].querySelectorAll(
		"input[required]"
	);

	// Confirm if all fields are filled out
	required_inputs.forEach(function (element) {
		if (!element.value) {
			input_valid = false;
			element.classList.add("invalid");
		} else {
			element.classList.remove("invalid");
		}
	});

	// Confirm if passwords match
	if (input_valid) {
		console.log("checking password");
		input_valid = validate_password();
	}

	return input_valid;
};

let validate_password = function () {
	if (password.value != confirm_password.value) {
		passwords_dont_match_toast_message();
		return false;
	} else {
		return true;
	}
};

let next_step_indicator = function () {
	let previous_step = all_step_indicators[current_tab_num - 1];
	let current_step = all_step_indicators[current_tab_num];

	if (current_tab_num > 0) {
		// Remove active and add finish to the previous step
		previous_step.classList.remove("active");
		previous_step.classList.add("finish");
	}

	// Add active to the current step
	current_step.classList.add("active");
};

let previous_step_indicator = function () {
	let next_step = all_step_indicators[current_tab_num + 1];
	let current_step = all_step_indicators[current_tab_num];

	// Remove active and finish on the right step
	next_step.classList.remove("active");
	next_step.classList.remove("finish");
	// Add active and remove finish on the current step
	current_step.classList.remove("finish");
	current_step.classList.add("active");
};
