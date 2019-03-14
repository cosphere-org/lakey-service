
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
    "request_uuid": "33515101-466a-11e9-b05d-0028f8484bd5"
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
    "request_uuid": "33515102-466a-11e9-b05d-0028f8484bd5"
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
    "authenticate_ui_uri": "/accounts/auth_requests/33515100-466a-11e9-b05d-0028f8484bd5/authenticate/ui/",
    "request_uuid": "33515100-466a-11e9-b05d-0028f8484bd5"
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
    "request_uuid": "33515103-466a-11e9-b05d-0028f8484bd5"
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
    "request_uuid": "f5e7e000-5074-11e4-9ab2-02426ec57dd1"
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjYsImVtYWlsIjoicWdpc2xhc29uQHJlaWxseS1zdGllZGVtYW5uLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1NX0.myqDR0tt1AbQ1mDJMG3hVTHDXRvr3rCypcn_MQM1ock
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjcsImVtYWlsIjoiaGJvZGVAdG9ycGh5LmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1NX0.lvLrmi6wS08CBlW6wQKVOBG32ro8yK9Fk238Vb95HBI
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
        "email": "hbode@torphy.com",
        "id": 27,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "lindgrenjocelynn@hotmail.com",
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
        "email": "hbode@torphy.com",
        "id": 27,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjksImVtYWlsIjoibGFraW5zdGFuQHlhaG9vLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1NX0.1IcajR8dGiHCSjVTcf72NcIJSrfbguwN3KTy3l_12U4
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzEsImVtYWlsIjoibmF0aGFsaWFoYXJyaXNAbWFudGUtb3JuLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1NX0.ccFfpzjVRoiKhfLdEFCHNJaZAUl2XhrVzXNjv463WAg
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
### DELETE_CATALOGUEITEM: DELETE /catalogue/items/{item_id}
Delete Catalogue Item 
None
#### 200 (CATALOGUEITEM_DELETED)
Request:
```http
DELETE /catalogue/items/13 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzIsImVtYWlsIjoiZW5vbGE4M0B5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTV9.LJOn_TXyudo9jphf6xiLn_dZOhMxdYKKddlxGHCpzWw
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzMsImVtYWlsIjoiaHltYW4yN0ByeWFuLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1NX0.00LjMLdWwN21MQqJmGMDKvUsmDn3MbSWfyWA_bkE7Qo
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImVtYWlsIjoiYXJpYW5lZ2lic29uQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYyMTU1fQ.p6F_n2tzS4dA02zZ35vOlJh5-XEV64e5bc1oBCP7LWY
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzUsImVtYWlsIjoiaGhvZGtpZXdpY3pAYmVyZ25hdW0uYml6IiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYyMTU1fQ.A_Yt9f-uSRCiIhsSPN5NKCvSQkSMvEGK4nskXhA1naI
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzYsImVtYWlsIjoiZXVsYWxpYTY5QGZlaWwtc21pdGhhbS5pbmZvIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYyMTU1fQ.vyYvV_zARaj67a7AI5XgpqXKZyJJfCiHO0sRXOEdlnA
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImVtYWlsIjoibW1ja2VuemllQGdtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1NX0.JWxG32IR4YLURWCAXV5yhHMAWWb-MkfDw1t6mEuPJqk
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
        "email": "wilfredframi@koch-kuhn.com",
        "id": 39,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "maintained_by": {
        "@type": "account",
        "email": "wardmarley@hotmail.com",
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
        "email": "mmckenzie@gmail.com",
        "id": 37,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/20 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDAsImVtYWlsIjoiY3Jpc3N5c3Ryb3NpbkBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1NX0.vTpyXdmiZK-s3VqJzspgdfWU75DeopXE6sswdAoa8sM
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDIsImVtYWlsIjoibWlzc3k3OUBrZWVsaW5nLWhvZWdlci5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTV9.f6rbYb8lUT54jILk15TG5XEW_e9_YHK-arti_su-Doo
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTgsImVtYWlsIjoic2NyaXN0QHRveS1icmF1bi5iaXoiLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTZ9.ZVflTbu0RE5Lk6u13uQW82hKjHrC6I4gG4wJIqU5RDg
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
                "name": "Maryjo Donnelly",
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
                "email": "danielkoelpin@hamill-lindgren.com",
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
                "name": "Maryjo Donnelly",
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
                "email": "danielkoelpin@hamill-lindgren.com",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjAsImVtYWlsIjoiY29yZGVsaWExM0BrcmVpZ2VyLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1Nn0.ltCzQCHobDl2zPecOPYCNo7t4KXta5h39HIEmpInK4E
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
        "name": "Dr. Viridiana Daugherty",
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
        "email": "cordelia13@kreiger.com",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjIsImVtYWlsIjoic3RldWJlcmphc3BlckBnbWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTZ9.pLYrHtL6UJLdfNEV1U5YgrjjmzuM2I81ylTYFLNvf2U
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
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
POST /downloader/requests/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjQsImVtYWlsIjoiZGVzaWJhbGlzdHJlcmlAamFjb2JpLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1Nn0.MhfjEfu0TFHxqXGOwAOm9qq0MpMiQc3HKEAxZsjwXOA
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
### DELETE_DOWNLOADREQUEST: DELETE /downloader/requests/{request_id}
Creator can cancel request or remove himself from waiters 
None
#### 200 (DOWNLOADREQUEST_DELETED)
Request:
```http
DELETE /downloader/requests/11 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjUsImVtYWlsIjoidGlsbG1hbm1haUBwYWRiZXJnLWNocmlzdGlhbnNlbi5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTZ9.3utCCFWcBuQnffEGAH_NedsLgBAwAfDPLL9RpGBOhwU
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjcsImVtYWlsIjoiamFza29sc2tpYW5kcmFAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTZ9.F-5qtMNahcc0f_wA4bzz5jkA7fGt2nOQX94U6hj4kgE
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTcsImVtYWlsIjoiYXRoYWRhbW9yZUB5YWhvby5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTZ9.8xlqdET-NRf7IaKuakNqYlJWPac6zeZqHLzAvZG23mw
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjgsImVtYWlsIjoibWFyeWx5bm1pbGxlckBnbG92ZXIuaW5mbyIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU1MjY2MjE1Nn0.SqAx2wB2UfT3rd4NnUFUV0IXM7XHAHQ6J9wXHGk5dBs
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
        "name": "Derl Wunsch",
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
        "email": "ryne55@hilll-gerlach.com",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NzEsImVtYWlsIjoiaHVkc29uZXNjb0BnbWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NTI2NjIxNTZ9.pTTlGfqZvF02Hwon57c26FyvWPopRCroYOiiOwlnRR0
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTYsImVtYWlsIjoia2luZ2FtaXJAZ21haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTUyNjYyMTU2fQ.iy9oK0upTxsoVfcH8X9UK08R22rszjRGB3a8PQhl1YY
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
