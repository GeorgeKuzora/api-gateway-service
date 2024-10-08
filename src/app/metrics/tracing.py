from typing import Any

from fastapi import Request
from jaeger_client.config import Config
from jaeger_client.tracer import Tracer
from opentracing import (
    InvalidCarrierException,
    SpanContextCorruptedException,
    global_tracer,
    propagation,
    tags,
)

from config.config import get_settings


def get_tracer() -> Tracer | None:
    """Создает трейсер."""
    settings = get_settings().tracing
    if not settings.enabled:
        return None
    config = Config(
        config={
            'sampler': {
                'type': settings.sampler_type,
                'param': settings.sampler_param,
            },
            'local_agent': {
                'reporting_host': settings.agent_host,
                'reporting_port': settings.agent_port,
            },
            'logging': settings.logging,
        },
        service_name=settings.service_name,
        validate=settings.validate,
    )
    return config.initialize_tracer()


def is_business_route(path: str) -> bool:
    """
    Проверяет относится ли путь к бизнес логике.

    :param path: Путь к URI.
    :type path: str
    :return: относится ли путь к бизнес логике приложения.
    :rtype: bool
    """
    not_business_routes = [
        '/healthz/up',
        '/healthz/ready',
        '/metrics',
    ]
    return not any((path.startswith(route) for route in not_business_routes))


async def tracing_middleware(request: Request, call_next) -> Any:
    """
    Создает спан для сервиса.

    :param request: Объект запроса к сервису.
    :type request: Request
    :param call_next: Следующая за middleware функция обработчик.
    :type call_next: Callable
    :return: Ответ от следующей за middleware функцией обработчиком.
    :rtype: Response
    """
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
