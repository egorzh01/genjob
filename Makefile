# 1. Включаем файл .env, если он существует
# ifneq ($(wildcard .env),)
#     include .env
#     # Экспортируем все переменные, которые только что прочитали
#     export $(shell sed 's/=.*//' .env)
# endif

MIGRATIONS_DIR?=./migrations

DB_URL=postgres://postgres:postgres@localhost:5432/genjob?sslmode=disable

# Команда для создания новых файлов миграции (запуск: make migrate-create name=init_users)
migrate-create:
	migrate create -ext sql -dir $(MIGRATIONS_DIR) -seq $(name)

# Накатить все миграции (запуск: make migrate-up)
migrate-up:
	migrate -path $(MIGRATIONS_DIR) -database "$(DB_URL)" up

# Откатить последнюю миграцию (запуск: make migrate-down)
migrate-down:
	migrate -path $(MIGRATIONS_DIR) -database "$(DB_URL)" down 1

# Принудительно установить версию (нужно, если база заблокировалась со статусом dirty)
migrate-force:
	migrate -path $(MIGRATIONS_DIR) -database "$(DB_URL)" force $(v)
