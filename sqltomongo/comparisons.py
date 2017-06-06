from sqltomongo.exceptions import SqmongoComparisonError


def comparison_converter(operator):
    try:
        if operator == '=':
            operator = '=='
        elif operator == '<>':
            operator = '!='
        elif operator == '>' or '>=' or '<' or '<=':
            pass
        else:
            raise SqmongoComparisonError
    except SqmongoComparisonError:
        pass
    else:
        return operator
