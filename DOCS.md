
# CoSphere API
CoSphere's API with hypermedia links
## Account & Auth Management
### ATTACH_ACCOUNT_TO_AUTH_REQUEST: POST /accounts/auth_requests/attach_account/
Attach Account to Auth Request 
None
#### 200 (ACCOUNT_TO_AUTH_REQUEST_ATTACHED)
Request:
```http
POST /accounts/auth_requests/attach_account/ HTTP/1.1
CONTENT-TYPE: application/json
{
    "code": "some-authorization-code",
    "email": "jacky@somewhere.org",
    "request_uuid": "2fbb0015-4669-11e9-b05d-0028f8484bd5"
}
```
Respone:
```json
{
    "@event": "ACCOUNT_TO_AUTH_REQUEST_ATTACHED",
    "@type": "empty"
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /accounts/auth_requests/attach_account/ HTTP/1.1
CONTENT-TYPE: application/json
{
    "email": "jacky@somewhere.org",
    "request_uuid": "some-uuid"
}
```
Respone:
```json
{
    "@event": "BODY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "code": [
            "This field is required."
        ],
        "request_uuid": [
            "\"some-uuid\" is not a valid UUID."
        ]
    },
    "user_id": "anonymous"
}
```
#### 404 (COULD_NOT_FIND_AUTHREQUEST)
Request:
```http
POST /accounts/auth_requests/attach_account/ HTTP/1.1
CONTENT-TYPE: application/json
{
    "code": "some-code",
    "email": "jacky@somewhere.org",
    "request_uuid": "2fbb0016-4669-11e9-b05d-0028f8484bd5"
}
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_AUTHREQUEST",
    "@type": "error",
    "user_id": "anonymous"
}
```
### CREATE_AUTH_REQUEST: POST /accounts/auth_requests/
Create Auth Request 
None
#### 201 (AUTH_REQUEST_CREATED)
Request:
```http
POST /accounts/auth_requests/ HTTP/1.1
```
Respone:
```json
{
    "@event": "AUTH_REQUEST_CREATED",
    "@type": "auth_request",
    "authenticate_ui_uri": "/accounts/auth_requests/2fbb0014-4669-11e9-b05d-0028f8484bd5/authenticate/ui/",
    "request_uuid": "2fbb0014-4669-11e9-b05d-0028f8484bd5"
}
```
### CREATE_AUTH_TOKEN: POST /accounts/auth_tokens/
Create Auth Token 
None
#### 201 (AUTH_TOKEN_CREATED)
Request:
```http
POST /accounts/auth_tokens/ HTTP/1.1
CONTENT-TYPE: application/json
{
    "request_uuid": "2fbb0017-4669-11e9-b05d-0028f8484bd5"
}
```
Respone:
```json
{
    "@event": "AUTH_TOKEN_CREATED",
    "@type": "auth_token",
    "token": "fd78cd7d87f"
}
```
#### 400 (EXPIRED_AUTH_REQUEST_DETECTED)
Request:
```http
POST /accounts/auth_tokens/ HTTP/1.1
CONTENT-TYPE: application/json
{
    "request_uuid": "f5e7e000-5074-11e4-b2e7-02426ec57dd1"
}
```
Respone:
```json
{
    "@event": "EXPIRED_AUTH_REQUEST_DETECTED",
    "@type": "error",
    "user_id": null
}
```
#### 404 (COULD_NOT_FIND_AUTHREQUEST)
Request:
```http
POST /accounts/auth_tokens/ HTTP/1.1
CONTENT-TYPE: application/json
{
    "request_uuid": "f5e7e000-5074-11e4-825f-02426ec57dd1"
}
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_AUTHREQUEST",
    "@type": "error",
    "user_id": "anonymous"
}
```
### RENDER_AUTH_REQUEST_AUTHENTICATE_UI: GET /accounts/auth_requests/{request_uuid}/authenticate/ui/
Render Auth Request Authentication UI 
None
#### 200
Request:
```http
GET /accounts/auth_requests/some-uuid/authenticate/ui/ HTTP/1.1
```
Respone:
```json
"<!DOCTYPE html>\n<html>\n    <head>\n        <title>Lakey Authentication</title>\n        <meta\n            name=\"google-signin-client_id\"\n            content=\"961918528927-12heq0l9f1tep1igb29tatkf2pr2p5f7.apps.googleusercontent.com\">\n\n        <link\n            href=\"https://fonts.googleapis.com/css?family=IBM+Plex+Sans\"\n            rel=\"stylesheet\">\n        <style>\n            body {\n                background: #e4e4e4;\n            }\n\n            #main {\n                height: 200px;\n                width: 100%;\n                font-family: 'IBM Plex Sans', sans-serif;\n            }\n\n            h2 {\n                font-weight: normal;\n            }\n\n            #authenticate {\n                display: flex;\n                flex-direction: column;\n                align-items: center;\n                justify-content: center;\n            }\n        </style>\n        <script\n            type=\"text/javascript\">\n\n            function renderButton() {\n                gapi.signin2.render('google-auth-button', {\n                    'scope': 'profile email',\n                    'width': 240,\n                    'height': 50,\n                    'longtitle': true,\n                    'theme': 'dark',\n                    'onsuccess': onSuccess,\n                    'onfailure': onFailure\n              });\n            }\n\n            function onSuccess(googleUser) {\n                let authRequestUUID = 'some-uuid';\n                let profile = googleUser.getBasicProfile();\n                let authorizationCode = googleUser.getAuthResponse().id_token;\n\n                // FIXME: add ajax call!\n                // FIXME: add progress while waiting for ajax\n                // FIXME: add switch to done screen\n                // FIXME: add switch something went wrong screen\n                // FIXME: add nice font\n                // https://developers.google.com/identity/sign-in/web/build-button\n                console.log('id_token: ' + authorizationCode);\n                console.log('Email: ' + profile.getEmail());\n\n                // document.body.innerHTML = '<div>DONE!</done>';\n            }\n\n            function onFailure(error) {\n                console.log(error);\n            }\n\n        </script>\n        <script\n            src=\"https://apis.google.com/js/platform.js?onload=renderButton\"\n            async\n            defer>\n        </script>\n    </head>\n\n    <body>\n\n        <div\n            id=\"main\">\n            <div\n                id=\"authenticate\">\n\n                <h2>Sign In To Lakey</h2>\n                <div\n                    id=\"google-auth-button\"></div>\n            </div>\n\n            <div\n                id=\"done\">\n\n                DONE\n            </div>\n\n        </div>\n    </body>\n\n</html>\n"
```
## Catalogue Items Management
### BULK_READ_CATALOGUEITEMS: GET /catalogue/items/
Bulk Read Catalogue Items 
None
#### 200 (CATALOGUEITEMS_BULK_READ)
Request:
```http
GET /catalogue/items/?query=IoT HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjYsImVtYWlsIjoienJheW5vckB6aWVtYW5uLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MTcyMH0.rpcJ1JJS9WMG2ONHMnO9RPaQ87Sv9TEtQSEaNwrA8Xs
```
Respone:
```json
{
    "@event": "CATALOGUEITEMS_BULK_READ",
    "@type": "catalogue_items_list",
    "items": [
        {
            "@type": "catalogue_item",
            "created_by": null,
            "executor_type": "DATABRICKS",
            "maintained_by": null,
            "name": "iot_features",
            "sample": [],
            "spec": [
                {
                    "distribution": null,
                    "is_nullable": false,
                    "name": "location",
                    "size": 190234,
                    "type": "STRING"
                },
                {
                    "distribution": [
                        {
                            "count": 9,
                            "value": 18.0
                        },
                        {
                            "count": 45,
                            "value": 19.1
                        },
                        {
                            "count": 10,
                            "value": 21.2
                        }
                    ],
                    "is_nullable": true,
                    "name": "value",
                    "size": null,
                    "type": "FLOAT"
                }
            ],
            "updated_by": null
        },
        {
            "@type": "catalogue_item",
            "created_by": null,
            "executor_type": "ATHENA",
            "maintained_by": null,
            "name": "iot_events",
            "sample": [],
            "spec": [
                {
                    "distribution": null,
                    "is_nullable": false,
                    "name": "location",
                    "size": 190234,
                    "type": "STRING"
                },
                {
                    "distribution": [
                        {
                            "count": 9,
                            "value": 18.0
                        },
                        {
                            "count": 45,
                            "value": 19.1
                        },
                        {
                            "count": 10,
                            "value": 21.2
                        }
                    ],
                    "is_nullable": true,
                    "name": "value",
                    "size": null,
                    "type": "FLOAT"
                }
            ],
            "updated_by": null
        }
    ]
}
```
#### 400 (QUERY_DID_NOT_VALIDATE)
Request:
```http
GET /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJubWVydHpAc2NodWx0ei5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI1ODkxNjJ9.Kklg4jUQ1sVSVikR1BZJAnWYEkE4a-AxXdPQpWJsShc
```
Respone:
```json
{
    "@event": "QUERY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "query": [
            "This field is required."
        ]
    },
    "user_id": "anonymous"
}
```
#### 500 (GENERIC_ERROR_OCCURRED)
Request:
```http
GET /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJ0bGVzY2hAb2Nvbm5lci5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI1ODkxOTJ9.S19vG5wViplR8_f1CIorJd8_BwejTfFrcZKF6Rzc89k
```
Respone:
```json
{
    "@event": "GENERIC_ERROR_OCCURRED",
    "@type": "error",
    "errors": [
        "'WSGIRequest' object has no attribute 'query'"
    ],
    "user_id": "anonymous"
}
```
### CREATE_CATALOGUEITEM: POST /catalogue/items/
Create Catalogue Item 
None
#### 201 (CATALOGUEITEM_CREATED)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjcsImVtYWlsIjoieGRpYmJlcnRAd2VpbWFubi5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.9ON72s-VaJ8MNQJkUtOoWjV9dz2_iKFqANFT8RwglBI
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 28,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ]
}
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_CREATED",
    "@type": "catalogue_item",
    "created_by": {
        "@type": "account",
        "email": "xdibbert@weimann.com",
        "id": 27,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "oharahouston@yahoo.com",
        "id": 28,
        "type": "RESEARCHER"
    },
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ],
    "updated_by": {
        "@type": "account",
        "email": "xdibbert@weimann.com",
        "id": 27,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjksImVtYWlsIjoiYmFydG9uZ2VvcmdpYW5hQGJydWVuLWtsaW5nLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MTcyMH0.VkVKyRNs7_K1nL8TISaPEmHsRtVn-nPi8z-ED62CFqw
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 30,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203
        }
    ]
}
```
Respone:
```json
{
    "@event": "BODY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "spec": [
            "JSON did not validate. PATH: '0' REASON: 'type' is a required property"
        ]
    },
    "user_id": "anonymous"
}
```
#### 400 (BODY_JSON_DID_NOT_PARSE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzEsImVtYWlsIjoibXVyYXppa2RhbHZpbkByb3dlLmJpeiIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MTcyMH0.y4YiDoqlVbMa9hPISX0fbS1cfnP-XOkwAbqQEPGoSoM
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 932039,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ]
}
```
Respone:
```json
{
    "@event": "BODY_JSON_DID_NOT_PARSE",
    "@type": "error",
    "errors": {
        "maintained_by": [
            "account instance with id 932039 does not exist."
        ]
    },
    "user_id": "anonymous"
}
```
#### 401 (COULD_NOT_FIND_AUTH_TOKEN)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJjb25uYWxiYUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjU4NzA5MX0.8h1V65YUtFreRoUfsuh-A7qYeLz8aj-WWZ4NElUMw6M
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 2,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ]
}
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_AUTH_TOKEN",
    "@type": "error",
    "user_id": null
}
```
#### 500 (GENERIC_ERROR_OCCURRED)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJvZGFsaXM2OEBnbWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI1ODcxMTV9.64emZl6jiE8XqWpR8L0YP4C4APEiiLt4HQvIOg7s1y0
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 2,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ]
}
```
Respone:
```json
{
    "@event": "GENERIC_ERROR_OCCURRED",
    "@type": "error",
    "errors": [
        "byte indices must be integers or slices, not str"
    ],
    "user_id": "anonymous"
}
```
### DELETE_CATALOGUEITEM: DELETE /catalogue/items/{item_id}
Delete Catalogue Item 
None
#### 200 (CATALOGUEITEM_DELETED)
Request:
```http
DELETE /catalogue/items/13 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzIsImVtYWlsIjoiZXJpY2gyN0BsYWtpbi5uZXQiLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.EzGz_OFm1jFTbbV1YrPx3PRGtkfJLIwtrYQWsF7eBF0
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_DELETED",
    "@type": "empty"
}
```
#### 400 (NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED)
Request:
```http
DELETE /catalogue/items/15 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzMsImVtYWlsIjoiYWxpdmlhdHJvbXBAbWNsYXVnaGxpbi5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.RNb6JPJUI5e8F8mgWKSJyN381QzzpbkNqeanTin9cvc
```
Respone:
```json
{
    "@event": "NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED",
    "@type": "error",
    "item_id": 15,
    "not_cancelled_count": 1,
    "user_id": null
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
DELETE /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImVtYWlsIjoicm9taWUzNUB5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.kir7wXjRaTIBSfYZwO2avGr_rR4bpQCfMTd-lPY0sMw
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error",
    "user_id": "anonymous"
}
```
### READ_CATALOGUEITEM: GET /catalogue/items/{item_id}
Read Catalogue Item 
None
#### 200 (CATALOGUEITEM_READ)
Request:
```http
GET /catalogue/items/17 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzUsImVtYWlsIjoiZW1taWV0b3duZUB5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.-prbUcg1tuj-T4_nDeR928ogvMCiMm0qXnXmiYR2b9k
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_READ",
    "@type": "catalogue_item",
    "created_by": null,
    "executor_type": "DATABRICKS",
    "maintained_by": null,
    "name": "temperatures",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "location",
            "size": 190234,
            "type": "STRING"
        },
        {
            "distribution": [
                {
                    "count": 9,
                    "value": 18.0
                },
                {
                    "count": 45,
                    "value": 19.1
                },
                {
                    "count": 10,
                    "value": 21.2
                }
            ],
            "is_nullable": true,
            "name": "value",
            "size": null,
            "type": "FLOAT"
        }
    ],
    "updated_by": null
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
GET /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzYsImVtYWlsIjoic3lkbmVlNDRAZ21haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxNzIwfQ.YfY-hSNnSMZunGbgAvqCz0KfkLrgYIn1KUSr5UHfQBE
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error",
    "user_id": "anonymous"
}
```
### UPDATE_CATALOGUEITEM: PUT /catalogue/items/{item_id}
Update Catalogue Item 
None
#### 200 (CATALOGUEITEM_UPDATED)
Request:
```http
PUT /catalogue/items/19 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImVtYWlsIjoianVkZDUyQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxNzIwfQ.ym0qFPgGiGa4925wVtaBCYz62oRaAe6dZzQv6VoMfDQ
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 38,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ]
}
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_UPDATED",
    "@type": "catalogue_item",
    "created_by": {
        "@type": "account",
        "email": "goodwinkevin@gmail.com",
        "id": 39,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "tbosco@swaniawski.com",
        "id": 38,
        "type": "RESEARCHER"
    },
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ],
    "updated_by": {
        "@type": "account",
        "email": "judd52@hotmail.com",
        "id": 37,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/20 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDAsImVtYWlsIjoiYnJpdG5leTYxQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxNzIwfQ.eEbTcz5QyOkeuqCxeowlJMFguNUm-Qt0D8HuXTANwyA
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 41,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203
        }
    ]
}
```
Respone:
```json
{
    "@event": "BODY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "spec": [
            "JSON did not validate. PATH: '0' REASON: 'type' is a required property"
        ]
    },
    "user_id": "anonymous"
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
PUT /catalogue/items/9022 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDIsImVtYWlsIjoibWFyZ2FyZXQ5MkBtZWRodXJzdC1ib2dpc2ljaC5iaXoiLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9._sKUc-Ma3tsCMMz5R06V3pCdjbMsX89VAwWK_w-jZ1E
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 43,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ]
}
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error",
    "user_id": "anonymous"
}
```
## Docs Management
## Download Requests Management
### BULK_READ_DOWNLOADREQUESTS: GET /downloader/requests/
Bulk Read Download Requests which you are waiting for 
None
#### 200 (DOWNLOADREQUESTS_BULK_READ)
Request:
```http
GET /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTgsImVtYWlsIjoicmFsZWlnaGhpbHBlcnRAaGFtbWVzLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MTcyMH0.qwfuWGCNRd1rhUEjpTt8LGlPAZ692fVf2OZbssJWjT4
```
Respone:
```json
{
    "@event": "DOWNLOADREQUESTS_BULK_READ",
    "@type": "download_requests_list",
    "requests": [
        {
            "@type": "download_request",
            "catalogue_item": {
                "@type": "catalogue_item",
                "created_by": null,
                "executor_type": "ATHENA",
                "maintained_by": null,
                "name": "Dian Flatley",
                "sample": [],
                "spec": [
                    {
                        "distribution": null,
                        "is_nullable": true,
                        "name": "product",
                        "size": null,
                        "type": "STRING"
                    },
                    {
                        "distribution": null,
                        "is_nullable": false,
                        "name": "price",
                        "size": null,
                        "type": "INTEGER"
                    }
                ],
                "updated_by": null
            },
            "created_by": {
                "@type": "account",
                "email": "bednarmarc@lehner-graham.net",
                "id": 59,
                "type": "RESEARCHER"
            },
            "estimated_size": null,
            "executor_job_id": null,
            "is_cancelled": false,
            "real_size": null,
            "spec": {
                "columns": [
                    "product"
                ],
                "filters": [
                    {
                        "name": "price",
                        "operator": ">=",
                        "value": 78
                    }
                ],
                "randomize_ratio": 1
            },
            "uri": null
        },
        {
            "@type": "download_request",
            "catalogue_item": {
                "@type": "catalogue_item",
                "created_by": null,
                "executor_type": "ATHENA",
                "maintained_by": null,
                "name": "Dian Flatley",
                "sample": [],
                "spec": [
                    {
                        "distribution": null,
                        "is_nullable": true,
                        "name": "product",
                        "size": null,
                        "type": "STRING"
                    },
                    {
                        "distribution": null,
                        "is_nullable": false,
                        "name": "price",
                        "size": null,
                        "type": "INTEGER"
                    }
                ],
                "updated_by": null
            },
            "created_by": {
                "@type": "account",
                "email": "bednarmarc@lehner-graham.net",
                "id": 59,
                "type": "RESEARCHER"
            },
            "estimated_size": null,
            "executor_job_id": null,
            "is_cancelled": false,
            "real_size": null,
            "spec": {
                "columns": [
                    "product"
                ],
                "filters": [
                    {
                        "name": "price",
                        "operator": "=",
                        "value": 18
                    }
                ],
                "randomize_ratio": 0.8
            },
            "uri": null
        }
    ]
}
```
### CREATE_DOWNLOADREQUEST: POST /downloader/requests/
Create Download Request 
Create a Download Request in a smart way meaning that: - if same `DownloadRequest` already exists do not start another one. (FIXME: maybe just attach user to the waiters list) -
#### 201 (DOWNLOADREQUEST_CREATED)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjAsImVtYWlsIjoiYmVlcm9kaWVAZ21haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxNzIwfQ.WDhpVJyZYURxfmeW_zpPAl4DMtPcTikyKZrrYVeWl-s
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 35,
    "spec": {
        "columns": [
            "product",
            "price"
        ],
        "filters": [],
        "randomize_ratio": 0.9
    }
}
```
Respone:
```json
{
    "@event": "DOWNLOADREQUEST_CREATED",
    "@type": "download_request",
    "catalogue_item": {
        "@type": "catalogue_item",
        "created_by": null,
        "executor_type": "DATABRICKS",
        "maintained_by": null,
        "name": "Dr. Joselyn Franecki PhD",
        "sample": [],
        "spec": [
            {
                "distribution": null,
                "is_nullable": true,
                "name": "product",
                "size": null,
                "type": "STRING"
            },
            {
                "distribution": null,
                "is_nullable": false,
                "name": "price",
                "size": null,
                "type": "INTEGER"
            }
        ],
        "updated_by": null
    },
    "created_by": {
        "@type": "account",
        "email": "beerodie@gmail.com",
        "id": 60,
        "type": "ADMIN"
    },
    "estimated_size": null,
    "executor_job_id": null,
    "is_cancelled": false,
    "real_size": null,
    "spec": {
        "columns": [
            "product",
            "price"
        ],
        "filters": [],
        "randomize_ratio": 0.9
    },
    "uri": null
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjIsImVtYWlsIjoibWNjbHVyZW9saWVAa3VwaGFsLm5ldCIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MTcyMH0.kZ7WULBQkWHW9AHV3B-DVJ2VgcUZrke9P1Zg9tuJDFw
CONTENT-TYPE: application/json
{
    "catalogue_item_id": "TEXT",
    "spec": {
        "columns": [
            "product",
            "price"
        ],
        "filters": [],
        "randomize_ratio": 0.9
    }
}
```
Respone:
```json
{
    "@event": "BODY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "catalogue_item_id": [
            "A valid integer is required."
        ]
    },
    "user_id": "anonymous"
}
```
#### 400 (BODY_JSON_DID_NOT_PARSE)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJncHJvc2FjY29AeWFob28uY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxMTI4fQ.OwHSOxfgL2PUwF2PKTq23kHJMhN0CauHxf9TJQoKLVI
```
Respone:
```json
{
    "@event": "BODY_JSON_DID_NOT_PARSE",
    "@type": "error",
    "user_id": "anonymous"
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjQsImVtYWlsIjoiZGVzaTI2QGR1cmdhbi5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.ex5AenL742InLgklhOBh9-bSj7qvC9bfmaDVJ5c9aXU
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 58495,
    "spec": {
        "columns": [
            "product",
            "price"
        ],
        "filters": [],
        "randomize_ratio": 0.9
    }
}
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error",
    "user_id": "anonymous"
}
```
#### 500 (GENERIC_ERROR_OCCURRED)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJsYXNodW5kYW1hbm5AZ21haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYwNDg3fQ.zVzUYolXI7xc_GzK9_X0p6pe85NMAOE0G7pVnGIpenk
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 3,
    "spec": {
        "columns": [
            "product",
            "price"
        ],
        "filters": [],
        "randomize_ratio": 0.9
    }
}
```
Respone:
```json
{
    "@event": "GENERIC_ERROR_OCCURRED",
    "@type": "error",
    "errors": [
        "'WSGIRequest' object has no attribute 'access'"
    ],
    "user_id": "anonymous"
}
```
### DELETE_DOWNLOADREQUEST: DELETE /downloader/requests/{request_id}
Creator can cancel request or remove himself from waiters 
None
#### 200 (DOWNLOADREQUEST_DELETED)
Request:
```http
DELETE /downloader/requests/11 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjUsImVtYWlsIjoib2xzb25vcmFuZ2VAeWFob28uY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxNzIwfQ.S9CH7DRLHsfQ3nVyG6q0kJv6WSH01mLJJBG0O8la2to
```
Respone:
```json
{
    "@event": "DOWNLOADREQUEST_DELETED",
    "@type": "empty"
}
```
#### 404 (COULD_NOT_FIND_DOWNLOADREQUEST)
Request:
```http
DELETE /downloader/requests/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjcsImVtYWlsIjoia3N0ZXViZXJAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.z85H4W6VlV055elZF2guyGpeJsm_Z7brLohLqPQiSp4
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_DOWNLOADREQUEST",
    "@type": "error",
    "user_id": "anonymous"
}
```
### ESTIMATE_SIZE_OF_DOWNLOAD_REQUEST: POST /downloader/requests/estimate/
Estimate the size download based on the provided spec 
None
#### 200 (SIZE_OF_DOWNLOAD_REQUEST_ESTIMATED)
Request:
```http
POST /downloader/requests/estimate/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTcsImVtYWlsIjoicm9iYjczQHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MTcyMH0.1n7SRaF49CEZQFKKUJpW6gA9pPRM5xdU_-8taa7KIUY
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 33,
    "spec": {
        "columns": [
            "product",
            "price"
        ],
        "filters": [],
        "randomize_ratio": 0.9
    }
}
```
Respone:
```json
{
    "@event": "SIZE_OF_DOWNLOAD_REQUEST_ESTIMATED",
    "@type": "download_request_estimated_size",
    "estimated_size": 1234
}
```
### READ_DOWNLOADREQUEST: GET /downloader/requests/{request_id}
Read DownloadRequest one is waiting for 
None
#### 200 (DOWNLOADREQUEST_READ)
Request:
```http
GET /downloader/requests/12 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjgsImVtYWlsIjoiaXNpc2tvdmFjZWtAZ21haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxNzIwfQ.IV6xFy_Oz5FhLGzc8lMQw2cUWb4Yz_t80eLiejFAb_8
```
Respone:
```json
{
    "@event": "DOWNLOADREQUEST_READ",
    "@type": "download_request",
    "catalogue_item": {
        "@type": "catalogue_item",
        "created_by": null,
        "executor_type": "DATABRICKS",
        "maintained_by": null,
        "name": "Chin Connelly",
        "sample": [],
        "spec": [
            {
                "distribution": null,
                "is_nullable": true,
                "name": "product",
                "size": null,
                "type": "STRING"
            },
            {
                "distribution": null,
                "is_nullable": false,
                "name": "price",
                "size": null,
                "type": "INTEGER"
            }
        ],
        "updated_by": null
    },
    "created_by": {
        "@type": "account",
        "email": "stehrmittie@kutch.info",
        "id": 69,
        "type": "RESEARCHER"
    },
    "estimated_size": null,
    "executor_job_id": null,
    "is_cancelled": false,
    "real_size": null,
    "spec": {
        "columns": [
            "product"
        ],
        "filters": [
            {
                "name": "price",
                "operator": ">=",
                "value": 78
            }
        ],
        "randomize_ratio": 1
    },
    "uri": null
}
```
#### 404 (COULD_NOT_FIND_DOWNLOADREQUEST)
Request:
```http
GET /downloader/requests/13 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzEsImVtYWlsIjoic3BvcmVyanVkeUBnbWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjE3MjB9.OH0-kphoeDxzhoXdFO738gBnBC6J3C6Rl8J0goxJVNU
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_DOWNLOADREQUEST",
    "@type": "error",
    "user_id": "anonymous"
}
```
### RENDER_DOWNLOAD_REQUEST_UI_DATA: POST /downloader/requests/render_ui_data/
Render data needed for the built up of the download request form on client side 
None
#### 200 (DOWNLOAD_REQUEST_UI_DATA_RENDERED)
Request:
```http
POST /downloader/requests/render_ui_data/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTYsImVtYWlsIjoieXZldHRlYnJla2tlQHF1aWdsZXkuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYxNzIwfQ.yHym5d9gzpWCcdeMhANUSb3VyMliA268qj59t6hS9pI
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 32
}
```
Respone:
```json
{
    "@event": "DOWNLOAD_REQUEST_UI_DATA_RENDERED",
    "@type": "download_request_render",
    "columns_operators": [
        {
            "@type": "column_operators",
            "name": "product",
            "operators": [
                ">",
                ">=",
                "<",
                "<=",
                "=",
                "!="
            ]
        },
        {
            "@type": "column_operators",
            "name": "price",
            "operators": [
                ">",
                ">=",
                "<",
                "<=",
                "=",
                "!="
            ]
        },
        {
            "@type": "column_operators",
            "name": "available",
            "operators": [
                "=",
                "!="
            ]
        }
    ]
}
```
#### 500 (GENERIC_ERROR_OCCURRED)
Request:
```http
POST /downloader/requests/render/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MSwiZW1haWwiOiJtdXJwaHlpc2lkcm9AbWVkaHVyc3QuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjU5MTc0fQ.VLiGxYMzQPYcAF6lHYi9KbYjxHq7DwFKUjau8DHo32Q
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 1
}
```
Respone:
```json
{
    "@event": "GENERIC_ERROR_OCCURRED",
    "@type": "error",
    "errors": [
        "byte indices must be integers or slices, not str"
    ],
    "user_id": "anonymous"
}
```
