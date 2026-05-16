SCRIPT_DIR=$(dirname "$0")
alembic -c /app/alembic.ini upgrade head
cd /app/src
python "${SCRIPT_DIR}/main.py"