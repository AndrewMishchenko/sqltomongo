def project_filter(projection):
    proj = dict()
    for obj in projection:
        if obj.endswith('.*'):
            obj = obj.replace('.*', '')
            proj[obj] = 1
        else:
            proj[obj] = 1
    return proj


def unwind_filter(projection):
    unw = list()
    for obj in projection:
        if obj.endswith('.*'):
            obj = (obj.replace('.*', '')).split('.')
            unw.append(obj[0])
        else:
            pass
    return (unw)
