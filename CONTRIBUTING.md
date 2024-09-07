# API-Gateway-Service

## Структура проекта

- `CHANGELOG.md` — файл с описанием изменений в проекте. Используется для отслеживания истории изменений в коде.
- `CONTRIBUTING.md` — файл с инструкциями для участников проекта. Содержит информацию о том, как вносить свой вклад в проект.
- `README.md` — файл с описанием проекта. Используется для предоставления информации о проекте.
- `pyproject.toml` — файл конфигурации Poetry. Используется для настройки сборки и зависимостей проекта.
- `poetry.lock` — файл блокировки зависимостей. Используется Poetry для обеспечения воспроизводимости сборки.
- `setup.cfg` — файл конфигурации setuptools. Используется для настройки сборки и публикации проекта.
- `Dockerfile` — файл для создания образа Docker контейнера.
- `.dockerignore` — файл для игнорирования файлов и директорий в ходе сборки Docker контейнера.
- `docker-compose.yml` - файл для развертывания приложения в виде сервисов docker-compose.
- `.gitlab-ci` - файл пайплайна gitlab ci-cd.
- `src/` — директория с исходным кодом проекта.
  - `app/` — директория с кодом приложения.
  - `config/` - директория с конфигурационными файлами приложения.
  - `tests/` — директория с тестами приложения.
- `manifests/` - директория с манифестами ресурсов kubernetes.
- `helm/` - директория с чартами helm.
- `configs/` - директория с конфигурациями внешних инструментов.
- `grafana/` - директория с примерами графиков grafana.

## Разработка и запуск проекта в devcontainer.

### Требования для разработки проекта в Devcontainer

Для разработки проекта используется рабочее окружение настроенное внутри devcontainer.

В зависимости от используемой операционной системы некоторые шаги и команды могут отличаться. В этом случае обращайтесь к версии документации для вашей операционной системы.

Для работы над проектом в devcontainer необходимо:

