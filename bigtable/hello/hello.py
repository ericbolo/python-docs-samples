#!/usr/bin/env python

# Copyright 2016 Google Inc.
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

"""Demonstrates how to connect to Cloud Bigtable and run some basic operations.

Prerequisites:

- Create a Cloud Bigtable cluster.
  https://cloud.google.com/bigtable/docs/creating-cluster
- Set your Google Application Default Credentials.
  https://developers.google.com/identity/protocols/application-default-credentials
- Set the GCLOUD_PROJECT environment variable to your project ID.
  https://support.google.com/cloud/answer/6158840
"""

import argparse

from gcloud import bigtable
from gcloud.bigtable import happybase


TABLE_NAME = 'Hello-Bigtable'
COLUMN_FAMILY_NAME = 'cf1'
COLUMN_NAME = 'greeting'
FULL_COLUMN_NAME = '{fam}:{col}'.format(
    fam=COLUMN_FAMILY_NAME,
    col=COLUMN_NAME)

GREETINGS = [
    'Hello World!',
    'Hello Cloud Bigtable!',
    'Hello HappyBase!',
]


def main(project, cluster_id, zone, table_name):
    # The client must be created with admin=True because it will create a
    # table.
    client = bigtable.Client(project=project, admin=True)

    with client:
        cluster = client.cluster(zone, cluster_id)
        cluster.reload()
        connection = happybase.Connection(cluster=cluster)

        print('Creating the {} table.'.format(table_name))
        connection.create_table(
            table_name,
            {
                COLUMN_FAMILY_NAME: dict()  # Use default options.
            })
        table = connection.table(table_name)

        print('Writing some greetings to the table.')
        for i, value in enumerate(GREETINGS):
            row_key = 'greeting{}'.format(i)
            table.put(row_key, {FULL_COLUMN_NAME: value})

        print('Scanning for all greetings:')
        for key, row in table.scan():
            print('\t{}: {}'.format(key, row[FULL_COLUMN_NAME]))

        print('Deleting the {} table.'.format(table_name))
        connection.delete_table(table_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='A sample application that connects to Cloud' +
                    ' Bigtable.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        'project',
        help='Google Cloud Platform project ID that contains the Cloud' +
             ' Bigtable cluster.')
    parser.add_argument(
        'cluster', help='ID of the Cloud Bigtable cluster to connect to.')
    parser.add_argument(
        'zone', help='Zone that contains the Cloud Bigtable cluster.')
    parser.add_argument(
        '--table',
        help='Table to create and destroy.',
        default=TABLE_NAME)

    args = parser.parse_args()
    main(args.project, args.cluster, args.zone, args.table)
