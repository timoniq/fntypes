class UnwrapError(TypeError):
    def __init__(self, err):
        self.err = err

__all__ = ("UnwrapError",)
