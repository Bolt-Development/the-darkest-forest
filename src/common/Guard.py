def guarded(statement, callback=None):
    try:
        valid = statement()
        if not callback is None:
            callback(valid)
        return valid
    except:
        return False
