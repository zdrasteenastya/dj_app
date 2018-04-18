// Form toggles between login and sign up, 0 for login and 1 for signup
var formType = 0;

function formToggle() {
    // flip function for formType value
    formType++;
    formType = formType % 2;

    // If it's a signup form
    if (formType === 1) {

        // Hide login elements
        $("#login_form").slideUp(250);
        $('#login_validation_errors').slideUp(250);

        // Modify text based elements for signup
        $("#formHeading").fadeOut(250, function () {
            $(this).text("Sign up or ").fadeIn(250);
        });
        $("#formOption").fadeOut(250, function () {
            $(this).text("Login").fadeIn(250);
        });

        // Show signup elements
        $("#signup_form").slideDown(250);

    }

    // If it's a login form
    if (formType === 0) {

        // Hide signup elements
        $("#signup_form").slideUp(250);
        $('#signup_validation_errors').slideUp(250);

        // Modify text based elements
        $("#formHeading").fadeOut(250, function () {
            $(this).text("Login or ").fadeIn(250);
        });
        $("#formOption").fadeOut(250, function () {
            $(this).text("Sign up").fadeIn(250);
        });

        // Show Login elements
        $('#login_form').slideDown(250);
    }

};



