# Метрика рэди пробы для сервиса

```
sum by(status) (kuzora_auth_ready_count_total{method="GET"})
```

# Метрика по продолжительности запросов

```
histogram_quantile(0.95, sum by(le) (rate(kuzora_auth_request_duration_bucket{service="auth-service"}[$__rate_interval])))
```

# Метрика по количеству запросов в разрезе эндпоинтов и статус кодов

```
sum by(status, endpoint) (kuzora_auth_request_count_total{service="auth-service"})
```

# Метрика по количеству успешных/неуспешных попыток авторизации

```
count(kuzora_auth_auth_success_count_total{status="200"})
```

```
count(kuzora_auth_auth_failure_count_total{status!="200"})
```
