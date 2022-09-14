class Config:
    TESTING: bool = False
    DEBUG: bool = False
    SECRET_KEY: str = ""
    TOKEN_EXPIRE: int = 1  # in days
    SALT: str = "pwqgj12asdfl"  # Please don't change after app started, u can change it in configs below


class ProductionCfg(Config):
    SECRET_KEY = ""  # set here your secret key, more in README.md


class DevelopmentCfg(Config):
    DEBUG = True
    SECRET_KEY = "2d9a54239b3b6c6f334dc13f951416f5885b473d8796b67179741940a35d47aa"


class TestingCfg(Config):
    DEBUG = True
    TESTING = True
    SECRET_KEY = "c117b2c0a00d97f76bbb843ffe45006c5dcf682a158722de91a35b11c2aa5bf0"
