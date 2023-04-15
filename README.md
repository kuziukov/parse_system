# parse_system


##### Конфигурация файла .env

```
DEBUG=True
RABBIT_URI=amqp://user:pass@rabbit_mq:5672/
```

##### Команды управления проектом описаны в Makefile
###### Основные из них

```
make install - установить зависимости
make run - запустить приложение (local)
make check - проверка кода
make test - запуск тестов

make docker-image - сборка проекта
make docker-run - запуск проекта в контейнерах
```
