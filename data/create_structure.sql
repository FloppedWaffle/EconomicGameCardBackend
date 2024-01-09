-- PostgreSQL скрипт для создания структуры базы данных.

CREATE DATABASE economicgame;

\c economicgame;

CREATE TABLE IF NOT EXISTS players(
    player_id SERIAL PRIMARY KEY,
    nfc_uid VARCHAR(32) NOT NULL UNIQUE,
    firstname VARCHAR(32) NOT NULL,
    lastname VARCHAR(32) NOT NULL,
    grade VARCHAR(16) NOT NULL,
    balance INTEGER NOT NULL,
    tax_paid INTEGER NOT NULL,
    company_id INTEGER NOT NULL,
    is_founder INTEGER NOT NULL,
    is_minister INTEGER NOT NULL,
    is_minister_paid INTEGER
);


CREATE TABLE IF NOT EXISTS teachers(
    teacher_id SERIAL PRIMARY KEY,
    nfc_uid VARCHAR(32) NOT NULL UNIQUE,
    password VARCHAR(64) NOT NULL UNIQUE,
    firstname VARCHAR(32) NOT NULL,
    middlename VARCHAR(32) NOT NULL,
    subject_name VARCHAR(256) NOT NULL UNIQUE,
    balance INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS companies(
    company_id SERIAL PRIMARY KEY,
    password VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(256) NOT NULL UNIQUE,
    balance INTEGER NOT NULL,
    profit INTEGER NOT NULL,
    taxes INTEGER NOT NULL,
    is_state INTEGER NOT NULL
);


CREATE TABLE IF NOT EXISTS services(
    service_id SERIAL PRIMARY KEY,
    company_id INTEGER NOT NULL,
    name VARCHAR(64) NOT NULL UNIQUE,
    quantity INTEGER NOT NULL,
    cost INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS bankers(
    banker_id SERIAL PRIMARY KEY,
    password VARCHAR(64) NOT NULL UNIQUE
);