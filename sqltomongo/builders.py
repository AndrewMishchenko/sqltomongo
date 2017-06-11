import sys

from pql import match, project, skip, limit, unwind, find

from sqltomongo.filters import (project_filter,
                                order_filter,
                                coma_filter,
                                unwind_filter,
                                order_filter_find
                                )
from sqltomongo.keywords import KEYWORDS
from sqltomongo.sql import Checker


class Router(object):
    def __init__(self, db, formated_query):
        '''Check that formated_query is not empty'''
        try:
            if bool(formated_query):
                self.formated_query = formated_query
            else:
                raise ValueError
        except ValueError:
            sys.exit('Stoped! Your parsed sql is empty! Please try again.')

        if Checker.parse_first(formated_query) == 'SELECT':
            self.query = SelectBuilder(db, formated_query).query
        else:
            pass


class SelectBuilder(object):
    def __init__(self, db, formated_query):
        """
        Initialize SELECT statement
        :param db: database
        :param formated_query: dict of parsed query
        """
        self.database = db.database
        self.formated_query = formated_query
        try:
            if len(formated_query["FROM"]) >= 1:
                try:
                    if self.database is not None:
                        self.collection = self.database[coma_filter(
                            formated_query["FROM"])[0]]
                    else:
                        raise TypeError
                except TypeError:
                    sys.exit('At first you must connect to the database with'
                             ' use method!'
                             )
            else:
                raise ValueError
        except ValueError:
            sys.exit('Stoped! Your collection is {}! Please try again.'
                     ''.format(formated_query["FROM"])
                     )
        try:
            # find()
            if (len(formated_query['SELECT']) >= 1 and (
                formated_query['SELECT'][0] == KEYWORDS['ASTERISK'])) or (
                len([obj for obj in coma_filter(formated_query['SELECT']
                                            ) if obj.endswith('.*')]) == 0):
                self.show_fields = project_filter(coma_filter(
                                    formated_query['SELECT'])) if not (
                                    formated_query['SELECT'][0] == KEYWORDS[
                                        'ASTERISK']) else None
                self.match = find(
                    " ".join(formated_query['WHERE'])) if (
                    'WHERE' in formated_query.keys()) else dict()
                self.sort = order_filter_find(
                    formated_query['ORDER']) if (
                    'ORDER' in formated_query.keys()) else None
                self.skip = int(formated_query['SKIP'][0]) if (
                    'SKIP' in formated_query.keys()) else None
                self.limit = int(formated_query['LIMIT'][0]) if (
                    'LIMIT' in formated_query.keys()) else None
                self.query = self.find_query()
            # aggregate
            elif len(formated_query['SELECT']) >= 1 and (
                    len([obj for obj in coma_filter(formated_query['SELECT']
                                            ) if obj.endswith('.*')]) >= 1):
                self.project = project(**(project_filter(
                    coma_filter(formated_query[
                                    'SELECT']))))[0]
                self.match = match(' '.join(formated_query['WHERE']))[0] if (
                    'WHERE' in formated_query.keys()) else None
                self.sort = order_filter(formated_query['ORDER']) if (
                    'ORDER' in formated_query.keys()) else None
                self.skip = skip(int(formated_query['SKIP'][0]))[0] if (
                    'SKIP' in formated_query.keys()) else None
                self.limit = limit(int(formated_query['LIMIT'][0]))[0] if (
                    'LIMIT' in formated_query.keys()) else None
                self.unwind = [unwind(obj)[0] for obj in unwind_filter(
                    coma_filter(formated_query['SELECT']))] if (
                    'SELECT' in formated_query.keys()) else None
                self.query = self.agregation_query()
            else:
                raise ValueError
        except ValueError:
            sys.exit('Stoped! Your projection is empty! Please try again.')

    def find_query(self):
        str_query = 'self.collection.find'
        if self.match is not None and self.show_fields is not None:
            str_query += '(self.match, self.show_fields)'
        elif self.show_fields is not None or self.match is not None:
            if self.show_fields is not None:
                str_query += '(self.show_fields)'
            else:
                str_query += '(self.match)'
        else:
            str_query += '()'
        if self.sort is not None:
            str_query += '.sort(self.sort)'
        if self.skip is not None:
            str_query += '.skip(self.skip)'
        if self.limit is not None:
            str_query += '.limit(self.limit)'
        query = eval(str_query)
        return query

    def agregation_query(self):
        query = list()
        query.append(self.project)
        if self.match is not None:
            query.append(self.match)
        if self.sort is not None:
            query.append(self.sort)
        if self.skip is not None:
            query.append(self.skip)
        if self.limit is not None:
            query.append(self.limit)
        if self.unwind is not None:
            for obj in self.unwind:
                query.append(obj)
        return self.collection.aggregate(query)
