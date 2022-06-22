#!/bin/bash

GCR_SERVICE=${1:-kent-dev}
MIN_INSTANCE_LIMIT=${2:-0}

gcloud config configurations activate juncture

GCP_PROJECT=`gcloud config get-value project`

echo GCP_PROJECT=${GCP_PROJECT} GCR_SERVICE=${GCR_SERVICE} MIN_INSTANCE_LIMIT=${MIN_INSTANCE_LIMIT}

cd $(dirname "$0")
rsync -va ../app.py .
# rsync -va ../static .

gcloud builds submit --tag gcr.io/${GCP_PROJECT}/${GCR_SERVICE}

rm -rf app.py static

gcloud beta run deploy ${GCR_SERVICE} \
    --image gcr.io/${GCP_PROJECT}/${GCR_SERVICE} \
    --min-instances ${MIN_INSTANCE_LIMIT} \
    --allow-unauthenticated \
    --platform managed \
    --memory 1Gi
