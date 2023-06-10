#!/bin/sh

set -e

prefect concurrency-limit create etherscan_rate_limit $ETHERSCAN_RATE_LIMIT

# # Deploy flows to Prefect server
prefect deployment build flows/historical_scan.py:scan_event_history -n prod --apply --interval $FLOW_TRIGGER_INTERVAL
prefect deployment run scan_event_history/prod

prefect deployment build flows/health_check.py:health_check -n prod --apply --interval $FLOW_TRIGGER_INTERVAL
prefect deployment build flows/health_check.py:health_check -n prod --apply --params "{\"name\":\"Marvin\",\"num\":42,\"url\":\"https://catfact.ninja/fact\"}"

prefect deployment run health_check/prod

# Start the agent to run the flow
prefect agent start -p default-agent-pool

# Evaluating passed command:
exec "$@"