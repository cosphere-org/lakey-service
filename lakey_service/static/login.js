function renderButton() {
    gapi.signin2.render('google-auth-button', {
        'scope': 'profile email',
        'width': 240,
        'height': 50,
        'longtitle': true,
        'theme': 'dark',
        'onsuccess': onSuccess,
        'onfailure': onFailure
  });
}

function onSuccess(googleUser) {
    let $done = document.getElementById('done');
    let $wait = document.getElementById('wait');
    let $authenticate = document.getElementById('authenticate');

    let authRequestUUID = '{{ auth_request_uuid }}';
    let profile = googleUser.getBasicProfile();

    let xhr = new XMLHttpRequest();
    xhr.open(
        'POST',
        '/accounts/auth_requests/attach_account/');

    xhr.setRequestHeader(
        "Content-Type", "application/json;charset=UTF-8");

    xhr.send(
        JSON.stringify({
            request_uuid: authRequestUUID,
            oauth_token: googleUser.getAuthResponse().id_token,
            email: profile.getEmail(),
        })
    );

    // -- hide AUTHENTICATE view and show WAIT view
    $authenticate.style['display'] = 'none';
    $wait.style['display'] = 'flex';

    xhr.onload = () => {
        // -- hide WAIT view and show DONE view
        $wait.style['display'] = 'none';
        $done.style['display'] = 'flex';
    };
}

function onFailure(error) {
    console.error(error);
}
