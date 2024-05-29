import os


DB_USER = os.environ.get("DB_USER") or "task"
DB_PASSWORD = os.environ.get("DB_PASSWORD") or 1
DB_HOST = os.environ.get("DB_HOST") or  "localhost"
DB_PORT = os.environ.get("DB_PORT") or 5432
DB_NAME = os.environ.get("DB_NAME") or "task"


POSTGRESQL_DATABASE_URI = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
SQLITE_DATABASE_URI = f"sqlite:///{DB_NAME}.db"
