
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
    "request_uuid": "3b2e93ab-6be3-11e9-bed6-0028f8484bd5"
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
    "request_uuid": "3b2e93ac-6be3-11e9-bed6-0028f8484bd5"
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
    "authenticate_ui_uri": "/accounts/auth_requests/3b2e93aa-6be3-11e9-bed6-0028f8484bd5/authenticate/ui/",
    "request_uuid": "3b2e93aa-6be3-11e9-bed6-0028f8484bd5"
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
    "request_uuid": "3b2e93ad-6be3-11e9-bed6-0028f8484bd5"
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
    "request_uuid": "f5e7e000-5074-11e4-82ad-0242557aae96"
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
GET /catalogue/items/?query=IoT HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjIsImVtYWlsIjoiZGV3YXluZTExQGd1c2lrb3dza2kuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMxfQ.JfHiTl9QM2YMLJ-MMDT-MafVbK8upbbyg1P7HaBbu_g
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
            "id": 16,
            "maintained_by": null,
            "name": "iot_features",
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
            "id": 18,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjMsImVtYWlsIjoianNjaHVsdHpAZ2lic29uLWhhbWlsbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY3ODIzMzF9.k549tKR9gEjvOXJezRuRLt3gTDXH3LqWm2NlyXXGrlk
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 24,
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
        "email": "jschultz@gibson-hamill.com",
        "id": 23,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "id": 19,
    "maintained_by": {
        "@type": "account",
        "email": "bernie99@jacobs.com",
        "id": 24,
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
        "email": "jschultz@gibson-hamill.com",
        "id": 23,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjUsImVtYWlsIjoiaGlyYW04MEBicmVra2UtamFjb2Jzb24uY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMxfQ.lZUfOj0TC0j2Z0GkrYLPbbHt4g6KFlAgBEL73Q0eXV0
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 26,
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
        "account_id": 25
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjcsImVtYWlsIjoiYnJhbnNvbm1hcmtzQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMxfQ.SRR080Gi9Uhsr_Ciiz2eKY8MDwXog2m5ARlrJpQ-UX4
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
        "account_id": 27
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
DELETE /catalogue/items/20 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgsImVtYWlsIjoiZWxsaW90c2Nob2VuQHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMX0.mCiPzYJW3DM4EvvnkW9S5DAq4jwCr4v3CYLVfELZOq0
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
DELETE /catalogue/items/22 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjksImVtYWlsIjoibW9udGFuYTU5QG1vaHItc3Ryb3Npbi5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY3ODIzMzF9.6wOQXNdajSYQZX0ZDB4zTP1iJS7-xSDe2GN8MLMWNWQ
```
Respone:
```json
{
    "@access": {
        "account_id": 29
    },
    "@event": "NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED",
    "@type": "error",
    "item_id": 22,
    "not_cancelled_count": 1
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
DELETE /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzAsImVtYWlsIjoiaXZhbm5hNTVAaGVyem9nLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMX0.iIqQUXdCSRqd3da7ywLOztA9-albZZ6n3y3OeGiBCEY
```
Respone:
```json
{
    "@access": {
        "account_id": 30
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
GET /catalogue/items/24 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzEsImVtYWlsIjoiaGFycm9sZDE5QG9iZXJicnVubmVyLmJpeiIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMX0.TajyiKqVMuqgTCxVPr1-DBoT1Wqw88zzlhlOwr9HDrI
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_READ",
    "@type": "catalogue_item",
    "created_by": null,
    "executor_type": "ATHENA",
    "id": 24,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzIsImVtYWlsIjoic3RyZWljaGFsdGFAbGFyc29uLWhlcm1hbm4uY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMxfQ.jsx88pI1VWyeAi9zOTZExx7-tLDUOnG1qEjbzBbRb2w
```
Respone:
```json
{
    "@access": {
        "account_id": 32
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
PUT /catalogue/items/26 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzMsImVtYWlsIjoiZXJuc2Vycm9sbGFuZEBnbWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY3ODIzMzF9.vUKwkqtq3tbwQFxNXYI7AHh4wZ18d3hAzQE30ewoyIc
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 34,
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
        "email": "heavenkunze@ernser.com",
        "id": 35,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "id": 26,
    "maintained_by": {
        "@type": "account",
        "email": "cummingsalexis@wilkinson.info",
        "id": 34,
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
        "email": "ernserrolland@gmail.com",
        "id": 33,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/27 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzYsImVtYWlsIjoiZ3VsZ293c2tpaG9iZXJ0QHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMX0.HhP90gOybj9IcS91NmSDw8_DKOTx2pwqdDmMlAb-VEs
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 37,
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
        "account_id": 36
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzgsImVtYWlsIjoidHJldXRlbGRvdHRpZUB5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY3ODIzMzF9.m9dnw17Y_Oeue_TEYuNHEF9-UPTQH-fGZ5oCkpXHYtE
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 39,
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
        "account_id": 38
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
PUT /catalogue/items/28/samples_and_distributions/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDAsImVtYWlsIjoic2ltbWllYWRhbXNAZ21haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMxfQ.faROELVb-Ik_aGXkRnrMEE7iO73DUWCHVFdC7ASDWsQ
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDMsImVtYWlsIjoib2Nvbm5AaG9tZW5pY2staHVkc29uLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMX0.jyz4fIX6_c1FCaPpu2C9SKCs8exQ-7IPLMoGRVy47jM
```
Respone:
```json
{
    "@access": {
        "account_id": 43
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjEsImVtYWlsIjoiY2dlcmxhY2hAZ21haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMxfQ.L-gxoE4AfFOOlvID-Elcg9dGls1r5E1FaOVGUKIl0iI
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
                "id": 40,
                "maintained_by": null,
                "name": "Linn Gottlieb",
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
                "email": "mazieankunding@yahoo.com",
                "id": 62,
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
                "id": 40,
                "maintained_by": null,
                "name": "Linn Gottlieb",
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
                "email": "mazieankunding@yahoo.com",
                "id": 62,
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
DELETE /downloader/requests/8 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjcsImVtYWlsIjoiYmVhaGFubGF0b25pYUB5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY3ODIzMzJ9.Ial4iOZp5UVnuIBgqCX-nbbh6go8uvxtg3EVWn4HTfM
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjksImVtYWlsIjoia2lyYTQxQGJlcmduYXVtLmJpeiIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMn0.adHU8o6DCvZlDmMGQwf_SLhQlFY3T0yBDGFO3t7hwW8
```
Respone:
```json
{
    "@access": {
        "account_id": 69
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjAsImVtYWlsIjoiYXVmZGVyaGFyY3Jpc3RlbkBzYW5mb3JkLmluZm8iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY3ODIzMzF9.f2xlxlPNEaJI-7hyyAWBZ8mZOpir3WDCgKR9B5tZHm0
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 39,
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
GET /downloader/requests/9 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzAsImVtYWlsIjoiemJlaWVyQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMyfQ.t3PJBbGyH4Ezz0XOv62WT0zh8W3ZcqY-B3FUfSIiSyM
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
        "id": 47,
        "maintained_by": null,
        "name": "Mr. Earl Ullrich",
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
        "email": "oolson@yahoo.com",
        "id": 71,
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
GET /downloader/requests/10 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzMsImVtYWlsIjoiYmVzczY0QGNvbm5lbGx5LmluZm8iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTY3ODIzMzJ9.BiIWkUVCE2jFzFtuUrpb3E-UpumcuImWjs9Gf7c0jf0
```
Respone:
```json
{
    "@access": {
        "account_id": 73
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjMsImVtYWlsIjoiZXJuc2Vybm9yYmVydG9Ad2Fsc2gtYmFocmluZ2VyLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMX0.vyNUah0TPBWdBdTgLikqolry3DZZwCm7mIj6MhlnDc4
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 41,
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
        "executor_type": "ATHENA",
        "id": 41,
        "maintained_by": null,
        "name": "Vita Zemlak",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjQsImVtYWlsIjoiZWxsc3dvcnRobHVldHRnZW5AeWFob28uY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMyfQ.D_gJJ_bzTK42ypksxxCZJoFEVQRsMP7Tv6HBpLtzDjk
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 42,
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
        "executor_type": "ATHENA",
        "id": 42,
        "maintained_by": null,
        "name": "Toney O'Connell",
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
        "email": "ellsworthluettgen@yahoo.com",
        "id": 64,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjUsImVtYWlsIjoiYm95ZXJ3aWxtZXJAeWFob28uY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMyfQ.fA8R1OXFYJoZ99pl6toe4sMvrdA7LgpObaJFEPqmqT0
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
        "account_id": 65
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjYsImVtYWlsIjoibmh1ZWxzQHNhdWVyLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Njc4MjMzMn0.D_IPWnOXvf7ElXS3xXTuh7X3JBQXFVZ1Vu4uqFHZ7K8
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
        "account_id": 66
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTksImVtYWlsIjoiZ3JheWNlMjdAeWFob28uY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTU2NzgyMzMxfQ._VShhcvxpgl4lk2EDQG65gC0ose_9LyU03jEnN-D_wc
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 38
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
