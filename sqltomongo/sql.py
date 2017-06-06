from sqltomongo.keywords import KEYWORDS
from sqltomongo.comparisons import comparison_converter


class Checker(object):
    def __init__(self, string):
        self.splited_sql = self.spliter(string)

    def spliter(self, string):
        if not isinstance(string, str):
            raise ValueError("The type of SQL must be a str")
        else:
            return string.split(' ')

    def check_first_dml(self):
        if self.splited_sql[0].upper() == 'SELECT':
            return self.parse_select(self.splited_sql)
        else:
            pass

    def parse(self):
        if self.check_first_dml() == 'SELECT':
            return self.parse_select(self.splited_sql)

    def parse_select(self, sql):
        if not isinstance(sql, list):
            raise ValueError("The type of SQL must be a list")
        else:
            key = None
            parsed_sql = dict()
            for obj in sql:
                if obj.upper() in KEYWORDS['DML']:
                    key = obj.upper()
                    parsed_sql[key] = []
                    continue
                elif obj.upper() in KEYWORDS['KEYWORD']:
                    if obj.upper() in KEYWORDS['LOGIC']:
                        parsed_sql[key].append(obj)
                        continue
                    elif obj.upper() == "BY":
                        continue
                    key = obj.upper()
                    parsed_sql[key] = []
                elif obj.upper() in KEYWORDS['SKIP']:
                    key = obj.upper()
                    parsed_sql[key] = []
                elif obj in KEYWORDS['COMPARISONS']:
                    operator = comparison_converter(obj)
                    parsed_sql[key].append(operator)
                elif key == "ORDER":
                    parsed_sql[key].append(obj)
                elif obj.upper() in KEYWORDS['LIMIT']:
                    key = obj.upper()
                    parsed_sql[key] = []
                else:
                    parsed_sql[key].append(obj)
            return parsed_sql
