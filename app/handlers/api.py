from mangum import Mangum

from app.main import app as fastapi_app

handler = Mangum(fastapi_app, api_gateway_base_path="/test", lifespan="auto")
