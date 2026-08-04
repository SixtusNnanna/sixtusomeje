class ExistException(Exception):
    def __init__(self, name: str):
        super().__init__(f"{name} has been created")


class NotFoundExcept(Exception):
    def __init__(self, name: str):
        super().__init__(f"The {name} is not Found")


class NotZeroError(Exception):
    pass

class StatusCompletedError(Exception):
    pass

class SameWareHouseTransferError(Exception):
    pass

class InSufficentStockError(Exception):
   pass
