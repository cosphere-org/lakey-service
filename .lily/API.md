
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
    "email": "jacky@somewhere.org",
    "oauth_token": "some-oauth-token",
    "request_uuid": "e07faa11-6b16-11e9-aee9-34f64bbaddd0"
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
        "oauth_token": [
            "This field is required."
        ],
        "request_uuid": [
            "\"some-uuid\" is not a valid UUID."
        ]
    }
}
```
#### 404 (COULD_NOT_FIND_AUTHREQUEST)
Request:
```http
POST /accounts/auth_requests/attach_account/ HTTP/1.1
CONTENT-TYPE: application/json
{
    "email": "jacky@somewhere.org",
    "oauth_token": "some-auth-token",
    "request_uuid": "e07faa12-6b16-11e9-aee9-34f64bbaddd0"
}
```
Respone:
```json
{
    "@event": "COULD_NOT_FIND_AUTHREQUEST",
    "@type": "error"
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
    "authenticate_ui_uri": "/accounts/auth_requests/e07faa10-6b16-11e9-aee9-34f64bbaddd0/authenticate/ui/",
    "request_uuid": "e07faa10-6b16-11e9-aee9-34f64bbaddd0"
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
    "request_uuid": "e07faa13-6b16-11e9-aee9-34f64bbaddd0"
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
    "request_uuid": "f5e7e000-5074-11e4-8ada-024247a0384a"
}
```
Respone:
```json
{
    "@event": "EXPIRED_AUTH_REQUEST_DETECTED",
    "@type": "error"
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
"<!DOCTYPE html>\n<html>\n    <head>\n        <title>Lakey Authentication</title>\n        <meta\n            name=\"google-signin-client_id\"\n            content=\"961918528927-12heq0l9f1tep1igb29tatkf2pr2p5f7.apps.googleusercontent.com\">\n\n        <link\n            href=\"https://fonts.googleapis.com/css?family=IBM+Plex+Sans\"\n            rel=\"stylesheet\">\n        <style>\n            body {\n                background: #e4e4e4;\n            }\n\n            #main {\n                height: 200px;\n                width: 100%;\n                font-family: 'IBM Plex Sans', sans-serif;\n            }\n\n            h2 {\n                font-weight: normal;\n            }\n\n            #authenticate, #done, #wait {\n                display: flex;\n                flex-direction: column;\n                align-items: center;\n                justify-content: center;\n            }\n\n            #done, #wait {\n                display: none;\n            }\n        </style>\n        <script\n            type=\"text/javascript\">\n\n\n            function renderButton() {\n                gapi.signin2.render('google-auth-button', {\n                    'scope': 'profile email',\n                    'width': 240,\n                    'height': 50,\n                    'longtitle': true,\n                    'theme': 'dark',\n                    'onsuccess': onSuccess,\n                    'onfailure': onFailure\n              });\n            }\n\n            function onSuccess(googleUser) {\n                let $done = document.getElementById('done');\n                let $wait = document.getElementById('wait');\n                let $authenticate = document.getElementById('authenticate');\n\n                let authRequestUUID = 'some-uuid';\n                let profile = googleUser.getBasicProfile();\n\n                let xhr = new XMLHttpRequest();\n                xhr.open(\n                    'POST',\n                    '/accounts/auth_requests/attach_account/');\n\n                xhr.setRequestHeader(\n                    \"Content-Type\", \"application/json;charset=UTF-8\");\n\n                xhr.send(\n                    JSON.stringify({\n                        request_uuid: authRequestUUID,\n                        oauth_token: googleUser.getAuthResponse().id_token,\n                        email: profile.getEmail(),\n                    })\n                );\n\n                // -- hide AUTHENTICATE view and show WAIT view\n                $authenticate.style['display'] = 'none';\n                $wait.style['display'] = 'flex';\n\n                xhr.onload = () => {\n                    // -- hide WAIT view and show DONE view\n                    $wait.style['display'] = 'none';\n                    $done.style['display'] = 'flex';\n                };\n            }\n\n            function onFailure(error) {\n                console.error(error);\n            }\n\n        </script>\n        <script\n            src=\"https://apis.google.com/js/platform.js?onload=renderButton\"\n            async\n            defer>\n        </script>\n    </head>\n\n    <body>\n\n        <div\n            id=\"main\">\n            <div\n                id=\"authenticate\">\n\n                <h2>Sign In To Lakey</h2>\n                <div\n                    id=\"google-auth-button\"></div>\n            </div>\n\n            <div\n                id=\"wait\">\n\n                PLEASE WAIT ...\n            </div>\n\n            <div\n                id=\"done\">\n\n                DONE, PLEASE RUN AGAIN CODE THAT GOT YOU HERE.\n            </div>\n\n        </div>\n    </body>\n\n</html>\n"
```
## Catalogue Items Management
### BULK_READ_CATALOGUEITEMS: GET /catalogue/items/
Bulk Read Catalogue Items 
None
#### 200 (CATALOGUEITEMS_BULK_READ)
Request:
```http
GET /catalogue/items/?query=IOT+%7Efeatures+%7C+temp HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzgsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.nAy2uoutLgukeq4vnEJ-QjkyMnw8YThkvlDj6l8Qfjk
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
            "id": 69,
            "maintained_by": null,
            "name": "temperatures",
            "sample": [],
            "spec": [
                {
                    "distribution": null,
                    "is_enum": false,
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
                    "is_enum": false,
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
            "id": 70,
            "maintained_by": null,
            "name": "iot_events",
            "sample": [],
            "spec": [
                {
                    "distribution": null,
                    "is_enum": false,
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
                    "is_enum": false,
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
### CREATE_CATALOGUEITEM: POST /catalogue/items/
Create Catalogue Item 
None
#### 201 (CATALOGUEITEM_CREATED)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzQsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.TD40Ha80HiX4OQFIgqApDs3hcCum2-9TDf13j2Qz96g
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 75,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
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
        "email": "charlanolan@oreilly-adams.com",
        "id": 74,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "id": 61,
    "maintained_by": {
        "@type": "account",
        "email": "finneganwaelchi@rowe.com",
        "id": 75,
        "type": "RESEARCHER"
    },
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ],
    "updated_by": {
        "@type": "account",
        "email": "charlanolan@oreilly-adams.com",
        "id": 74,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzIsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.cerwGk1XLVfbKvEoYrnTwhUMy3MXevGDfPAdwgvMhWY
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 73,
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
    "@access": {
        "account_id": 72
    },
    "@event": "BODY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "spec": [
            "JSON did not validate. PATH: '0' REASON: 'type' is a required property"
        ]
    }
}
```
#### 400 (BODY_JSON_DID_NOT_PARSE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzEsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.aSHP7rByKZYlVzrusKVx05iy-uaUQ8OBMGuwgxU-dq4
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 932039,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
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
    "@access": {
        "account_id": 71
    },
    "@event": "BODY_JSON_DID_NOT_PARSE",
    "@type": "error",
    "errors": {
        "maintained_by": [
            "account instance with id 932039 does not exist."
        ]
    }
}
```
### DELETE_CATALOGUEITEM: DELETE /catalogue/items/{item_id}
Delete Catalogue Item 
None
#### 200 (CATALOGUEITEM_DELETED)
Request:
```http
DELETE /catalogue/items/71 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODAsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.2YmM0N7D2MEsjtxUOJOR8dfbMjKVJH9SAYRHr3iZ1MI
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
DELETE /catalogue/items/77 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODgsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.UYWhszx6urFdGZNg8nwIxvvW2Z-mCRNzpuNa2aAVflU
```
Respone:
```json
{
    "@access": {
        "account_id": 88
    },
    "@event": "NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED",
    "@type": "error",
    "item_id": 77,
    "not_cancelled_count": 1
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
DELETE /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODcsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.0n3S1Mja0TIUkcs9L-HSqjr1DJBJv5C9tj7z96EQjiA
```
Respone:
```json
{
    "@access": {
        "account_id": 87
    },
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error"
}
```
### READ_CATALOGUEITEM: GET /catalogue/items/{item_id}
Read Catalogue Item 
None
#### 200 (CATALOGUEITEM_READ)
Request:
```http
GET /catalogue/items/74 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODQsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.qy1S00c-_iMrT8do109oCpVkgzfvCOja5S0TtJ4uaIo
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_READ",
    "@type": "catalogue_item",
    "created_by": null,
    "executor_type": "DATABRICKS",
    "id": 74,
    "maintained_by": null,
    "name": "temperatures",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
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
            "is_enum": false,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzksImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.rB47tYlZgemkr23r-n9Sig0XNgxqQp9HgzH22dqD2zU
```
Respone:
```json
{
    "@access": {
        "account_id": 79
    },
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error"
}
```
### UPDATE_CATALOGUEITEM: PUT /catalogue/items/{item_id}
Update Catalogue Item 
None
#### 200 (CATALOGUEITEM_UPDATED)
Request:
```http
PUT /catalogue/items/73 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODEsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.EiuirfOxL5vKDZVcCYMFfFQ5U6RWLePTX3-Zry6SGpY
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 82,
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
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
        "email": "ochamplin@hotmail.com",
        "id": 83,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "id": 73,
    "maintained_by": {
        "@type": "account",
        "email": "finneganwaelchi@rowe.com",
        "id": 82,
        "type": "RESEARCHER"
    },
    "name": "temperatures",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
            "is_nullable": false,
            "name": "value",
            "size": 19203,
            "type": "FLOAT"
        }
    ],
    "updated_by": {
        "@type": "account",
        "email": "charlanolan@oreilly-adams.com",
        "id": 81,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/76 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODUsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.XOaRrCZ7xrnqOHjGK_Y5jlubI1NB_HAx244tu025oLw
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 86,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
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
    "@access": {
        "account_id": 85
    },
    "@event": "BODY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "spec": [
            "JSON did not validate. PATH: '0' REASON: 'type' is a required property"
        ]
    }
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
PUT /catalogue/items/9022 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODksImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.9jz0msFYiBkysCPRou3SqVuPpbeD2DWxLfI0hj-7W1E
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 90,
    "name": "iot_events",
    "sample": [],
    "spec": [
        {
            "distribution": null,
            "is_enum": false,
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
    "@access": {
        "account_id": 89
    },
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error"
}
```
### WITH_SAMPLE_AND_DISTRIBUTION_UPDATE_CATALOGUEITEM: PUT /catalogue/items/{item_id}/samples_and_distributions/
Update Catalogue Item with Samples and Distributions 
None
#### 200 (CATALOGUEITEM_WITH_SAMPLE_AND_DISTRIBUTION_UPDATED)
Request:
```http
PUT /catalogue/items/79/samples_and_distributions/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTEsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.YjKkgqsXRlkcsRAoMQijQipNO0Yqa09hNO2Th0Cxg84
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_WITH_SAMPLE_AND_DISTRIBUTION_UPDATED",
    "@type": "empty"
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
PUT /catalogue/items/9022/samples_and_distributions/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTQsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjN9.wXEdpAHF27rexsydNbU2uIVcCdC3uLSD-Z14G1Np_4Q
```
Respone:
```json
{
    "@access": {
        "account_id": 94
    },
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error"
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjYsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.wlQfG7CXUvntRqzwxuP6iWt0ziJk_nXSzUHTHgR9ync
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
                "executor_type": "DATABRICKS",
                "id": 34,
                "maintained_by": null,
                "name": "Lindy Davis I",
                "sample": [],
                "spec": [
                    {
                        "distribution": null,
                        "is_enum": true,
                        "is_nullable": true,
                        "name": "product",
                        "size": null,
                        "type": "STRING"
                    },
                    {
                        "distribution": null,
                        "is_enum": false,
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
                "email": "bashirianjustice@yahoo.com",
                "id": 27,
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
                "executor_type": "DATABRICKS",
                "id": 34,
                "maintained_by": null,
                "name": "Lindy Davis I",
                "sample": [],
                "spec": [
                    {
                        "distribution": null,
                        "is_enum": true,
                        "is_nullable": true,
                        "name": "product",
                        "size": null,
                        "type": "STRING"
                    },
                    {
                        "distribution": null,
                        "is_enum": false,
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
                "email": "bashirianjustice@yahoo.com",
                "id": 27,
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
### DELETE_DOWNLOADREQUEST: DELETE /downloader/requests/{request_id}
Creator can cancel request or remove himself from waiters 
None
#### 200 (DOWNLOADREQUEST_DELETED)
Request:
```http
DELETE /downloader/requests/13 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.vLXbspY9MTsIoEIHdrwZl9uB71T4GbXcGb-PNlBTt24
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzAsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.Ac9wk8SgfiS_m2zk_6JdEKQPsrARjGr2Dbegd04D7XA
```
Respone:
```json
{
    "@access": {
        "account_id": 30
    },
    "@event": "COULD_NOT_FIND_DOWNLOADREQUEST",
    "@type": "error"
}
```
### ESTIMATE_SIZE_OF_DOWNLOAD_REQUEST: POST /downloader/requests/estimate/
Estimate the size download based on the provided spec 
None
#### 200 (SIZE_OF_DOWNLOAD_REQUEST_ESTIMATED)
Request:
```http
POST /downloader/requests/estimate/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjEsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjF9.mjYKcwzyA9fFZf0nc0E4yoV80vJoXraejgVKO2A4D4k
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 29,
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
GET /downloader/requests/14 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzEsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.c_779Xg_cYRmj7bVOnOXKDBrT72doPtOFs3_zz47M-w
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
        "id": 37,
        "maintained_by": null,
        "name": "Lindy Davis I",
        "sample": [],
        "spec": [
            {
                "distribution": null,
                "is_enum": true,
                "is_nullable": true,
                "name": "product",
                "size": null,
                "type": "STRING"
            },
            {
                "distribution": null,
                "is_enum": false,
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
        "email": "bashirianjustice@yahoo.com",
        "id": 32,
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
GET /downloader/requests/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzUsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.bZ2UpIFEjgzXVYLY-BQYA5fjTh7Tw6SyOlCMLkUu6Jc
```
Respone:
```json
{
    "@access": {
        "account_id": 35
    },
    "@event": "COULD_NOT_FIND_DOWNLOADREQUEST",
    "@type": "error"
}
```
### READ_OR_CREATE_DOWNLOADREQUEST: POST /downloader/requests/
Create Download Request 
Create a Download Request in a smart way meaning that: - if same `DownloadRequest` already exists do not start another one. (FIXME: maybe just attach user to the waiters list) -
#### 200 (DOWNLOADREQUEST_READ)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjIsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjF9.hjOCY_7yg-ETdwWgAdSqbf8niweQEW_7gA8t5ytYJro
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 30,
    "spec": {
        "columns": [
            "product",
            "price"
        ],
        "filters": [
            {
                "name": "product",
                "operator": "=",
                "value": "jack"
            },
            {
                "name": "price",
                "operator": "=",
                "value": 23
            },
            {
                "name": "price",
                "operator": ">=",
                "value": 78
            }
        ],
        "randomize_ratio": 0.9
    }
}
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
        "id": 30,
        "maintained_by": null,
        "name": "Lindy Davis I",
        "sample": [],
        "spec": [
            {
                "distribution": null,
                "is_enum": true,
                "is_nullable": true,
                "name": "product",
                "size": null,
                "type": "STRING"
            },
            {
                "distribution": null,
                "is_enum": false,
                "is_nullable": false,
                "name": "price",
                "size": null,
                "type": "INTEGER"
            }
        ],
        "updated_by": null
    },
    "created_by": null,
    "estimated_size": null,
    "executor_job_id": null,
    "is_cancelled": false,
    "real_size": null,
    "spec": {
        "columns": [
            "price",
            "product"
        ],
        "filters": [
            {
                "name": "price",
                "operator": ">=",
                "value": 78
            },
            {
                "name": "price",
                "operator": "=",
                "value": 23
            },
            {
                "name": "product",
                "operator": "=",
                "value": "jack"
            }
        ],
        "randomize_ratio": 0.9
    },
    "uri": "https://s3.this.region.amazonaws.com/buk.et/results/567.csv"
}
```
#### 201 (DOWNLOADREQUEST_CREATED)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjUsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.G-O4kIEmLGqKxVCUcVhEXeCnjRcKN5JJMMgc4bYtUPo
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
    "@event": "DOWNLOADREQUEST_CREATED",
    "@type": "download_request",
    "catalogue_item": {
        "@type": "catalogue_item",
        "created_by": null,
        "executor_type": "DATABRICKS",
        "id": 33,
        "maintained_by": null,
        "name": "Lindy Davis I",
        "sample": [],
        "spec": [
            {
                "distribution": null,
                "is_enum": true,
                "is_nullable": true,
                "name": "product",
                "size": null,
                "type": "STRING"
            },
            {
                "distribution": null,
                "is_enum": false,
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
        "email": "charlanolan@oreilly-adams.com",
        "id": 25,
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
    "uri": "https://s3.this.region.amazonaws.com/buk.et/results/567.csv"
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjMsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.-rVYtzCtLbxN1sy8KuiP9fpoeptMvSQuJTiY2wcLRyk
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
    "@access": {
        "account_id": 23
    },
    "@event": "BODY_DID_NOT_VALIDATE",
    "@type": "error",
    "errors": {
        "catalogue_item_id": [
            "A valid integer is required."
        ]
    }
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjQsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.W2krTHLVXhMiWJxwOsg_p6XmNqevYYSLK1JBHw_WMyw
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
    "@access": {
        "account_id": 24
    },
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error"
}
```
### RENDER_DOWNLOAD_REQUEST_UI_DATA: POST /downloader/requests/render_ui_data/
Render data needed for the built up of the download request form on client side 
None
#### 200 (DOWNLOAD_REQUEST_UI_DATA_RENDERED)
Request:
```http
POST /downloader/requests/render_ui_data/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzYsImVtYWlsIjoiY2hhcmxhbm9sYW5Ab3JlaWxseS1hZGFtcy5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY2OTQ1NjJ9.RQDWPnCX4Akon-YOxD_9MFz2S2xEfghxYMtTWR3rgWo
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 40
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
