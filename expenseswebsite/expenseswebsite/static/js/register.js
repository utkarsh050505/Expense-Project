const usernameField = document.querySelector('#usernameField');
const usernameFeedbackField = document.querySelector(".invalid-feedback-username");
const emailField = document.querySelector("#emailField");
const emailFeedbackField = document.querySelector(".invalid-feedback-email");
const passwordField = document.querySelector('#passwordField');
const passwordToggleView = document.querySelector(".toggleView");
const submitButton = document.querySelector(".submit-btn");

const handleToggle = (event) => {
    if (passwordToggleView.textContent == 'SHOW') {
        passwordToggleView.textContent = 'HIDE';
        passwordField.setAttribute("type", "text");
    }
    else {
        passwordToggleView.textContent = 'SHOW';
        passwordField.setAttribute("type", "password");
    }
}

passwordToggleView.addEventListener('click', handleToggle)

emailField.addEventListener('keyup', (event) => {
    emailVal = event.target.value;
    emailField.classList.remove("is-invalid");
    emailFeedbackField.style.display = "none";
    emailFeedbackField.innerHTML = ``;

    if (emailVal.length > 0) {
        fetch('/authentication/validate-email', {
            body: JSON.stringify({email: emailVal}),
            method: 'POST',
        })
        .then(
            response => response.json()
        )
        .then(
            data => {
                if (data.email_error) {
                    emailField.classList.add("is-invalid");
                    emailFeedbackField.style.display = "block";
                    emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
                    submitButton.setAttribute("disabled", "true");
                } else { submitButton.removeAttribute("disabled"); }
            }
        )
    }
})

usernameField.addEventListener('keyup', (event) => {
    usernameVal = event.target.value;
    usernameField.classList.remove('is-invalid');
    usernameFeedbackField.style.display = 'none';
    usernameFeedbackField.innerHTML = ``;
    
    if (usernameVal.length > 0) {
        fetch('/authentication/validate-username', {
            body: JSON.stringify({username: usernameVal}),
            method: 'POST',
        })
        .then(
            respose => respose.json()
        )
        .then(
            data => {
                if (data.username_error) {
                    usernameField.classList.add('is-invalid');
                    usernameFeedbackField.style.display = 'block';
                    usernameFeedbackField.innerHTML = `<p>${data.username_error}</p>`;
                    submitButton.setAttribute("disabled", "true");
                } else { submitButton.removeAttribute("disabled"); }
            }
        );
    }
})