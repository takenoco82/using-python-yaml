.PHONY: run
run: stop
	docker-compose up -d --remove-orphans

.PHONY: stop
stop:
	docker-compose stop
	docker-compose rm -f
