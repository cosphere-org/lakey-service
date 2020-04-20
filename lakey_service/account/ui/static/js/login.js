(() => {

    let $dom = {
        signin: $('.signin a'),
        catalogueItems: $('.catalogue-items'),
        // -- TOKEN
        copyTokenToClipboard: $('.token a'),
        token: $('.token'),
        tokenInput: $('.token input'),
    }

    let oauth2;

    let init = () => {
      gapi.load('auth2', () => {
        oauth2 = gapi.auth2.init();
        $dom.signin.removeClass('disabled');
      });
    }

    /**
     * EVENTS
     */
    $dom.signin.on('click', () => {
        let options = new gapi.auth2.SigninOptionsBuilder();
        options.setAppPackageName('com.example.app');
        options.setPrompt('select_account');
        options.setScope('profile').setScope('email');

        oauth2.signIn(options)
            .then(_ => {
                let user = oauth2.currentUser.get();
                let email = user.getBasicProfile().getEmail();
                let oauth2token = user.getAuthResponse().id_token;
                let authRequestUUID = isAttachAccountToAuthRequest();

                // -- make a call to the BE to generate user token
                apiCreateAuthToken(email, oauth2token).then(token => {
                    $dom.signin.css('display', 'none');

                    Cookies.set('lakey-auth-token', token);

                    if (authRequestUUID) {
                        $dom.token.css('display', 'flex');
                        $dom.tokenInput.val(token);
//                     apiAttachAccountToAuthRequest(email, oauth2token, authRequestUUID).then(_ => {
// console.log('AUTH REQUEST DONE');
//                     });

                    } else {
                        $dom.catalogueItems.css('display', 'flex');

                    }

                }).catch(error => {
                    console.error(error);
                });

            })
            .catch(error => {
                console.error(error);
            });
    });

    $dom.copyTokenToClipboard.on('click', () => {

      $dom.tokenInput.select();

      document.execCommand('copy');
      alert('API token copied to the Clipboard');
    });

    /**
     * API
     */
    apiCreateAuthToken = (email, oauth2token) => {
        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();
            xhr.open(
                'POST',
                '/accounts/auth_tokens/');

            xhr.setRequestHeader(
                "Content-Type", "application/json;charset=UTF-8");

            xhr.send(
                JSON.stringify({
                    oauth_token: oauth2token,
                    email: email,
                }));

            xhr.onload = () => {
                resolve(JSON.parse(xhr.response).token);
            };
        });
    }

    let isAttachAccountToAuthRequest = () => {
        let parseQuery = queryString => {
            let query = {};
            let pairs = (queryString[0] === '?' ? queryString.substr(1) : queryString).split('&');
            for (let i = 0; i < pairs.length; i++) {
                let pair = pairs[i].split('=');
                query[decodeURIComponent(pair[0])] = decodeURIComponent(pair[1] || '');
            }

            return query;
        }

        return parseQuery(window.location.search.substring(1))['auth_request_uuid'];
    }

    apiAttachAccountToAuthRequest = (email, oauth2token, authRequestUUID) => {
        return new Promise((resolve, reject) => {
            let xhr = new XMLHttpRequest();
            xhr.open(
                'POST',
                '/accounts/auth_requests/attach_account/');

            xhr.setRequestHeader(
                "Content-Type", "application/json;charset=UTF-8");

            xhr.send(
                JSON.stringify({
                    request_uuid: authRequestUUID,
                    oauth_token: oauth2token,
                    email: email,
                }));

            xhr.onload = () => {
                resolve();
            };
        });
    }

    /**
     * EXPORTS
     */
    window.init = init;
})();
