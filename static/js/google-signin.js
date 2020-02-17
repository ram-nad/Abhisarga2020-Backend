function init() {
    gapi.load('auth2', function () {
        auth2 = gapi.auth2.init({
            client_id: document.querySelector("meta[name='GOOGLE_CLIENT_ID']").getAttribute("content"),
            ux_mode: 'popup'
        });
        auth2.attachClickHandler(document.getElementById('google-sign-in-button'), {}, googleSignIn, signInFailed);
    });
}

function googleSignIn(googleUser) {
    let form = document.getElementById('google-sign-in-submit-form');
    form.getElementsByTagName('input')[1].value = googleUser.getAuthResponse().id_token;
    form.submit();
}

function signInFailed(error) {
    alert(`Google Sign-In Failed. (${error.error})`)
}