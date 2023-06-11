#!/bin/sh

set -e

# Define global concurrency limits
prefect concurrency-limit create etherscan_rate_limit $ETHERSCAN_RATE_LIMIT
# Deploy tx_scanner config flows to Prefect server
prefect deployment build flows/historical_scan.py:scan_event_history -n WETH_USDC --apply 
# Deploy deployer flows to Prefect server (with this deployer we can resuse the same flow for all pairs)
prefect deployment build flows/tx_scan_deployer.py:deploy_tx_scanner -n WETH_USDC --apply --params "{\"symbols\":\"WETH_USDC\",\"config\":{\"interval\":$FLOW_TRIGGER_INTERVAL}}"
# Start deployer to deploy subflows (tx_scanner)
prefect deployment run deploy_tx_scanner/WETH_USDC
# Start the agent to execute the flow and schedule the task
prefect agent start -p default-agent-pool

# Evaluating passed command:
exec "$@"