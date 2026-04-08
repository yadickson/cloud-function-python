from dataclasses import asdict
from typing import Any

from dacite import Config, from_dict

from app.domain.model.config_model import ConfigModel
from app.infrastructure.mapper.config_merge_mapper_interface import ConfigMergeMapperInterface


class ConfigMergeMapper(ConfigMergeMapperInterface):
    def merge(self, left: ConfigModel, right: ConfigModel) -> ConfigModel:
        merge = asdict(left, dict_factory=self.exclude_none_factory) | asdict(right, dict_factory=self.exclude_none_factory)
        return from_dict(data_class=ConfigModel, data=merge, config=Config(allow_missing_fields_as_none=True))

    @staticmethod
    def exclude_none_factory(data: Any) -> dict:
        return {key: value for key, value in data if value}
