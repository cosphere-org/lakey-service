
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
    "request_uuid": "4bda0178-8c72-11e9-a979-0028f8484bd5"
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
    "request_uuid": "4bda0179-8c72-11e9-a979-0028f8484bd5"
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
    "authenticate_ui_uri": "/accounts/auth_requests/4bda0177-8c72-11e9-a979-0028f8484bd5/authenticate/ui/",
    "request_uuid": "4bda0177-8c72-11e9-a979-0028f8484bd5"
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
    "request_uuid": "4bda0176-8c72-11e9-a979-0028f8484bd5"
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
    "request_uuid": "f5e7e000-5074-11e4-9ea7-02424daebf90"
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
GET /catalogue/items/?query=feature+%26+IOT+%7C+temperature HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NjAsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.VIN4ltbhxXixTT0DS0mFJUgUdBUSy56v-zwKTexeP6s
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
            "id": 47,
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
            "id": 48,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTEsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.Mg5YTPah6ZTz7abjotH_B0SZNinFwikC9cY0s7kIVwE
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 52,
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
        "email": "lynchrandle@hotmail.com",
        "id": 51,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "id": 34,
    "maintained_by": {
        "@type": "account",
        "email": "levi49@yahoo.com",
        "id": 52,
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
        "email": "lynchrandle@hotmail.com",
        "id": 51,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTUsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.XvgVV7AYHabVHH2tJxhCV7b4bKvkteq5BAbWMmw3ekc
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 56,
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
        "account_id": 55
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NTQsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.VJcDqSpknuYkGsmGavDv7XNh6-Orh9NUPLzJj5VLF9A
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
        "account_id": 54
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
DELETE /catalogue/items/23 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzgsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.5NkO7c_onGqGJSY_u2CHVBcMCXPJNjolspnnhesHIsU
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
DELETE /catalogue/items/27 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDEsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.RXf4sXLmRTsBm-eYjKWSXhJX5JhMwsb8F6rtInxk8QA
```
Respone:
```json
{
    "@access": {
        "account_id": 41
    },
    "@event": "NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED",
    "@type": "error",
    "item_id": 27,
    "not_cancelled_count": 1
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
DELETE /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzksImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.T_49IGSIp0UcYdMOozMHewW-aZY9z9Q3nRCJIBKBfTc
```
Respone:
```json
{
    "@access": {
        "account_id": 39
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
GET /catalogue/items/25 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDAsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.tP4vUoWYGkdmaxFHtXGp30tBUnJ731CEXOZZ27Ib_UU
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_READ",
    "@type": "catalogue_item",
    "created_by": null,
    "executor_type": "ATHENA",
    "id": 25,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDcsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.PHEPF_N63MTDnIHiSgUMG-XZNF8SJrW5OZoOvtVKtyA
```
Respone:
```json
{
    "@access": {
        "account_id": 47
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
PUT /catalogue/items/29 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDIsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.9sxNWIeXZgNmb108lsQGQ9PscsqusSunkVIMD3pdYqE
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 43,
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
        "email": "qmohr@franecki-russel.net",
        "id": 44,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "id": 29,
    "maintained_by": {
        "@type": "account",
        "email": "levi49@yahoo.com",
        "id": 43,
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
        "email": "lynchrandle@hotmail.com",
        "id": 42,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/30 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDgsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.9wU90Bgl6AjhaxI0I9fJ4SlbUILmu7GlGyqZOiznX8o
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 49,
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
        "account_id": 48
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NDUsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.v--OW6u1FzeJDk5_S4JF0ZrdJW2qNVP8kLqXkNRcDuk
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
    "@access": {
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
PUT /catalogue/items/22/samples_and_distributions/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzQsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.ga4AVmbwD714dlVNh3fsd31gwK3fA_09tp0XMa9SNYE
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTN9.zVitpUijdtAiq8BRiJk82Cku1S_nhjam263TuXZrwaY
```
Respone:
```json
{
    "@access": {
        "account_id": 37
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTJ9.GVcc5aAmSPRJOgkGEqrMDjQc8gxwpyvOhe98j__Xrtw
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
                "id": 10,
                "maintained_by": null,
                "name": "Evette Gleichner",
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
                "email": "kendal68@hotmail.com",
                "id": 15,
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
                "id": 10,
                "maintained_by": null,
                "name": "Evette Gleichner",
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
                "email": "kendal68@hotmail.com",
                "id": 15,
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
DELETE /downloader/requests/2 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZW1haWwiOiJseW5jaHJhbmRsZUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU2MDM2MjIxMn0.SOtSNhbytiHPeALjlxm-H3vUEvgDi5YBXzH4-6kDzcA
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OCwiZW1haWwiOiJseW5jaHJhbmRsZUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU2MDM2MjIxMn0.3sQaU5fsdCGyIvXFfZ2SJeEgF7EKV-ioMmvtEfYZ0qo
```
Respone:
```json
{
    "@access": {
        "account_id": 8
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTcsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTJ9.yl8KDC3p6jsPTkI5XfbIszHhiIz_ZgCURul0MOYvA9Y
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 12,
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
GET /downloader/requests/1 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJseW5jaHJhbmRsZUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU2MDM2MjIxMn0.2OyeifTet8iwOYIrUFOMBBRAc-vSbsD6wfEaxhtkoc0
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
        "id": 2,
        "maintained_by": null,
        "name": "Evette Gleichner",
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
        "email": "kendal68@hotmail.com",
        "id": 4,
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
GET /downloader/requests/3 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OSwiZW1haWwiOiJseW5jaHJhbmRsZUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU2MDM2MjIxMn0.qVE_Nyk8N28wH-PBLJzaep4BSXiqHBuHc_9iVkx_DHo
```
Respone:
```json
{
    "@access": {
        "account_id": 9
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTEsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTJ9.w7iBLnjdZOZVUZtU3N1aQ4uoW-We96Jp7Bf734lLEE8
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 7,
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
        "id": 7,
        "maintained_by": null,
        "name": "Evette Gleichner",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTYsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTJ9.fs1EiOS5JtCKOQoTdVW5MkIq-5zsDRFpeGQ_cXID-j8
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 11,
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
        "id": 11,
        "maintained_by": null,
        "name": "Evette Gleichner",
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
        "email": "lynchrandle@hotmail.com",
        "id": 16,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTIsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTJ9.MI1ENC3otkPOFor2TDCkHIbmyiukbWZswmrNcZsjuf0
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
        "account_id": 12
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTMsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTJ9.-14TjyJ5_518J93KUB5wOcPaUnvGqqu7Jt12GB0YCcY
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
        "account_id": 13
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTgsImVtYWlsIjoibHluY2hyYW5kbGVAaG90bWFpbC5jb20iLCJ0eXBlIjoiQURNSU4iLCJleHAiOjE1NjAzNjIyMTJ9.2pRlWX079GF9VYsugIyvq8d1L-qD3v6EdihsvfwtIXY
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 13
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
