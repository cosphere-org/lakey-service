
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
    "request_uuid": "bfbea6b3-7b31-11ea-83d0-4485007e7d04"
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
    "request_uuid": "bfbea6b2-7b31-11ea-83d0-4485007e7d04"
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
    "authenticate_ui_uri": "/accounts/auth_requests/bfbea6b0-7b31-11ea-83d0-4485007e7d04/authenticate/ui/",
    "request_uuid": "bfbea6b0-7b31-11ea-83d0-4485007e7d04"
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
    "request_uuid": "bfbea6b1-7b31-11ea-83d0-4485007e7d04"
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
    "request_uuid": "f5e7e000-5074-11e4-9c1a-507b9deb8705"
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
GET /catalogue/items/?has_samples=False HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjgsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxN30.r3p_9LIRdP5X9VagtKSzSvs0kwYN-IXNXS8DJfeBA1k
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
            "id": 26,
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
            "id": 28,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjUsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxN30.VSO6z6kCUJ-NUEOmQgI5_i8WSX5VJlrH7L-g32oRABY
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 26,
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
        "email": "feilshanta@hotmail.com",
        "id": 25,
        "type": "ADMIN"
    },
    "executor_type": "DATABRICKS",
    "id": 22,
    "maintained_by": {
        "@type": "account",
        "email": "neelymorissette@lueilwitz-marvin.com",
        "id": 26,
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
        "email": "feilshanta@hotmail.com",
        "id": 25,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
POST /catalogue/items/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjEsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxN30.3WXbTAKKlZfoaI8rQcQDZnXEkoAlyHuVpo1GQz5KOzs
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
    "@authorizer": {
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MjQsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxN30.TZdVRp9Lr80-1tmZtVgdnV-DPcnBrHBaZFH-x2JEc6k
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
        "account_id": 24
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
DELETE /catalogue/items/1 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MiwiZW1haWwiOiJmZWlsc2hhbnRhQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2NjEyODE2fQ.oh3p86VnxsmOgGXP2jEsAaPi8W_QQETPBUkBGgHchyo
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
DELETE /catalogue/items/3 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MywiZW1haWwiOiJmZWlsc2hhbnRhQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2NjEyODE2fQ.Q9RljX7iNGxLHwdiv3WZ-oB-KdevHLtf8Af99h-qsik
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 3
    },
    "@event": "NOT_CANCELLED_DOWNLOAD_REQEUSTS_DETECTED",
    "@type": "error",
    "item_id": 3,
    "not_cancelled_count": 1
}
```
#### 404 (COULD_NOT_FIND_CATALOGUEITEM)
Request:
```http
DELETE /catalogue/items/69506 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTAsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxNn0.5tUppeVGbs6K3IqX3B4DUdtYRRDR-YZQ9f1JIrjmqDA
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 10
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
GET /catalogue/items/6 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OSwiZW1haWwiOiJmZWlsc2hhbnRhQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2NjEyODE2fQ.ESJvIsioW-AdL_thI5n7OZEJ38NoqatDY7Ix3_aPrAI
```
Respone:
```json
{
    "@event": "CATALOGUEITEM_READ",
    "@type": "catalogue_item",
    "created_by": null,
    "executor_type": "ATHENA",
    "id": 6,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NCwiZW1haWwiOiJmZWlsc2hhbnRhQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2NjEyODE2fQ.lFArgWrpVeME5PEoNNphO3WmyGJY30At4hD64XZBP_A
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 4
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
PUT /catalogue/items/8 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTEsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxN30.9y_PDuqDzNyGCgpESdoNbEzTN63avtee0tGvszlE2WE
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 12,
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
        "email": "rhuels@walter.com",
        "id": 13,
        "type": "RESEARCHER"
    },
    "executor_type": "DATABRICKS",
    "id": 8,
    "maintained_by": {
        "@type": "account",
        "email": "neelymorissette@lueilwitz-marvin.com",
        "id": 12,
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
        "email": "feilshanta@hotmail.com",
        "id": 11,
        "type": "ADMIN"
    }
}
```
#### 400 (BODY_DID_NOT_VALIDATE)
Request:
```http
PUT /catalogue/items/5 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NywiZW1haWwiOiJmZWlsc2hhbnRhQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2NjEyODE2fQ.lOac3ivmDN1dbM_ZPFmHN_YyzclBejHpGoY9vrJPlq8
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 8,
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
        "account_id": 7
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6NSwiZW1haWwiOiJmZWlsc2hhbnRhQGhvdG1haWwuY29tIiwidHlwZSI6IkFETUlOIiwiZXhwIjoxNTg2NjEyODE2fQ.1vBz2A51DEzwtmXG3p9QQmFeOrGTpLsVO2d8kethoR8
CONTENT-TYPE: application/json
{
    "executor_type": "DATABRICKS",
    "maintained_by_id": 6,
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
        "account_id": 5
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
PUT /catalogue/items/9/samples_and_distributions/ HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTQsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxN30.XxRyY29LR7s8jXsqYmC44D4jYcwsX1BgsX_46sUkBGo
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MTcsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgxN30.aMsYr4P1o7Vdrv0h6N5DY-pmeh2y99TWF71eYZObypA
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 17
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTAsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyM30.KwwRQ2kPV7C3SwWssrIRcEZHTyVPT4sIzM2tYQI6bkw
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
                "id": 77,
                "maintained_by": null,
                "name": "Tyron Medhurst",
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
                "email": "gay68@hirthe.biz",
                "id": 91,
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
                "id": 77,
                "maintained_by": null,
                "name": "Tyron Medhurst",
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
                "email": "gay68@hirthe.biz",
                "id": 91,
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
DELETE /downloader/requests/16 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODQsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyMn0.7fLVRBfwdtNKWTReT8bH91W2uOoZ8UMKiRZZf9Jp1Ho
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODYsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyMn0.doO3Qj9j7JFYQqJK6NnssPNRIWh-a9PK0Xn_ZR3dBGQ
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 86
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTUsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyM30.y0sZEMJRigBxT4IBXuNsMAlB5A8UK1hYdPc0KAPKH4Q
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 81,
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
GET /downloader/requests/15 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODIsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyMn0.EkH7xgyGQ5eGnj-cQX0brVo7tse7LfH3DCYKXIY9x6M
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
        "id": 72,
        "maintained_by": null,
        "name": "Tyron Medhurst",
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
        "email": "gay68@hirthe.biz",
        "id": 83,
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
GET /downloader/requests/17 HTTP/1.1
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODcsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyMn0.1HMdPoNCS4nljM4ZtOhqTC0JmrstPH9_x__deWjl7X4
```
Respone:
```json
{
    "@authorizer": {
        "account_id": 87
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTQsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyM30.vn5e30jcutnXqFMSr7okWduwM0CBAe2DBkZGKyq5L50
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 80,
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
        "id": 80,
        "maintained_by": null,
        "name": "Tyron Medhurst",
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTIsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyM30.USVcdeR8U2_d1WuDqb7rfXTiMG4TVw67R9cyFhwMhLY
CONTENT-TYPE: application/json
{
    "catalogue_item_id": 78,
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
        "id": 78,
        "maintained_by": null,
        "name": "Tyron Medhurst",
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
        "email": "feilshanta@hotmail.com",
        "id": 92,
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6OTMsImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyM30.LVqyUJzo7NZ22j4rOoXSDJItFWmIXzTa_uELKfT87Fk
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
        "account_id": 93
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
AUTHORIZATION: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6ODksImVtYWlsIjoiZmVpbHNoYW50YUBob3RtYWlsLmNvbSIsInR5cGUiOiJBRE1JTiIsImV4cCI6MTU4NjYxMjgyMn0.pYYMapbAYjY9nK5Ggz_qvPgq5Zq2_oy_JnyUGInToe0
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
        "account_id": 89
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
