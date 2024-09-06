from pydantic import BaseModel


class NoExtra(BaseModel, extra='forbid'):
    pass
