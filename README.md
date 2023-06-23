# EVM Transaction Indexer

Table of Contents

- [About the Project](#about-the-project)
- [Notes](#notes)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
    - [Run Test](#run-test)
- [System Design](#system-design)
- [Project Layout](#project-layout)
- [Next Steps](#next-steps)
- [Guides](#guides)
- [Appendix](#appendix)

## About the project

The purpose of the project is to create a robust API server and Interactive Web application to track transaction fee history in the Uniswap V3 USDC/ETH pool, specifically focusing on recording the transaction fee in USDT when each transaction is confirmed on the blockchain.

It supports real-time data recording and historical batch data recording, allowing continuous capture of live data and retrieval of past transactions. The system provides extensive RESTful APIs that support horizontal/vertical filters, pagination, ordering, and composite queries.

Additionally, It provides a client application that allows users to query transactions by ID/hash and time range, displaying a paginated list of transactions with customizable pagination options.

## Notes

To prevent the limitation of external APIs and extends the usability, This project has pre-indexed transaction swap event data of Uniswap V3 USDC/ETH pool from block 12376729 (contract deployment block) on the Ethereum mainnet. To start quickly you can either import provided .csv file from [here](https://github.com/marktrs/tx-stream/tree/main/data) to your database or start running the service from your own block number by running the indexer flow with the `start_block` parameter (default initial block was set to 12376729) see Appendix Section for more details. If default initial block was used, this can take up to 40 mins to reach latest block according to etherscan API rate limit.

## API documentation

For full API document [please checkout this section](https://github.com/marktrs/tx-stream/tree/main/apidoc)

## Getting Started

To start using this application on local hosted server you need to clone this repository along with [the submodule repository](https://github.com/marktrs/txfee-history-client) where the web client application is located.

```
git clone --recurse-submodules https://github.com/marktrs/txfee-history-client.git
```

This project is using Git submodule to allows managing dependencies in a larger Git repository, referencing other repositories as subdirectories while maintaining separate version control and revision history for each.

## Prerequisites

To build using docker:

- Docker [Docker](https://www.docker.com/)

To build from source without docker:

- Installed [Python 3.11.4](https://www.python.org/downloads/) for API server testing, building from source.
- Installed [Node.JS 18](https://nodejs.org/dist/v18.16.1/) for NextJS client application building on local.
- Installed Postgres with a user configuration from the [environment variable file](https://github.com/marktrs/simple-todo/blob/main/.env.example)

## Usage

Using docker compose

1. Create .env file from .env.example and fill in the environment variables such as ETHERSCAN_API_KEY

```sh
$ cp .env.example .env
```

2. Start all services

```shell
$ make start-server
```

This will start following services:

```shell
- PostgreSQL: Persistence data store
- PostgREST: RESTful API web server for PostgreSQL
- Prefect server & Prefect Agent: Dataflow automation and worker
- NextJS: Client application
```

3. Checkout Prefect Server Dashboard on [http://localhost:4200/flow-runs/](http://localhost:4200/flow-runs/)

This pre-configured dashboard will allow you to:

- Start a new flow run with parameters (e.g. index new event topic on the different pool) concurrently.
- Monitor flow run history status and metrics to identify bottlenecks and optimize performance.
- Retry failed flow run and debugging with logs

4. Then navigate to the web application on [http://localhost:8080/](http://localhost:8080/) to try out the web application dashboard

### Stop all services

This command will remove all running containers, local images, and volumes

```sh
$ make stop-server
```

### Run Test

Run unit testing from source

```sh
make test
```

<!-- TODO: complete instruction -->

## System Design

This project is designed for scalability and extensibility. It allows you to add new data sources and processing steps as needed. For example, with the current implementation, you can add:

1. New DEX and Pool by adding a new flow deployment with a different contract address.
2. New event topic by adding new flow deployment with different event topics.

In terms of reliability and availability, the system is designed to be highly available and scalable. It uses a distributed task execution where workflows in Prefect are standalone objects that can be run at any time. Fault-tolerant scheduling is a crucial feature in Prefect that ensures the reliability and availability of data pipelines, especially in production environments.

For more detail, The following section will explain the use case of 3 main components: API server, Dataflow automation, and client application and documentation of the API server.

### API Server - PostgREST

Using PostgREST eliminating the need for custom API servers and object-relational mapping. It establishes a single source of truth by putting the data itself at the center. With declarative programming, PostgreSQL handles data joins and permissions effortlessly, reducing the complexity of coding. It offers a leak-proof abstraction, bypassing the need for ORMs and allowing efficient API creation using SQL. In short, it streamlines database-centric operations and empowers administrators to build APIs efficiently.

### Dataflow Automation - Prefect

To establish efficient data pipelines, Workflow management tool with a web-based UI and API is required. It must supports parallel task execution, flexible task definition, and error handling. With a graphical interface, it must provides visibility into pipeline workflows and offers fault-tolerant scheduling. Prefect enables dynamic and parameterized workflows, task caching for faster development, and includes robust error-handling features. It's a reliable and adaptable choice for managing workflows efficiently.

### Client Application - NextJS

This project require framework that support client-side and server-side rendering, optimized with static and dynamic rendering. NextJS simplifies data fetching with async/await support and aligns with React and the Web Platform. With enhanced TypeScript support, including improved type checking and efficient compilation, it provides a seamless development experience. NextJS provides additional structure, features, and optimizations for your application, abstracting and configuring tooling like bundling and compiling, allowing you to focus on building your app without the hassle of setup.

### API Documentation - Open API

This project use the OpenAPI specification to document the API server's endpoints and responses to provides a clear and standardized way of describing the API, Enables the automatic generation of documentation and client libraries, which can save significant development time and effort and provides a machine-readable format that can be used for automated testing.

## Project Layout

```
.
├── apidoc
│   └── ...
├── client
│   └── ...
├── docker
│   └── data
├── flows
│   ├── indexer
│   │   └── ...
│   └── ...
├── migrations
│   └── init.sql
├── tests
│   └── ...
├── Dockerfile
├── Makefile
├── README.md
├── docker-compose.yaml
├── pyproject.toml
├── requirements.txt
└── entrypoint.sh
```

`apidoc`: Contains OpenAPI specification and Swagger JSON files

`client`: Contains the client-side code or files, included frontend code, static assets, or other components related to the user interface.

`docker`: Docker container volume data

`flows`: Contains Prefect workflow, modeled as a Python function.

`flows/indexer` Contains python modules (`etherscan.py`, `event_parser.py`, `scanner.py`, `store.py`, and `utils.py`) responsible for indexing and processing data from external sources.

`migrations`: Contains SQL migration files for initialize database schema and structure.

`tests`: Unit testing for flows runner and related modules.

`root directory`: Contains miscellaneous files, including Makefile, Dockerfile, and shell scripts for deployment

## Next Steps

- `Caching`
  - Application Caching - Route base caching on client server to reduce the number of requests to the database and improve the performance of the application.
  - PostgREST API Server Schema Cache - Some PostgREST features need metadata from the database schema. Getting this metadata requires expensive queries. To avoid repeating this work, PostgREST uses a schema cache.
  - Database caching - PostgreSQL has a built-in caching mechanism that caches data in memory. It is called the shared buffer cache, and it is managed by the PostgreSQL buffer manager. The buffer manager is responsible for reading data from disk into memory, writing changed data back to disk, and maintaining the integrity of the in-memory data.
- `Testing` More coverage test beside core functionalities
- `gRPC` to provide more efficient binary protocol, which can result in faster and more efficient communication between client and server
- `Event decoding ` Decode transaction event data to get more information about the transaction

## Guides

> **Deploy new event topic indexer**

You can create a new flow run with a parameter to index a new event topic on different pool concurrently by following these steps:

1. Using Prefect Server Dashboard UI

- Navigate to (http://localhost:4200/flows)[http://localhost:4200/flows] and locate to `deploy_symbol_scanner` flow
- Click on `:` > `Quick run` button and fill in the parameter > Click `Run` button
- The new deployment will be add to queue. You can monitor the flow run status on the `Flow Runs` tab
- See available deployment configurations ![Flow deployment configuration](https://github.com/marktrs/tx-stream/tree/main/apidoc/assets/deployment.png)

2. Using Prefect CLI

```
// attach to prefect-agent container
$ docker exec -it prefect-agent bash

// edit following parameters to match your needs, see .env.example file for reference
$ export SYMBOLS=
$ export POOL_CONTRACT=
$ export INITIAL_BLOCK=
$ export BLOCK_RANGE=
$ export EVENT_TOPIC=
$ export RESULT_OFFSET=
$ export POLLING_INTERVAL_SEC=


// create a new deployment for above symbol / pool / event topic
$ prefect deployment build flows/tx_scan_deployer.py:tx_scan_deployer -n deploy-symbol-scanner --apply --params "{\"symbols\":\"$SYMBOLS\",\"pool_addr\":\"$POOL_CONTRACT\",\"initial_block\":$INITIAL_BLOCK,\"block_range\":$BLOCK_RANGE,\"event_topic\":\"$EVENT_TOPIC\",\"result_offset\":$RESULT_OFFSET, \"polling_interval_sec\":$POLLING_INTERVAL_SEC}"

// run the new deployment
$ prefect deployment run tx_scan_deployer/deploy-symbol-scanner
```

> **Set concurrency limit**

1. Using Prefect Server Dashboard UI

- Navigate to (http://localhost:4200/concurrency-limits)[http://localhost:4200/concurrency-limits] and locate to `Task Run Concurrency Limits` concurrency limit
- Click on `+` > fill in the parameter > Click `Add` button
- The new concurrency limit will be set. New task run will use this value as limit
- See available concurrency limit configurations ![Concurrency limit configuration](https://github.com/marktrs/tx-stream/tree/main/apidoc/assets/concurrency-limit.png)

2. Using Prefect CLI

```
// attach to prefect-agent container
$ docker exec -it prefect-agent bash

// edit following parameters to match your needs, see .env.example file for reference
$ export ETHERSCAN_RATE_LIMIT=

// set a new concurrency limit
$ prefect concurrency-limit create etherscan_rate_limit $ETHERSCAN_RATE_LIMIT
```

## Appendix

1.  [Docker](https://docs.docker.com/)
2.  [PostgREST](https://postgrest.org/en/v7.0.0/)
3.  [Prefect](https://docs.prefect.io/core/)
4.  [NextJS](https://nextjs.org/docs/getting-started)
5.  [OpenAPI Specification](https://swagger.io/specification/)
