class ValidationError(ValueError):
    pass

class NotFoundError(LookupError):
    pass

class ConflictError(RuntimeError):
    pass

class StateError(RuntimeError):
    pass
