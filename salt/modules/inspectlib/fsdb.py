# -*- coding: utf-8 -*-
#
# Copyright 2016 SUSE LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import csv
import datetime
from salt.utils.odict import OrderedDict


class CsvDBEntity(object):
    '''
    Serializable object for the table.
    '''
    def _serialize(self, description):
        '''
        Serialize the object to a row for CSV according to the table description.

        :return:
        '''
        return [getattr(self, attr) for attr in description]


class CsvDB(object):
    '''
    File-based CSV database.
    This database is in-memory operating plain text csv files.
    '''
    def __init__(self, path):
        '''
        Constructor to store the database files.

        :param path:
        '''
        self._prepare(path)
        self._opened = False
        self.db_path = None
        self._opened = False
        self._tables = {}

    def _prepare(self, path):
        self.path = path
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def _label(self):
        '''
        Create label of the database, based on the date-time.

        :return:
        '''
        return datetime.datetime.utcnow().strftime('%Y%m%d.%H%M%S')

    def new(self):
        '''
        Create a new database and opens it.

        :return:
        '''
        dbname = self._label()
        self.db_path = os.path.join(self.path, dbname)
        if not os.path.exists(self.db_path):
            os.makedirs(self.db_path)
        self._opened = True
        self.list_tables()

        return dbname

    def purge(self, dbid):
        '''
        Purge the database.

        :param dbid:
        :return:
        '''

    def list(self):
        '''
        List all the databases on the given path.

        :return:
        '''
        databases = []
        for dbname in os.listdir(self.path):
            databases.append(dbname)
        return list(reversed(sorted(databases)))

    def list_tables(self):
        '''
        Load existing tables and their descriptions.

        :return:
        '''
        if not self._tables:
            for table_name in os.listdir(self.db_path):
                self._tables[table_name] = self._load_table(table_name)

        return self._tables.keys()

    def _load_table(self, table_name):
        with open(os.path.join(self.db_path, table_name), 'rb') as table:
            return OrderedDict([tuple(elm.split(':')) for elm in csv.reader(table).next()])

    def open(self, dbname=None):
        '''
        Open database from the path with the name or latest.
        If there are no yet databases, create a new implicitly.

        :return:
        '''
        databases = self.list()
        if self.is_closed():
            self.db_path = os.path.join(self.path, dbname or (databases and databases[0] or self.new()))
            if not self._opened:
                self.list_tables()
                self._opened = True

    def close(self):
        '''
        Close the database.

        :return:
        '''
        self._opened = False

    def is_closed(self):
        '''
        Return if the database is closed.

        :return:
        '''
        return not self._opened

    def table_from_object(self, obj):
        '''
        Create a table from the object.
        NOTE: This method doesn't stores anything.

        :param obj:
        :return:
        '''
        get_type = lambda item: str(type(item)).split("'")[1]
        if not os.path.exists(os.path.join(self.db_path, obj._TABLE)):
            with open(os.path.join(self.db_path, obj._TABLE), 'wb') as table_file:
                csv.writer(table_file).writerow(['{col}:{type}'.format(col=elm[0], type=get_type(elm[1]))
                                                 for elm in tuple(obj.__dict__.items())])

    def store(self, obj):
        '''
        Store an object in the table.

        :param obj:
        :return:
        '''
        with open(os.path.join(self.db_path, obj._TABLE), 'a') as table:
            csv.writer(table).writerow(self._validate_object(obj))

    def _validate_object(self, obj):
        descr = self._tables.get(obj._TABLE)
        if descr is None:
            raise Exception('Table {0} not found.'.format(obj._TABLE))
        return obj._serialize(self._tables[obj._TABLE])

    def get(self, table_name, matches=None, mt=None, lt=None, eq=None):
        '''
        Get objects from the table.

        :param table_name:
        :param matches: Regexp.
        :param mt: More than.
        :param lt: Less than.
        :param eq: Equals.
        :return:
        '''
        objects = []
        return objects
