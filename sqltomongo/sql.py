from sqltomongo.comparisons import comparison_converter
from sqltomongo.keywords import KEYWORDS


class Checker(object):
    def __init__(self, string):
        self.splited_sql = self.spliter(string)

    def spliter(self, string):
        if not isinstance(string, str):
            raise ValueError("The type of SQL must be a str")
        else:
            return string.split(' ')

    def parse(self):
        if self.splited_sql[0].upper() == 'SELECT':
            return self.parse_select(self.splited_sql)
        else:
            pass

    @staticmethod
    def parse_first(parsed_sql):
        if not isinstance(parsed_sql, dict):
            raise ValueError("The type of SQL must be a dict")
        else:
            for obj in parsed_sql.keys():
                if obj.upper() in KEYWORDS['DML']:
                    return obj.upper()
            else:
                pass

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
