from typing import Dict, List, Union
from serializers.item import ItemJSON

StoreJSON = Dict[str, Union[int, str, List[ItemJSON]]]
