import json
from typing import Optional, Any, Union, Callable, Type, Dict

import pandas as pd
from pydantic import BaseModel


class DataFrameBaseModel(BaseModel):
    """
        This class deals with pydantic models with all attributes being of type pandas.dataframe,
        it adapts pydantic utilities (model.json(), Model.parse_obj)
    """

    class Config:
        arbitrary_types_allowed = True

    def json(
            self,
            *,
            include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
            exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            encoder: Optional[Callable[[Any], Any]] = None,
            **dumps_kwargs: Any,
    ) -> str:

        model_as_dict = {}
        for value in self.__fields__.values():
            if type(object.__getattribute__(self, value.name)) == pd.DataFrame:
                model_as_dict[value.name] = object.__getattribute__(self, value.name).to_json(orient='columns')
            elif type(object.__getattribute__(self, value.name)) == dict:
                # If serializing a dictionary -> value (DataFrame) is serialized using to_json
                if object.__getattribute__(self, value.name):
                    model_as_dict[value.name] = {key: val.to_json(orient='columns') for key, val in
                                                   object.__getattribute__(self, value.name).items()}
                else:
                    model_as_dict[value.name] = {}
            else:
                model_as_dict[value.name] = object.__getattribute__(self, value.name)
        return json.dumps(model_as_dict)

    @classmethod
    def parse_obj(cls: Type[BaseModel], obj: Any):

        obj_dict = {}
        for name in cls.__fields__.keys():
            # If parsing a dictionary -> value (DataFrame) is parsed using read_json
            if type(obj[name]) == dict:
                obj_dict[name] = {key: pd.read_json(val, orient="columns") for key, val in obj[name].items()}
            else:
                try:
                    obj_dict[name] = pd.read_json(obj[name], orient="columns")
                except Exception:
                    obj_dict[name] = obj[name]

        return cls(**obj_dict)

    def dict(
            self,
            *,
            include: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
            exclude: Union['AbstractSetIntStr', 'MappingIntStrAny'] = None,
            by_alias: bool = False,
            skip_defaults: bool = None,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
    ) -> Dict:
        """
            will convert all attributes, exclusion flags are ignored
        """
        model_as_dict = {}
        for value in self.__fields__.values():
            if type(object.__getattribute__(self, value.name)) == pd.DataFrame:
                model_as_dict[value.name] = object.__getattribute__(self, value.name).to_dict()
            elif type(object.__getattribute__(self, value.name)) == dict:
                # If converting to a dictionary -> value (DataFrame) is serialized using to_dict
                if object.__getattribute__(self, value.name):
                    model_as_dict[value.name] = {key: val.to_dict() for key, val in
                                                   object.__getattribute__(self, value.name).items()}
                else:
                    model_as_dict[value.name] = {}
            else:
                model_as_dict[value.name] = object.__getattribute__(self, value.name)
        return model_as_dict
