import configparser
from dataclasses import dataclass


@dataclass
class DB:
    user: str
    password: str
    host: str
    port: int
    db_name: str


@dataclass
class AppConfig:
    db_cfg: DB


def load_config(path: str = 'cfg.ini') -> AppConfig:
    config = configparser.ConfigParser()
    config.read(path)

    return AppConfig(
        db_cfg=DB(**config["db"])
    )
