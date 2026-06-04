from logging.config import fileConfig
import os
import sys

from alembic import context
from sqlalchemy import engine_from_config, pool
from dotenv import load_dotenv

# =========================================================
# LOAD ENV
# =========================================================
load_dotenv()

# =========================================================
# PATH SETUP (make backend importable)
# =========================================================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

# =========================================================
# ALEMBIC CONFIG
# =========================================================
config = context.config

# logging is optional (DO NOT BREAK MIGRATIONS IF IT FAILS)
if config.config_file_name:
    try:
        fileConfig(config.config_file_name)
    except Exception:
        pass

# =========================================================
# IMPORT APP METADATA
# =========================================================
from backend.app.infrastructure.database.database import Base
import backend.app.infrastructure.database.models  # noqa: F401

# =========================================================
# DATABASE URL FROM .env
# =========================================================
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env")

config.set_main_option("sqlalchemy.url", DATABASE_URL)

target_metadata = Base.metadata

# =========================================================
# MIGRATION FUNCTIONS
# =========================================================

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()