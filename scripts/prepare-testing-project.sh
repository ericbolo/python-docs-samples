#!/bin/bash

# Copyright 2015 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

GCLOUD_PROJECT=$(gcloud config list project --format="value(core.project)" 2>/dev/null)

echo "Configuring project $GCLOUD_PROJECT for system tests."

echo "Creating cloud storage bucket."
gsutil mb gs://$GCLOUD_PROJECT
gsutil defacl set public-read gs://$GCLOUD_PROJECT

echo "Creating bigquery resources."
gcloud alpha bigquery datasets create test_dataset
gcloud alpha bigquery datasets create ephemeral_test_dataset
gsutil cp bigquery/api/resources/data.csv gs://$GCLOUD_PROJECT/data.csv
gcloud alpha bigquery import \
    gs://$GCLOUD_PROJECT/data.csv \
    test_dataset/test_table \
    --schema-file bigquery/api/resources/schema.json

echo "Creating datastore indexes."
gcloud preview app deploy -q datastore/api/index.yaml

echo "Creating pubsub resources."
gcloud alpha pubsub topics create gae-mvm-pubsub-topic

echo "To finish setup, follow this link to enable APIs."
echo "https://console.cloud.google.com/flows/enableapi?project=${GCLOUD_PROJECT}&apiid=bigquery,cloudmonitoring,compute_component,datastore,datastore.googleapis.com,dataproc,dns,plus,pubsub,logging,storage_api,vision.googleapis.com"
