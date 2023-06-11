from prefect import flow, task, get_run_logger

from health_check import health_check
from prefect.deployments import Deployment, run_deployment
from prefect.server.schemas.schedules import IntervalSchedule


@flow
def create_deployment(symbols: str, interval: int):
    return Deployment.build_from_flow(
        flow=health_check,
        name=symbols,
        version=1,
        work_pool_name="default-agent-pool",
        schedule=(IntervalSchedule(interval=interval)),
    )


@flow
def apply_deployment(deployment):
    deployment.apply()


@flow
def run_tx_scanner_deployment(symbols: str, config: dict):
    run_deployment(
        name=f"health_check/{symbols}",
        flow_run_name="health_check",
        parameters={
            "config": config,
        },
    )


@flow(name="deploy_tx_scanner")
def deploy_tx_scanner(symbols: str, **config):
    deployment = create_deployment(symbols=symbols, interval=config.get("interval", 10))
    apply_deployment(deployment)
    run_tx_scanner_deployment(symbols, config)


if __name__ == "__main__":
    deploy_tx_scanner(symbols="WETH_USDC", config={"interval": 10})
