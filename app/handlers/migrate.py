import sys

sys.path.append("/opt")

import alembic.config


def handler(event, context):
    try:
        print("Start")

        alembicArgs = [
            "--raiseerr",
            "upgrade",
            "head",
        ]
        alembic.config.main(argv=alembicArgs)

        return {"statusCode": 200, "body": "Migration completed successfully"}
    except Exception as e:
        print(f"Error details: {str(e)}")
        return {"statusCode": 500, "body": f"Migration failed: {str(e)}"}
