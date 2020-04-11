
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
    "request_uuid": "88ba07dc-7bf0-11ea-83d0-4485007e7d04"
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
            "Must be a valid UUID."
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
    "request_uuid": "88ba07dd-7bf0-11ea-83d0-4485007e7d04"
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
    "authenticate_ui_uri": "/accounts/auth_requests/88ba07db-7bf0-11ea-83d0-4485007e7d04/authenticate/ui/",
    "request_uuid": "88ba07db-7bf0-11ea-83d0-4485007e7d04"
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
    "request_uuid": "88ba07da-7bf0-11ea-83d0-4485007e7d04"
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
    "request_uuid": "f5e7e000-5074-11e4-9515-507b9deb8705"
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzYsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.5XxK6iQxnhbTsdtaO94F_x5C-_0ol6_eBpNljNLpHpQ
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
            "executor_type": "ATHENA",
            "id": 32,
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
            "executor_type": "DATABRICKS",
            "id": 34,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjksImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.E6fws4k6li8M28AQhDA4mRfFRpsAwY3tn6bzgKyRkHs
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 30,
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
        "email": "gerardwiegand@hotmail.com",
        "id": 29,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "id": 19,
    "maintained_by": {
        "@type": "account",
        "email": "trinidadhuel@yahoo.com",
        "id": 30,
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
        "email": "gerardwiegand@hotmail.com",
        "id": 29,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjYsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.k5SCQVoo3ECScMucwl_bSOONbt_i8qhgg1ZK-6CaDLw
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 27,
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
    "@authorizer": {
        "account_id": 26
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzIsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.lGrOoReOgsZqxv08Ipnp9eu2D6vo1w4Q6CPdVtNeRi0
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
    "@authorizer": {
        "account_id": 32
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
DELETE /catalogue/items/35 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.jdwBAV5MGn3_6m2YT8n5vnvNk_tC-ndr-1aF8fLWJws
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
DELETE /catalogue/items/41 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDcsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.ztCRa7v-F9fCt3XplljqBhc038-rt6gb0Ecl0_YCmsU
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 47
    },
    "@event": "NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED",
    "@type": "error",
    "item_id": 41,
    "not_cancelled_count": 1
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
DELETE /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzgsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.7IvMoE7VmagxAifgBe9M02N28vM-hfG6VG_GUY2RFto
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 38
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
GET /catalogue/items/37 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzksImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.iZFE2daIrmF6CurVC7oDqodL_z9N7gnFBMzw74XjeMs
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_READ",
    "@type": "catalogue_item",
    "created_by": null,
    "executor_type": "ATHENA",
    "id": 37,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDgsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2M30.2Vz8H8fmnf2S_Lp-4gbwcXzpGBuXBwuGabq2jnL9Tfk
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 48
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
PUT /catalogue/items/39 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDAsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.djTKEc7l_sLOCvQC8HFYDuwF2Uc9cWxGz-zFNCmo5cQ
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 41,
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
        "email": "heaneyzelda@yundt.com",
        "id": 42,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "id": 39,
    "maintained_by": {
        "@type": "account",
        "email": "trinidadhuel@yahoo.com",
        "id": 41,
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
        "email": "gerardwiegand@hotmail.com",
        "id": 40,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/40 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDMsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.ky54LzCXJ_86ASJvctdJUlN5ISAqdIgGwWfSfj36p6Q
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 44,
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
    "@authorizer": {
        "account_id": 43
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDUsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2Mn0.WvHizcPYeM9eKe45lhf1SZB80C__L7wBbKLMU1NkuBQ
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 46,
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
    "@authorizer": {
        "account_id": 45
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
PUT /catalogue/items/43/samples_and_distributions/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTAsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2M30.0xaABGczD4EWqNn8cgqA3caMupw6xv920EghjjUAW_c
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDksImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2M30.J3IrmcdC_gKLg3sIETKIuBKxH_xxdx2SQxAa4WURReA
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 49
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZW1haWwiOiJnZXJhcmR3aWVnYW5kQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2Njk0NzYwfQ.4-ebQdsO7eLF2mgFfE5CD9fh6wdcAO_vkfMI-eXgKU4
```
Respone:
```json
{
    "@event": "DOWNLOADREQUESTS_BULK_READ",
    "@type": "download_requests_list",
    "requests": [
        {
            "@type": "download_request",
            "blob_name": null,
            "catalogue_item": {
                "@type": "catalogue_item",
                "created_by": null,
                "executor_type": "ATHENA",
                "id": 2,
                "maintained_by": null,
                "name": "Denice Jacobi",
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
                "email": "keely20@yahoo.com",
                "id": 6,
                "type": "RESEARCHER"
            },
            "download_uri": null,
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
            }
        },
        {
            "@type": "download_request",
            "blob_name": null,
            "catalogue_item": {
                "@type": "catalogue_item",
                "created_by": null,
                "executor_type": "ATHENA",
                "id": 2,
                "maintained_by": null,
                "name": "Denice Jacobi",
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
                "email": "keely20@yahoo.com",
                "id": 6,
                "type": "RESEARCHER"
            },
            "download_uri": null,
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
            }
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
DELETE /downloader/requests/7 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTUsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2MX0.TYNKo2K3NmMmM_uibTm5AMdpwTzQAPk1kYoJMkm347U
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTIsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2MX0.f_wuijgv7wvJAXvuIkwJlvyed1hhHm2WEatsubijWVI
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 12
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTAsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2MX0.iuGDOZfqZlMHmuOJt3bppiZKKKDnkABQjejAsgMWDjk
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 6,
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
GET /downloader/requests/8 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTcsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2MX0.ksP_1HNADv6TiPX5icLkqNvgl8bIgpSZpLrv4MiD54U
```
Respone:
```json
{
    "@event": "DOWNLOADREQUEST_READ",
    "@type": "download_request",
    "blob_name": null,
    "catalogue_item": {
        "@type": "catalogue_item",
        "created_by": null,
        "executor_type": "ATHENA",
        "id": 11,
        "maintained_by": null,
        "name": "Denice Jacobi",
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
        "email": "keely20@yahoo.com",
        "id": 18,
        "type": "RESEARCHER"
    },
    "download_uri": null,
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
    }
}
```
#### 404 (COULD_NOT_FIND_DOWNLOADREQUEST)
Request:
```http
GET /downloader/requests/6 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTMsImVtYWlsIjoiZ2VyYXJkd2llZ2FuZEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjY5NDc2MX0.A9I7uxFOzPyXHiaaLBXvpyRtLJCxm4Vx0j0oCLHqevM
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 13
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwiZW1haWwiOiJnZXJhcmR3aWVnYW5kQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2Njk0NzYwfQ.L_jbtNTA0t-NBxCrrrI6SR64GYO8IXBwl8ZtkZcON_U
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 1,
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
    "blob_name": "https://s3.this.region.amazonaws.com/buk.et/results/567.csv",
    "catalogue_item": {
        "@type": "catalogue_item",
        "created_by": null,
        "executor_type": "ATHENA",
        "id": 1,
        "maintained_by": null,
        "name": "Denice Jacobi",
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
    }
}
```
#### 201 (DOWNLOADREQUEST_CREATED)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZW1haWwiOiJnZXJhcmR3aWVnYW5kQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2Njk0NzYwfQ.own2ZaIfezhUYB7VwGpUcdoBC0PPHvUOWkNeVh2E658
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
    "@event": "DOWNLOADREQUEST_CREATED",
    "@type": "download_request",
    "blob_name": "https://s3.this.region.amazonaws.com/buk.et/results/567.csv",
    "catalogue_item": {
        "@type": "catalogue_item",
        "created_by": null,
        "executor_type": "ATHENA",
        "id": 3,
        "maintained_by": null,
        "name": "Denice Jacobi",
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
        "email": "gerardwiegand@hotmail.com",
        "id": 7,
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
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OCwiZW1haWwiOiJnZXJhcmR3aWVnYW5kQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2Njk0NzYwfQ.NwiZnr-l52HHNdneR6QirIkc5Lhk2C3GGEs3mL2KN-0
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
    "@authorizer": {
        "account_id": 8
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
#### 400 (BODY_JSON_DID_NOT_PARSE)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OSwiZW1haWwiOiJnZXJhcmR3aWVnYW5kQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2Njk0NzYwfQ.xjtqiOo2ZUue0JBoKoCwDm9K0D4qMInMu7XOP2nNQWQ
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
    "@authorizer": {
        "account_id": 9
    },
    "@event": "BODY_JSON_DID_NOT_PARSE",
    "@type": "error",
    "errors": {
        "catalogue_item": [
            "catalogue item instance with id 58495 does not exist."
        ]
    }
}
```
