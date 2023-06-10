CREATE EXTENSION citext;

CREATE TABLE public.events (
    "time" integer,
    tx_from citext COLLATE pg_catalog."default",
    tx_to citext COLLATE pg_catalog."default",
    gas bigint,
    gas_price bigint,
    total_fee bigint,
    block integer,
    value numeric,
    contract_to citext COLLATE pg_catalog."default",
    tx_hash citext COLLATE pg_catalog."default",
    PRIMARY KEY (tx_hash)
);

CREATE TABLE public.health ("ok" boolean) TABLESPACE pg_default;

CREATE INDEX tx_hash_index ON public.events USING btree (tx_hash) TABLESPACE pg_default;

CREATE INDEX block_index ON public.events USING btree (block) TABLESPACE pg_default;

CREATE INDEX contract_to_index ON public.events USING btree (contract_to COLLATE pg_catalog."default") TABLESPACE pg_default;

CREATE INDEX tx_from_index ON public.events USING btree (tx_from COLLATE pg_catalog."default") TABLESPACE pg_default;

CREATE INDEX tx_to_index ON public.events USING btree (tx_to COLLATE pg_catalog."default") TABLESPACE pg_default;

CREATE VIEW current_block as
SELECT
    MAX(block)
FROM
    public.events;

INSERT INTO
    public.health(status)
VALUES
    (true);