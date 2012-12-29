def guarded(statement):
    try:
        return statement()
    except:
        return False
