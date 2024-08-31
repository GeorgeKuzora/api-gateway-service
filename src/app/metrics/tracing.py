from fastapi import Request
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)


def is_business_route(path: str) -> bool:
    """Проверяет относится ли путь к бизнесс логике."""
    not_business_routes = [
        '/healthz/up',
        '/healthz/ready',
        '/metrics',
    ]
    return not any((path.startswith(route) for route in not_business_routes))


async def tracing_middleware(request: Request, call_next):
    """Создает спан для сервиса."""
    path = request.url.path
    if not is_business_route(path):
        return await call_next(request)
    try:
        span_ctx = global_tracer().extract(
            propagation.Format.HTTP_HEADERS, request.headers,
        )
    except (InvalidCarrierException, SpanContextCorruptedException):
        span_ctx = None
    span_tags = {
        tags.SPAN_KIND: tags.SPAN_KIND_RPC_SERVER,
        tags.HTTP_METHOD: request.method,
        tags.HTTP_URL: str(request.url),
    }
    with global_tracer().start_active_span(
        f'api_gateway_{request.method}_{path}',
        child_of=span_ctx,
        tags=span_tags,
    ) as scope:
        response = await call_next(request)
        scope.span.set_tag(tags.HTTP_STATUS_CODE, response.status_code)
        return response
