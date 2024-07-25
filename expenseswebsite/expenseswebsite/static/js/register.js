const usernameField = document.querySelector('#usernameField');
const feedbackField = document.querySelector(".invalid-feedback")

usernameField.addEventListener('keyup', (event) => {
    usernameVal = event.target.value;
    usernameField.classList.remove('is-invalid');
    feedbackField.style.display = 'none';
    feedbackField.innerHTML = ``;
    
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
                console.log("data", data);
                if (data.username_error) {
                    usernameField.classList.add('is-invalid');
                    feedbackField.style.display = 'block';
                    feedbackField.innerHTML = `<p>${data.username_error}</p>`;
                }
            }
        );
    }
})