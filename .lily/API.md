
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
    "request_uuid": "b3fff397-4974-11e9-b05d-0028f8484bd5"
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
    "request_uuid": "b3fff398-4974-11e9-b05d-0028f8484bd5"
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
    "authenticate_ui_uri": "/accounts/auth_requests/b3fff396-4974-11e9-b05d-0028f8484bd5/authenticate/ui/",
    "request_uuid": "b3fff396-4974-11e9-b05d-0028f8484bd5"
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
    "request_uuid": "b3fff399-4974-11e9-b05d-0028f8484bd5"
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
    "request_uuid": "f5e7e000-5074-11e4-9c28-02426ec57dd1"
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImVtYWlsIjoiYW5pYmFsbGFiYWRpZUBseW5jaC1saW5kZ3Jlbi5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI5OTY1MjB9.N4WOL-bF7yTKfDeVHDPrttV-5pNJihdsmyNGsSAdmrc
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
### CREATE_CATALOGUEITEM: POST /catalogue/items/
Create Catalogue Item 
None
#### 201 (CATALOGUEITEM_CREATED)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTUsImVtYWlsIjoicGdyYWR5QGt1dGNoLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.e4HQE3ZKm_UwPfU5pmWXN0LOW9i86nBeHPWjTIsAlwA
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 16,
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
        "email": "pgrady@kutch.com",
        "id": 15,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "ramon87@yahoo.com",
        "id": 16,
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
        "email": "pgrady@kutch.com",
        "id": 15,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTcsImVtYWlsIjoiY2FydHdyaWdodHRydW1hbkBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.AFoO4cGR9mWcbN2W2rEiznKBeha6QVPsPjtia19oNag
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 18,
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
        "account_id": 17
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTksImVtYWlsIjoiaGFsZXllZEB5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI5OTY1MjB9.Kc1EsIZg9N-2lN48s0MtSBKXb4WuuJmirntlMDc6vnw
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
    "@access": {
        "account_id": 19
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
DELETE /catalogue/items/8 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjAsImVtYWlsIjoidGJvZ2lzaWNoQHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.FLanN-58m1w_qrfGZXm7IbOf67bQbOKuIFsS0qs3d_o
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
DELETE /catalogue/items/10 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjEsImVtYWlsIjoiZ3JpbWVzbWFpQHN0ZWhyLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.zJWw-XBae_rJoCcf3bAgEO6gYWfxuZXcQvtRlI6PjLo
```
Respone:
```json
{
    "@event": "NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED",
    "@type": "error",
    "item_id": 10,
    "not_cancelled_count": 1
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
DELETE /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjIsImVtYWlsIjoiZGFybmVsbDI4QGtvc3MuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyOTk2NTIwfQ.b7FxWniFL4l3ANklJ3qulGp2X6_oy1whaM1RLYCcYXw
```
Respone:
```json
{
    "@access": {
        "account_id": 22
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
GET /catalogue/items/12 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjMsImVtYWlsIjoiYnJpYW5uZWhvcHBlQGdtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.MjubpMjv81Pg9S1UB5KBBvEwxFQgNM7Gpsyw--iDyP0
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_READ",
    "@type": "catalogue_item",
    "created_by": null,
    "executor_type": "ATHENA",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjQsImVtYWlsIjoiZHVidXF1ZW9ydmVsQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyOTk2NTIwfQ.HLXGIry7tXg9th4vD59-BIBhlmgxm8c8SfFSehXGHo4
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
### UPDATE_CATALOGUEITEM: PUT /catalogue/items/{item_id}
Update Catalogue Item 
None
#### 200 (CATALOGUEITEM_UPDATED)
Request:
```http
PUT /catalogue/items/14 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjUsImVtYWlsIjoiaGFsdm9yc29uYXVkcmlhbmFAc2NoYWVmZXIuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyOTk2NTIwfQ.aLCoumekExHs-lCXc36l7bRBaxGFq6FBQpvhX4E5Xmg
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
        "email": "eulalieyost@johns.com",
        "id": 27,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "framisherlyn@gmail.com",
        "id": 26,
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
        "email": "halvorsonaudriana@schaefer.com",
        "id": 25,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/15 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgsImVtYWlsIjoiZ2xlYW5ub25Acm9oYW4uYml6IiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyOTk2NTIwfQ.y2UQM1aV1N6uKO13aD_m72jwb3zXshtYE6T-WjPMNgs
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 29,
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
        "account_id": 28
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzAsImVtYWlsIjoib2t1bmV2YWp1bGlzYUBnbWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI5OTY1MjB9.25mest26zgGvETpN0wv5KT06nNrM0rqpT5PrcTydYOI
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 31,
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
    "@access": {
        "account_id": 30
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDYsImVtYWlsIjoiYXJtaWRhemVtbGFrQGdyZWVuLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.IFh9QYppsvjJ_oUGxTIqcScISJWznROxIq6TlJ5YE6Y
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
                "name": "Farris Schmitt",
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
                "email": "rossiestroman@jaskolski-herzog.org",
                "id": 47,
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
                "name": "Farris Schmitt",
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
                "email": "rossiestroman@jaskolski-herzog.org",
                "id": 47,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDgsImVtYWlsIjoidnNoaWVsZHNAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI5OTY1MjB9.tVukobqloqAqaZo_Pg9RdsRBOqhKOD3MxOvMwS7GaTU
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 24,
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
        "maintained_by": null,
        "name": "Brigitte Cole",
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
        "email": "vshields@hotmail.com",
        "id": 48,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDksImVtYWlsIjoiemVub2JpYXNpcGVzQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyOTk2NTIwfQ.B9a3W7KJPfni_oSc7rnI60hMAcAm4x5gjGKo1Cvokng
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
        "account_id": 49
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTAsImVtYWlsIjoiZ3JldGFtb3Jpc3NldHRlQGdtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.4aAdGk5dqyKX6vqL58M5eIF1CrXeera7L28D3An2Mgo
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
        "account_id": 50
    },
    "@event": "COULD_NOT_FIND_CATALOGUEITEM",
    "@type": "error"
}
```
### DELETE_DOWNLOADREQUEST: DELETE /downloader/requests/{request_id}
Creator can cancel request or remove himself from waiters 
None
#### 200 (DOWNLOADREQUEST_DELETED)
Request:
```http
DELETE /downloader/requests/7 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTEsImVtYWlsIjoiZmFiaWFuOTVAbGVobmVyLXRoaWVsLmJpeiIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.OQdYEfxG3WYHDhBV74NTUJ0Os_8QeNKBSGDRKe-plOc
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTMsImVtYWlsIjoibW1hbnRlQGxpbmQuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyOTk2NTIwfQ.7D1a_K0wJd1Mrlc3HVwqkn8la7BRzey86GAjdSlrtW4
```
Respone:
```json
{
    "@access": {
        "account_id": 53
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDUsImVtYWlsIjoiZGFtYXJpb24zMkBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.4eXk4rT-93rs6sU53w7mla5dgdibfWwJPDfSdFHlMBs
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 22,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTQsImVtYWlsIjoicGluazAwQHJpcHBpbi1ibGljay5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI5OTY1MjB9.R6dAYGQXOmXBzG7Gh7mkNqUZPwLi-I_ptGawcU8a2QM
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
        "name": "Dr. Mat Volkman II",
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
        "email": "osborn37@prohaska-lueilwitz.com",
        "id": 55,
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
GET /downloader/requests/9 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTcsImVtYWlsIjoieGhhcnJpc0BsZWFubm9uLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.u5hAEjDKp2CA5mHfSIrNUTJeBesjdRO9JORSAYOiANs
```
Respone:
```json
{
    "@access": {
        "account_id": 57
    },
    "@event": "COULD_NOT_FIND_DOWNLOADREQUEST",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDQsImVtYWlsIjoib2hhcmFzdGVwaGFpbmVAd3Vuc2NoLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1Mjk5NjUyMH0.TcDqBxqsKwmnWGy9vJQIsaTupGZdrtFIev-1R66oGHE
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 21
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