- Для Windows: рекомендуется использовать [WSL](https://virgo.ftc.ru/pages/viewpage.action?pageId=1084887269).
- Установить Docker Desktop для MacOS/Windows или просто docker для Linux. [Docker Desktop](https://www.docker.com/products/docker-desktop/).
- Установить [Visual Studio Code](https://code.visualstudio.com/download).
-  [Настроить Visual Studio Code и Docker для использования Devcontainers](https://code.visualstudio.com/docs/devcontainers/containers#_getting-started).
  - Необходимые плагины VS Code:
    - `ms-vscode-remote.remote-containers`
    - `ms-azuretools.vscode-docker`
- Установить Git
- Установить OpenSSH с SSH Agent.
- [Настроить Git и SSH для работы в Devcontainer](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials)
- Установить OpenSSL
- Установить [Шрифты для powerlevel10k](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#fonts)
- [Установить шрифт Meslo Nerd Font для CLI в терминале](https://github.com/romkatv/powerlevel10k?tab=readme-ov-file#fonts)
- По необходимости установить и настроить kubectl, внутри контейнера будут использованы настройки с хоста
- Склонировать этот репозиторий на рабочую станцию
- Открыть директорию с репозиторием через Visual Studio Code
- Ввести `Ctrl+Shift+P` или `Cmd+Shift+P` и выбрать `Dev Containers: Rebuild and Reopen in Container`

### Подготовка рабочего окружения

Если какие-то из дальнейших пунктов у вас уже выполнены, смело пропускайте шаг.

После установки необходимого ПО:
- Сгенерируйте SSH ключ и добавьте его в свой MosHub аккаунт
- Настройте `user.name` и `user.email` для Git
- [Настройте SSH Agent c вашим ключом](https://code.visualstudio.com/remote/advancedcontainers/sharing-git-credentials)
- Склонируйте текущий репозиторий в локальную директорию, если еще не сделали этого

Для настройки kubernetes:
- Сгенерируйте ключи для kubectl и положите их в папку `~/.kube`
- Настройте kubectl на использование ключей из папки `~/.kube`

После настройки локального окружения:
- Откройте директорию в Visual Studio Code
- Нажмите `Ctrl+Shift+P` или `Cmd+Shift+P`
- Введите `Dev Containers:`
- Выберите из предложенных вариантов пункт `Dev Containers: Rebuild and Reopen in Container`
- Дождитесь открытия проекта внутри окружения в Devcontainer

### Окружение доступное после старта Devcontainer

После старта контейнера будут доступны следующие преднастроенные возможности:

#### Преднастроенная конфигурация для запуска линтера

  Доступ из командной панели:

  - Нажмите `Ctrl+Shift+P` или `Cmd+Shift+P`
  - Выберете `Tasks: Run Task`
  - Выберете `Flake8`, `MyPy`, или `ISort`

#### Преднастроенная конфигурация для запуска тестов

Смотрите по кнопке `Testing` в боковой панели Visual Studio Code.

#### Преднастроенная конфигурация для запуска сервиса

  Смотрите по кнопке `Run and Debug` в боковой панели Visual Studio Code.

- `Zsh` с Oh-My-Zsh в качестве shell по-умолчанию
- базовые консольные инструменты вроде `git`, `curl` и прочие
- `kubectl` и `helm` для работы с kubernetes
- `python` версии 3.12 с `poetry` для управления зависимостями и виртуальным окружением
- настроен доступ до `docker` на хосте

## Запуск приложения в Docker контейнере

Для приложения создан [Dockerfile](./Dockerfile).

Для запуска приложения в Docker контейнере необходимо:

Установить Docker Desktop для MacOS/Windows или просто docker для Linux. [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Выполнить команду `docker build` для сборки образа контейнера:

```shell
docker build -t api-gateway:latest .
```

Для создания и запуска контейнера выполните команду `docker run`:

```shell
docker run --name api-gateway -p 127.0.0.1:8084:8000 api-gateway
```

Приложение будет доступно на порту `127.0.0.1:8084`.

## Запуск проекта в docker-compose

Для приложения создан [файл docker-compose.yml](./docker-compose.yml).

Для запуска проекта в docker-compose необходимо:

Установить Docker Desktop для MacOS/Windows или просто docker для Linux. [Docker Desktop](https://www.docker.com/products/docker-desktop/).

Клонировать проект в локальную директорию:

```shell
git clone https://hub.mos.ru/shift-python/y2024/homeworks/gkuzora/api-gateway-service.git
```

Открыть директорию корень проекта:

```shell
cd <путь-к-проекту>
```

Переключиться на необходимую ветку git:

```shell
git checkout <имя-нужной-ветки>
```

Инициализировать и обновить сабмодули проекта:

```shell
git submodule init && \
git submodule update --remote
```

После выполнения команд выше, директории сабмодулей должны содержать необходимые файлы для работы с микросервисами, в том числе Dockerfile.

Запустить сборку проекта в docker-compose:

```shell
docker compose up -d
```

Docker скачает соберет и запустит контейнеры. Чтобы посмотреть запущенные контейнеры выполните команду:

```shell
docker container list
```

Сервисы будут доступны по адресам:

- face-verification-service - `127.0.0.1:8081`
- transaction-service -  `127.0.0.1:8082`
- auth-service -  `127.0.0.1:8083`
- api-gateway-service -  `127.0.0.1:8084`

## Запуск сервиса в kubernetes

Для работы приложения в kubernetes созданы манифесты ресурсов kubernetes - `manifests`.

Для того чтобы запустить необходимые ресурсы в кластере kubernetes выполните следующие команды:

```shell
kubectl apply -f manifests/pvc.yml
kubectl apply -f manifests/configMap.yml
kubectl apply -f manifests/service.yml
kubectl apply -f manifests/deployment.yml
kubectl apply -f manifests/job.yml
```

Для упрощения работы с манифестами kubernetes создан пакет чартов helm. Для установки приложения в kubernetes при помощи helm выполните команду:

```shell
helm install kuzora-api-gateway ./kuzora-api-gateway
```
