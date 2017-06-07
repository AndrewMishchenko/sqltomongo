from sqltomongo.exceptions import SqmongoComparisonError


def comparison_converter(operator):
    if not isinstance(operator, str):
        raise SqmongoComparisonError(operator)
    else:
        if operator == '=':
            return '=='
        elif operator == '<>':
            return '!='
        elif operator == '>' or operator == '>=' or operator == '<' or operator == '<=':
            return operator
        elif not operator:
            raise SqmongoComparisonError(operator)
        else:
            raise SqmongoComparisonError(operator)
