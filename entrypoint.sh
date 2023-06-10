#!/bin/sh

set -e

# # Deploy flows to Prefect server
prefect deployment build flows/historical_scan.py:scan_historical_event -n prod --apply --interval 2
prefect deployment run scan_historical_event/prod

prefect deployment build flows/health_check.py:health_check -n prod --apply
prefect deployment run health_check/prod

# Start the agent to run the flow
prefect agent start -p default-agent-pool

# Evaluating passed command:
exec "$@"