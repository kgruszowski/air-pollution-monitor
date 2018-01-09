DROP DATABASE IF EXISTS airpollutionmonitor;
DROP ROLE IF EXISTS air;
CREATE ROLE air WITH LOGIN;
CREATE DATABASE airpollutionmonitor WITH OWNER air;
GRANT ALL PRIVILEGES ON DATABASE airpollutionmonitor TO air;
\c airpollutionmonitor air localhost
DROP TABLE IF EXISTS stations;
CREATE TABLE stations(
	id SERIAL,
	vendor VARCHAR(5),
	stationid INTEGER,
	stationname VARCHAR(200),
	lng NUMERIC,
	lat NUMERIC,
	city VARCHAR(20),
	street VARCHAR(60),
		CONSTRAINT pk_stations PRIMARY KEY (id)
);
DROP TABLE IF EXISTS monitoring;
CREATE TABLE monitoring(
	id SERIAL,
	stationid INTEGER,
	pm2_5 NUMERIC,
	pm10 NUMERIC,
	temp NUMERIC,
	date TIMESTAMP WITHOUT TIME ZONE,
		CONSTRAINT pk_monitoring PRIMARY KEY (id),
		CONSTRAINT fk_monitoring_stations FOREIGN KEY (stationid) REFERENCES stations(id)
);
