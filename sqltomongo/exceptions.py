class SqmongoConnectionError(Exception):
    """Connection faild with None database"""

    def __init__(self, db, msg=None):
        if msg is None:
            print('Inputed name o database is "{}". Please try again.'.format(db))
        super(SqmongoConnectionError, self).__init__(msg)
        self.db = db


class SqmongoComparisonError(Exception):
    """Raised when comparison isn't in comparison_converter"""

    def __init__(self, comparison, msg=None):
        if msg is None:
            print('There is no equal comparison to "{} ". Please check and try again'.format(comparison))
        super(SqmongoComparisonError, self).__init__()
        self.comparison = comparison