CREATE DATABASE vulndb;

CREATE TABLE cve(
    id serial NOT NULL PRIMARY KEY,
    data jsonb NOT NULL
);

CREATE INDEX cve_id ON cve USING gin ((data->'id'));

CREATE TABLE cpe(
    id serial NOT NULL PRIMARY KEY,
    data jsonb NOT NULL
);

CREATE INDEX cpe_name_id ON cpe USING gin ((data->'cpeNameId'));

CREATE TABLE osv(
    id serial NOT NULL PRIMARY KEY,
    ecosystem VARCHAR(64) NOT NULL DEFAULT '',
    data jsonb NOT NULL
);

CREATE INDEX osv_id ON osv USING gin((data->'id'));
CREATE INDEX osv_alias_id ON osv USING gin((data->'aliases'));
