class ListSocket:
    @classmethod
    def getDefaultValue(cls):
        raise NotImplementedError()

    @classmethod
    def getFromValuesCode(cls):
        raise NotImplementedError()

    @classmethod
    def getJoinListsCode(cls):
        raise NotImplementedError()

    @classmethod
    def getReverseCode(cls):
        raise NotImplementedError()

class PythonListSocket(ListSocket):
    @classmethod
    def getDefaultValue(cls):
        return []

    @classmethod
    def getDefaultValueCode(cls):
        return "[]"

    @classmethod
    def getFromValuesCode(cls):
        return "value"

    @classmethod
    def getJoinListsCode(cls):
        return "list(itertools.chain(value))"

    @classmethod
    def getReverseCode(cls):
        return "list(reversed(value))"

class CythonListSocket(ListSocket):
    listClass = None

    @classmethod
    def getDefaultValue(cls):
        return cls.listClass()

    @classmethod
    def getDefaultValueCode(cls):
        return cls.listClass.__name__ + "()"

    @classmethod
    def getCopyExpression(cls):
        return "value.copy()"

    @classmethod
    def getFromValuesCode(cls):
        return cls.listClass.__name__ + ".fromValues(value)"

    @classmethod
    def getJoinListsCode(cls):
        return cls.listClass.__name__ + ".join(value)"

    @classmethod
    def getReverseCode(cls):
        return "value.reversed()"

    @classmethod
    def correctValue(cls, value):
        if isinstance(value, cls.listClass):
            return value, 0
        try: return cls.listClass.fromValues(value), 1
        except: return cls.getDefaultValue(), 2
