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
"""

import argparse
# [START dependencies]
import datetime

from google.cloud import bigtable
from google.cloud.bigtable import column_family
from google.cloud.bigtable import row_filters
# [END dependencies]


class BigTable():
    """ It covers basic operations like
        create table,
        delete table,
        list tables,
        insert rows,
        read_rows,
        filter_data
        delete rows,
    """
    PROJECT_ID = 'my-project-id'
    INSTANCE_ID = 'tf-instance'
    SAMPLE_ROWS = ['Manoj', 'Dave', 'kumar']

    def __init__(self, service_account_json=None, admin=True):
        self.instance = self.get_connection(service_account_json=service_account_json, admin=admin)

    def get_connection(self, service_account_json=None, admin=True):
        # The client must be created with admin=True because it will create a
        # table.
        if service_account_json is not None:
            client = bigtable.Client\
                .from_service_account_json(json_credentials_path=service_account_json, project=self.PROJECT_ID, admin=admin)
        else:
            client = bigtable.Client(project=self.PROJECT_ID, admin=admin)
        return client.instance(self.INSTANCE_ID)

    def list_tables(self):
        table_list = self.instance.list_tables()
        for table in table_list:
            print(table.table_id)
        return table_list

    def create_table(self, table_id):
        print('Creating the {} table.'.format(table_id))
        table = self.instance.table(table_id)

        print('Creating column family cf1 with Max Version GC rule...')
        # Create a column family with GC policy : most recent N versions
        # Define the GC policy to retain only the most recent 2 versions
        max_versions_rule = column_family.MaxVersionsGCRule(2)
        column_family_id = 'cf1'
        column_families = {column_family_id: max_versions_rule}
        if not table.exists():
            table.create(column_families=column_families)
        else:
            print("Table {} already exists.".format(table_id))

    def delete_table(self, table_id):
        """

        :param table_id:
        :return:
        """
        table = self.instance.table(table_id)
        print('Deleting the {} table.'.format(table_id))
        table.delete()

    def insert_rows(self, table_id, column_family_id='cf1'):
        column_name = 'names'.encode()
        table = self.instance.table(table_id)
        rows = []
        for i,value in enumerate(self.SAMPLE_ROWS):
            row_key = 'name{}'.format(i).encode()
            row = table.row(row_key)
            row.set_cell(column_family_id,
                         column_name,
                         value,
                         timestamp=datetime.datetime.utcnow())
            rows.append(row)
        table.mutate_rows(rows)

    def filter_row(self, table_id, column_family_id='cf1', column='name', key='name1'):
        print('Getting a single row by row key.')
        key = key.encode()
        table = self.instance.table(table_id)
        row_filter = row_filters.CellsColumnLimitFilter(1)
        row = table.read_row(key, row_filter)
        print(row.cell_value(column_family_id, column))

    def read_rows(self, table_id, column_family_id='cf1', column='names'.encode()):
        print('Scanning for all rows:')
        table = self.instance.table(table_id)
        row_filter = row_filters.CellsColumnLimitFilter(1)
        partial_rows = table.read_rows(filter_=row_filter)
        for row in partial_rows:
            cell = row.cells[column_family_id][column][0]
            print(cell.value.decode('utf-8'))

    def delete_cells(self, table_id, columns=['names'.encode()], key='name1'.encode()):
        print("deleting all cells in table {}".format(table_id))
        table = self.instance.table(table_id)
        row_filter = row_filters.CellsColumnLimitFilter(1)
        row = table.row(row_key=key)
        row.delete_cells(column_family_id='cf1', columns=columns)
        row.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--table_id', dest="table_id", default='sample_table', help="bigtable Table name")
    parser.add_argument('--key_path', dest="key_path", default=None, help="path for your service account json file path")
    args = parser.parse_args()
    bt = BigTable(service_account_json=args.key_path)
    bt.create_table(args.table_id)
    bt.list_tables()
    bt.insert_rows(args.table_id)
    bt.read_rows(args.table_id)
    bt.delete_cells(args.table_id)
    bt.read_rows(args.table_id)
    bt.delete_table(args.table_id)