
# Lakey-Service

Is a project allowing huge amount of people (clients) to connect with expensive Data Lakes in order to download data to their local machines which will allow rapid prototyping of data driven algorithms and applications.

## The Goal

Laker was built and designed with one goal in mind: "to free up the data, which are otherwise sitting idle and just being covered in dust".

To learn more read high level overview regarding the [Big Data Myths](https://github.com/cosphere-org/lakey-service/blob/master/LAKEY.md)

Before one starts working with `Lakey-Service` two files must be obtained over secured channel: `ngrok_private.yaml` and `env_private.sh` (please reach author for them).

## Installation

```bash
make install
source .venv/bin/activate
```

## Running development server

```bash
make start_dev_server port=8889
```

## Running grok

In order to test the authentication while still developing locally one can use `ngrok` proxy which will expose the locally running service over the web.

In order to start such a process one can run:

```bash
source env.sh && \
ngrok start --config ngrok_private.yaml --region eu lakey-<you-name>
```

## Architecture

[![lakey-flows-main](./assets/lakey-flows-main.png)](https://www.draw.io/#G10wj4nSI7JHLVParPvdDMrLe4CMT4Vg6r)

### Auth Token Management - who is who

[![auth-token-flow](./assets/lakey-auth-token-flow.png)](https://www.draw.io/#G10wj4nSI7JHLVParPvdDMrLe4CMT4Vg6r)

### Catalogue - discovery of data

https://github.com/cosphere-org/lakey-service/blob/master/.lily/API.md#catalogue-items-management

### Downloader - efficient data download

https://github.com/cosphere-org/lakey-service/blob/master/.lily/API.md#download-requests-management

