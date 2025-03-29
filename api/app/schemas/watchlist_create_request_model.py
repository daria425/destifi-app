from pydantic import BaseModel, ConfigDict
from typing import List
class Equity(BaseModel):
    name:str
    symbol:str
    model_config=ConfigDict(extra='allow')

class Watchlist(BaseModel):
    equities: List[Equity]
    watchlist_name: str
    model_config=ConfigDict(extra='allow')


class WatchlistCreateRequestModel(BaseModel):
    uid: str
    watchlist: Watchlist



    