import cmd
import signal
import sys

from sqltomongo.builders import Router
from sqltomongo.database import DatabaseConnection
from sqltomongo.keywords import KEYWORDS
from sqltomongo.sql import Checker


class SqltomongoCli(cmd.Cmd):
    def do_start(self, database, host, port):
        self.connection = DatabaseConnection(database, host, port)
        self.print_count = 20

    def do_use(self, database):
        self.connection.use_db(database)

    def do_auth(self, args):
        auth = args.strip('()')
        clean_auth = list()
        for obj in auth.split(','):
            if ' ' in obj:
                obj = obj.replace(' ', '')
            if "'" in obj:
                obj = obj.replace("'", '')
            if '"' in obj:
                obj = obj.replace('"', '')
            clean_auth.append(obj)
        self.connection.authenticate(clean_auth[0], clean_auth[1])

    def default(self, line):
        try:
            if Checker.spliter(line)[0].upper() in KEYWORDS['DML']:
                try:
                    if self.connection.database is not None:
                        parsed_sql = Checker(line)
                        router = Router(self.connection, parsed_sql.parse())
                        self.result = [item for item in router.query]
                        self.st_index = 0
                        self.end_index = self.print_count
                        self.print_result(self.result, self.st_index,
                                          self.end_index
                                          )
                        if len(self.result) > self.print_count:
                            print('Type "it" for more')
                    else:
                        print('At first you must connect to the database '
                              'with use method!'
                              )
                except KeyError:
                    print('Something went wrong! Please check the request!')
        except Exception as err:
            print(err)

    def print_result(self, a, st_index, end_index):
        for i in a[st_index: end_index]:
            print(i)
        self.st_index = end_index
        self.end_index += self.print_count

    def do_it(self, line):
        try:
            self.print_result(self.result, self.st_index, self.end_index)
            if len(self.result) - self.st_index >= self.print_count:
                print('Type "it" for more')
        except AttributeError:
            print('At first you must enter the query!')

    def do_result_count(self, args):
        self.print_count = int(args)
        print('Count of results - {}'.format(args))

    def do_db(self, args):
        try:
            print(self.connection.database.name)
        except Exception as err:
            print('At first you must connect to the database '
                              'with use method!')

    def do_quit(self, args):
        """Quits the program."""
        print('bye')
        raise SystemExit

    def cmdloop(self, intro=None):
        while True:
            try:
                super(SqltomongoCli, self).cmdloop()
                self.postloop()
                break
            except KeyboardInterrupt:
                self.do_quit('')


def handler(signum, frame):
    SqltomongoCli().do_quit('')


signal.signal(signal.SIGTSTP, handler)


def main():
    try:
        database = sys.argv[1]
    except IndexError:
        database = None
    try:
        host = sys.argv[2]
    except IndexError:
        host = 'localhost'
    try:
        port = int(sys.argv[3])
    except IndexError:
        port = 27017

    prompt = SqltomongoCli()
    print('Sqltomongo shell version v0.1')
    prompt.do_start(database, host, port)
    prompt.prompt = '> '
    prompt.cmdloop()


if __name__ == '__main__':
    main()
