
# Laker

Is a project allowing huge amount of people (clients) to connect with expensive Data Lakes in order to download data to their local machines which will allow rapid prototyping of data driven algorithms and applications.

## The Goal

Laker was built and designed with one goal in mind: "to free up the data, which are otherwise sitting idle and just being covered in dust".

## TODO

[ ] create fixture for models
    --> add manage.py command for creating sample catalog items
[ ] make sure that entry point works

[ ] remember to add task with regards to registering data needs, amount of downloads, who is requesting what etc.
    --> data audit

[ ] finish styling of authentication page
[ ] create repo for lakey-ui and add some basic stuff there
[ ] add it to lakey-ui
[ ] add in lakey-ui authentication screen on discover and download
[ ] add very basic widget for download
[ ] add very basic widget for discover --> no full text search just display what it receives
[ ] on download return random DataFrame

[ ] describe how to set up ngrok
- add ngrok conf for each developer to work in an independent way
- `ngrok start --config ~/.ngrok/ngrok.yml --region eu --all`

[ ] add instructions with regards to usage of postgres --> maybe just use dockerized one --> like in presenter and others
[ ] create notebook for adding custom Catalog Items
[ ] update docs of lily --> move to github
[ ] add lily assitent --> move to github
[ ] lily sort out stuff with `conf.yaml` --> maybe overwrite setup.py?
[ ] what about secrets?
    - pass them over slack
    - ignore from git
    - just a bash script
[ ] create installations instructions on github / bitbucket
[ ] decide how to compile QUERY --> should process download do it based on spec? --> yup or rather executor?
[ ] TO BE USED for client side download:
    https://blogs.msdn.microsoft.com/cie/2017/05/13/azure-blob-storage-operations-with-storage-python-sdk/
    https://github.com/Azure/azure-storage-python/blob/master/azure-storage-blob/azure/storage/blob/baseblobservice.py#L2082

## Architecture

[![architecture](./assets/lakey-architecture.png)](https://www.draw.io/#G1zrMb3J6eeFVEmbUvT6ETs240ZzVe4eAy)

### Auth Token Management - who is who

[ ] FIXME: add diagram to describe the FLOW here!!!!


### Cataloger - discovery of data

...


### Downloader - efficient data download

...
