#!/bin/sh

set -e

# Define global concurrency limits
prefect concurrency-limit create etherscan_rate_limit $ETHERSCAN_RATE_LIMIT

# Deploy tx_scanner config flows to Prefect server
prefect deployment build flows/tx_scanner.py:tx_scanner -n $SYMBOLS --apply --params "{\"symbols\":\"$SYMBOLS\",\"pool_addr\":\"$POOL_CONTRACT\",\"initial_block\":$INITIAL_BLOCK,\"block_range\":$BLOCK_RANGE,\"event_topic\":\"$EVENT_TOPIC\",\"result_offset\":$RESULT_OFFSET}"

# Deploy deployer flows to Prefect server (with this deployer we can resuse the same flow for all pairs)
prefect deployment build flows/tx_scan_deployer.py:tx_scan_deployer -n deploy-symbol-scanner --apply --params "{\"symbols\":\"$SYMBOLS\",\"pool_addr\":\"$POOL_CONTRACT\",\"initial_block\":$INITIAL_BLOCK,\"block_range\":$BLOCK_RANGE,\"event_topic\":\"$EVENT_TOPIC\",\"result_offset\":$RESULT_OFFSET, \"polling_interval_sec\":$POLLING_INTERVAL_SEC}"

# Start deployer to deploy subflows (tx_scanner)
prefect deployment run tx_scan_deployer/deploy-symbol-scanner

# Start the agent to execute the flow and schedule the task
prefect agent start -p default-agent-pool

# Evaluating passed command:
exec "$@"