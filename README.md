## Локальная разработка

Установка виртуального окружения и пакетов:
```shell
python3 -m virtualenv .venv
source .venv/bin/activate
python3 -m pip install -r requirements/base.txt
```

Запуск сервер разработки и окружения:

```shell
source .venv/bin/activate

make docker_dev
make run
```
