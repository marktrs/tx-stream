start-server:
	docker compose --profile server up -d --build

stop-server:
	docker compose --profile server down --rmi local --volumes

test:
	pytest --cov=flows tests/