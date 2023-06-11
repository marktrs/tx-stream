#!/bin/sh

set -e

prefect concurrency-limit create etherscan_rate_limit $ETHERSCAN_RATE_LIMIT

# # Deploy flows to Prefect server
prefect deployment build flows/historical_scan.py:scan_event_history -n production --apply --interval $FLOW_TRIGGER_INTERVAL
prefect deployment run scan_event_history/production

# prefect deployment build flows/cube.py:calculate_cube_surface_area -n production --apply --param cube_name=rubiks-cube
# prefect deployment run calculate-cube-surface-area/production

# prefect deployment build flows/health_check.py:health_check -n production --apply --interval $FLOW_TRIGGER_INTERVAL
# prefect deployment run health_check/production

# prefect deployment build flows/tx_scan_deployer.py:deploy_tx_scanner -n production --apply --params "{\"symbols\":\"WETH_USDC\",\"config\":{\"interval\":10}}"
# prefect deployment run deploy_tx_scanner/production


# Start the agent to run the flow
prefect agent start -p default-agent-pool

# Evaluating passed command:
exec "$@"