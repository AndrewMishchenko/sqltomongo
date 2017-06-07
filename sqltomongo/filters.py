from pymongo import ASCENDING, DESCENDING

from sqltomongo.keywords import KEYWORDS


def coma_filter(list_with_coma):
    if not isinstance(list_with_coma, list):
        raise ValueError("The type of list_with_coma must be a list")
    else:
        return [obj.replace(KEYWORDS['COMA'], '') for obj in list_with_coma]


def project_filter(projection):
    if not isinstance(projection, list):
        raise ValueError("The type of project_filter must be a list")
    else:
        proj = dict()
        for obj in projection:
            if obj.endswith('.*'):
                obj = obj.replace('.*', '')
                proj[obj] = 1
            elif obj == KEYWORDS['ASTERISK']:
                proj = obj
                break
            else:
                proj[obj] = 1
        return proj


def unwind_filter(projection):
    if not isinstance(projection, list):
        raise ValueError("The type of unwind_filter must be a list")
    else:
        unw = list()
        for obj in projection:
            if obj.endswith('.*'):
                obj = (obj.replace('.*', ''))  # .split('.')
                unw.append(obj)
            else:
                pass
        return unw


def order_filter(order_list):
    if not isinstance(order_list, list):
        raise ValueError("The type of order must be a list")
    else:
        filtered = dict()
        key = ''
        for obj in coma_filter(order_list):

            if obj.upper() == 'ASC':
                obj = ASCENDING
            elif obj.upper() == 'DESC':
                obj = DESCENDING
            else:
                key = obj
                continue
            filtered[key] = obj
        return {'$sort': filtered}


def order_filter_find(order_list):
    """
    Get dirty format of ordering expression and zip it into normal.
    :param o_list: list of tuples in format [('value_to_order', 1/-1)]
    :return: filtered ordering expression
    """
    if not isinstance(order_list, list):
        raise ValueError("The type of order must be a list")
    else:
        filtered_list = list()
        for obj in coma_filter(order_list):
            if obj.upper() == 'ASC':
                obj = ASCENDING
            elif obj.upper() == 'DESC':
                obj = DESCENDING
            filtered_list.append(obj)
        filtered_list = iter(filtered_list)
        filtered_list = [i for i in zip(filtered_list, filtered_list)]
        return filtered_list
