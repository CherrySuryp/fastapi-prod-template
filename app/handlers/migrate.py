import sys

sys.path.append("/opt")

import alembic.config


def handler(event: dict, context: dict) -> None:
    alembicArgs = [
        "--raiseerr",
        "upgrade",
        "head",
    ]
    alembic.config.main(argv=alembicArgs)
