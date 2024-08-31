import logging
import os
from functools import lru_cache
from pathlib import Path
from typing import Self

import yaml
from pydantic_settings import BaseSettings

logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Ошибка конфигурации сервиса."""


class TracingSettings(BaseSettings):
    """Конфигурация трейсинга."""

    enabled: bool = False
    sampler_type: str = 'const'
    sampler_param: int = 1
    agent_host: str = 'jaeger'
    agent_port: int = 6831
    service_name: str = 'api-gateway-service'
    logging: bool = True
    validate: bool = True


class Settings(BaseSettings):
    """Конфигурация приложения."""

    localhost: str
    auth_host: str
    auth_port: str
    transactions_host: str
    transactions_port: str
    tracing: TracingSettings

    @classmethod
    def from_yaml(cls, file_path) -> Self:
        """Создает объект класса из файла yaml."""
        if not cls._is_valid_path(file_path):
            logger.critical(
                f'config file {file_path} not found',
            )
            raise ConfigError(
                f'config file {file_path} not found',
            )
        with open(file_path, 'r') as settings_file:
            settings = yaml.safe_load(settings_file)
        return cls._create_instance(settings)

    @classmethod
    def _is_valid_path(cls, path: str) -> bool:
        passlib_path = Path(path)
        return passlib_path.is_file()

    @classmethod
    def _create_instance(cls, settings) -> Self:
        conf = {
            'localhost': settings.get('localhost'),
            'auth_host': settings.get('authentification').get('host'),
            'auth_port': settings.get('authentification').get('port'),
            'transactions_host': settings.get('transactions').get('host'),
            'transactions_port': settings.get('transactions').get('port'),
            'tracing': settings.get('tracing'),
        }
        return cls(**conf)


@lru_cache
def get_settings():
    """Создает конфигурацию сервиса."""
    config_path_env_var = 'CONFIG_PATH'
    config_file = os.getenv(config_path_env_var)
    return Settings.from_yaml(config_file)
