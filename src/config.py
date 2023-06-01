import os
import typing as tp

from dotenv import load_dotenv
from sqlalchemy.engine import URL

load_dotenv()

POSTGRES_INDEXES_NAMING_CONVENTION = {
    'all_column_names': lambda constraint, table: '_'.join([
        column.name for column in constraint.columns.values()
    ]),
    'ix': 'ix__%(table_name)s__%(all_column_names)s',
    'uq': 'uq__%(table_name)s__%(all_column_names)s',
    'ck': 'ck__%(table_name)s__%(constraint_name)s',
    'fk': 'fk__%(table_name)s__%(all_column_names)s__%(referred_table_name)s',
    'pk': 'pk__%(table_name)s'
}


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Secrets(metaclass=Singleton):
    @staticmethod
    def str2bool(str_val: tp.Union[bool, str]):
        """Converts str boolean value to python bool"""
        if isinstance(str_val, bool):
            return str_val

        _str_val = str_val.strip().lower()
        if _str_val == 'true':
            return True
        if _str_val == 'false':
            return False

        raise ValueError('Boolean value expected.')

    @property
    def PG_DSN(self) -> URL:
        pg_dsn: URL = URL.create(
            drivername="postgresql+asyncpg",
            username=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            database=os.getenv("PG_DB")
        )
        return pg_dsn

    @property
    def DEBUG_MODE(self) -> bool:
        _value = os.getenv('DEBUG_MODE')
        return False if _value is None else self.str2bool(_value)

    @property
    def PG_POOL_SIZE(self) -> int:
        _pool_size = os.getenv('PG_POOL_SIZE')
        return int(_pool_size)

    @property
    def JWT_SECRET(self) -> str:
        return str(os.getenv('JWT_SECRET'))

    @property
    def PG_SCHEMA(self) -> str:
        return str(os.getenv('PG_SCHEMA'))
