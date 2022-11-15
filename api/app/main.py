from fastapi import FastAPI
from starlette_exporter import PrometheusMiddleware, handle_metrics

from .routers import v1

app = FastAPI()

app.add_middleware(PrometheusMiddleware, app_name='documents', prefix='documents')
app.add_route('/metrics', handle_metrics)

app.include_router(v1.documents.router)
