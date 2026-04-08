from dacite import Config, from_dict

from app.domain.model.config_model import ConfigModel
from app.infrastructure.mapper.config_mapper_interface import ConfigMapperInterface


class ConfigMapper(ConfigMapperInterface):
    def get_configuration(self, config: dict) -> ConfigModel:
        environment = {k.lower().strip(): str(v).strip() if v else v for k, v in config.items()}
        return from_dict(data_class=ConfigModel, data=environment, config=Config(allow_missing_fields_as_none=True))
