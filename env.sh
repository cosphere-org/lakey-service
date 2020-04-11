#!/bin/bash

export LILY_SERVICE_PORT=8887

export GOOGLE_OAUTH2_CLIENT_ID=to.be.overwritten

export GOOGLE_OAUTH2_CLIENT_SECRET=to.be.overwritten

#
# AUTH
#
export AUTH_TOKEN_SECRET_KEY=to.be.overwritten

export AUTH_TOKEN_EXPIRATION_SECONDS=86400

export AUTH_REQUEST_EXPIRATION_SECONDS=600

#
# DB
#
export POSTGRES_DB=lakey_service

export POSTGRES_USER=lakey_service

export POSTGRES_PASSWORD=f8d9f8d9

export POSTGRES_HOST=localhost

export POSTGRES_PORT=5433


#
# AWS_S3
#
export AWS_LAKEY_KEY_ID=to.be.overwritten

export AWS_LAKEY_KEY_SECRET=to.be.overwritten

export AWS_LAKEY_REGION=to.be.overwritten

export AWS_LAKEY_RESULTS_LOCATION=to.be.overwritten

export AWS_S3_BUCKET=to.be.overwritten

#
# AZURE BLOB STORAGE
#
export AZURE_BLOB_STORAGE_ACCOUNT_NAME=to.be.overwritten

export AZURE_BLOB_STORAGE_ACCOUNT_KEY=to.be.overwritten

export AZURE_BLOB_STORAGE_CONTAINER=to.be.overwritten

#
# DATABRICKS
#
export DATABRICKS_TOKEN=to.be.overwritten

export DATABRICKS_HOST=to.be.overwritten

export DATABRICKS_CLUSTER_ID=to.be.overwritten

export DATABRICKS_RESULTS_LOCATION=to.be.overwritten

export DATABRICKS_SCRIPT_LOCATION=to.be.overwritten

#
# CATALOGUE ITEMS
#
export CATALOGUE_ITEMS_SAMPLE_SIZE=100

export CATALOGUE_ITEMS_DISTRIBUTION_VALUE_LIMIT=1000

export CATALOGUE_ITEMS_DISTRIBUTION_VALUE_BINS_COUNT=100

# -- THE OVERWRITES
source env_private.sh
