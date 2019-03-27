
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
    "request_uuid": "94c2656b-50ca-11e9-a64a-dc536008769a"
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
    "request_uuid": "94c2656c-50ca-11e9-a64a-dc536008769a"
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
    "authenticate_ui_uri": "/accounts/auth_requests/94c2656a-50ca-11e9-a64a-dc536008769a/authenticate/ui/",
    "request_uuid": "94c2656a-50ca-11e9-a64a-dc536008769a"
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
    "request_uuid": "94c2656d-50ca-11e9-a64a-dc536008769a"
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
    "request_uuid": "f5e7e000-5074-11e4-8dd2-507b9d415345"
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTgsImVtYWlsIjoiY2F0aHJ5bjEwQHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2Mn0.TSmSB2XyvR1QUnA_I4EOqUa4O7iV0814gTNUvqQoXQw
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
### CREATE_CATALOGUEITEM: POST /catalogue/items/
Create Catalogue Item 
None
#### 201 (CATALOGUEITEM_CREATED)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTksImVtYWlsIjoibXVsbGVya2FtaWxhaEBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2Mn0.VwxMsCkQECIkbhofLra1Is5eWR-YKdwO4N2vago4KQA
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 20,
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
        "email": "mullerkamilah@hotmail.com",
        "id": 19,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "eleanoresteuber@gmail.com",
        "id": 20,
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
        "email": "mullerkamilah@hotmail.com",
        "id": 19,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjEsImVtYWlsIjoibWFydGlyZW5uZXJAd2lsbC5vcmciLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTM4MDMwNjJ9.g-pRJW2QPdTAVSdjvRBqcrsrIZcPCvkruHk8LxniRdI
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 22,
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
        "account_id": 21
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjMsImVtYWlsIjoib25pa29sYXVzQHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2Mn0.9_DD8gjFFYeUNN2y67RfM4azKZMFfWHNTe6H-asQB3I
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
        "account_id": 23
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjQsImVtYWlsIjoiaGVybmFuMDBAZ2xlYXNvbi5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTM4MDMwNjJ9.RFMGNSFSGJG-b68M7tK0X12C6xzBF_0HDwwt_GLzM-8
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjUsImVtYWlsIjoiY3N0YXJrQGdtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2Mn0.7H-j8xMLLzHzqEcBkZ7BjW7hFNUt7js9upmf18NovPE
```
Respone:
```json
{
    "@access": {
        "account_id": 25
    },
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjYsImVtYWlsIjoibW96ZWxsYTI0QGJlYWhhbi10b3kuYml6IiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ.taj4RtnV-VGCUIfmvenfOfSKUzF584K-qWcsux2pA94
```
Respone:
```json
{
    "@access": {
        "account_id": 26
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjcsImVtYWlsIjoibWlndWVsNDJAc2lwZXMtbW9yYXIuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ.ro51BNms8ZrQpOcapBIyH4p0nno6xM-TMUCcN_GqFiM
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgsImVtYWlsIjoiamFteWFoYW5kQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ._LiNUPsetCWtDhD6DgsjmJM2GklIweJR9C2-BDnHf8A
```
Respone:
```json
{
    "@access": {
        "account_id": 28
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjksImVtYWlsIjoicmlja2k0M0B5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTM4MDMwNjN9.SravUDIpub6c58r6LC-ibAehB5iMIawu-njLIAMSjz8
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
        "email": "kathryne00@watsica-pfeffer.net",
        "id": 31,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "tenika37@gutmann.com",
        "id": 30,
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
        "email": "ricki43@yahoo.com",
        "id": 29,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/15 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzIsImVtYWlsIjoicnVudGVmbGVtQHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2M30.q0RO1Hy8-_QqD1C4v1Tz53uItmfEk5DooajXqlo0_Nk
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 33,
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
        "account_id": 32
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImVtYWlsIjoibXdoaXRlQGdtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2M30.QHGNI5FiEBH5c6iXwdijXcORVyG42Vu2dc3bbAcrupo
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 35,
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
        "account_id": 34
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTAsImVtYWlsIjoib2dyYWR5QGJhc2hpcmlhbi1iYWlsZXkub3JnIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ.d2DvWaqpxnRsxSsuJLIrWcO5CE8xII18w5YmCHbahDY
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
                "maintained_by": null,
                "name": "Allie Thompson",
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
                "email": "rashaadaufderhar@pouros.com",
                "id": 51,
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
                "maintained_by": null,
                "name": "Allie Thompson",
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
                "email": "rashaadaufderhar@pouros.com",
                "id": 51,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTIsImVtYWlsIjoiZW1vZ2VuZXN0b2x0ZW5iZXJnQGRpY2tpbnNvbi1ydXNzZWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ.IWTxxY-6J0kpqV-dWCXcS9AAk2UY6YhUvrAL-kPSsfw
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
        "name": "Roma Armstrong",
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
        "email": "emogenestoltenberg@dickinson-russel.com",
        "id": 52,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTMsImVtYWlsIjoiY3VtbWluZ3NjaHJ5c3RhbEB5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTM4MDMwNjN9.aON15PRJtR_vwdXxZzFfyfEwZKy_vF5Un716TSiBvTI
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
        "account_id": 53
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTQsImVtYWlsIjoibm9lbDQzQGdtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2M30.2ZEAPicdFmaVhZ-RMrN7P7BUC0WR2BJ_89bSqLNH014
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
        "account_id": 54
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTUsImVtYWlsIjoiaG93ZWZsb3lAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTM4MDMwNjN9.R6d3ATY7m4gKKr7Tn_gM0whvtpSxXsVmGxu2bb8ZQjI
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTcsImVtYWlsIjoiam1pdGNoZWxsQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ.FmtgbHH79k_q1zZXMtd0M4k9J94LUGyxeT0--OzW6gY
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
### ESTIMATE_SIZE_OF_DOWNLOAD_REQUEST: POST /downloader/requests/estimate/
Estimate the size download based on the provided spec 
None
#### 200 (SIZE_OF_DOWNLOAD_REQUEST_ESTIMATED)
Request:
```http
POST /downloader/requests/estimate/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDksImVtYWlsIjoiZ2lubnlzYXR0ZXJmaWVsZEBib2dpc2ljaC1kYW1vcmUuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ.Kei5eLU-H9sVMcYuc-BfvQIIXlkl0buawDnzp1_Cg1g
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTgsImVtYWlsIjoiY2xlZG5lckB3aWxsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MzgwMzA2M30.gaHXyUFQPlmn-yVEeOK_vZ0RMLdquqTFs6iBmKXn5bA
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
        "maintained_by": null,
        "name": "Billy Witting",
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
        "email": "andra65@yahoo.com",
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
}
```
#### 404 (COULD_NOT_FIND_DOWNLOADREQUEST)
Request:
```http
GET /downloader/requests/9 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjEsImVtYWlsIjoiZ2F5bG9uamFrdWJvd3NraUBnbWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTM4MDMwNjR9.hN6BCx9pHzCk7cEbHTHU22KV--ySm8lceEnAYHuvZEg
```
Respone:
```json
{
    "@access": {
        "account_id": 61
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDgsImVtYWlsIjoiYWRsaW5lMTRAZXJkbWFuLWhhbmUuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUzODAzMDYzfQ.hzIFg17OS3zCctEEgjrsiAqO4yWUL27gM8794sKmm7M
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
