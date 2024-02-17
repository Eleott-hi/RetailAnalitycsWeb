-- DROP DATABASE IF EXISTS Retail_Analitycs;
-- CREATE DATABASE Retail_Analitycs;
--  DROP SCHEMA public CASCADE;
--  CREATE SCHEMA public;

DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE IF NOT EXISTS Roles
(
    ID SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS Users
(
    ID SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(256) NOT NULL,
    Role_ID INTEGER REFERENCES Roles (ID),
    email VARCHAR(50) UNIQUE
);


CREATE TABLE IF NOT EXISTS Personal_Data
(
    Customer_ID            BIGSERIAL PRIMARY KEY,
    Customer_Name          VARCHAR(100) NOT NULL CHECK (Customer_Name ~ '^([А-Я][- а-я]+)|([A-Z][- a-z]+)$'),
    Customer_Surname       VARCHAR(100) NOT NULL CHECK (Customer_Surname ~ '^([А-Я][- а-я]+)|([A-Z][- a-z]+)$'),
    Customer_Primary_Email VARCHAR(100) UNIQUE CHECK (Customer_Primary_Email ~ '^\w+([-.'']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$'),
    Customer_Primary_Phone VARCHAR(12) UNIQUE CHECK (Customer_Primary_Phone ~ '[+7][0-9]{10}')
);

CREATE TABLE IF NOT EXISTS Cards
(
    Customer_Card_ID SERIAL PRIMARY KEY,
    Customer_ID      BIGINT REFERENCES Personal_Data (Customer_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Group_SKU
(
    Group_ID   SERIAL PRIMARY KEY,
    Group_Name VARCHAR UNIQUE NOT NULL CHECK (Group_Name ~ '^[- A-zА-я0-9_\/]+$')
);

CREATE TABLE IF NOT EXISTS SKU
(
    SKU_ID   SERIAL PRIMARY KEY,
    SKU_Name VARCHAR(100) NOT NULL CHECK (SKU_Name ~ '^[- A-zА-я0-9_\/]+$'),
    Group_ID BIGINT REFERENCES Group_SKU (Group_ID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS Stores
(
    Transaction_Store_ID BIGINT  NOT NULL CHECK (Transaction_Store_ID > 0),
    SKU_ID               BIGINT REFERENCES SKU (SKU_ID) ON DELETE CASCADE,
    SKU_Purchase_Price   NUMERIC NOT NULL CHECK (SKU_Purchase_Price >= 0),
    SKU_Retail_Price     NUMERIC NOT NULL CHECK (SKU_Purchase_Price >= 0),

    CONSTRAINT unique_transaction_store_id_sku_id UNIQUE (Transaction_Store_ID, SKU_ID)
);

CREATE TABLE IF NOT EXISTS Transactions
(
    Transaction_ID       SERIAL PRIMARY KEY,
    Customer_Card_ID     BIGINT REFERENCES Cards (Customer_Card_ID) ON DELETE CASCADE,
    Transaction_Summ     NUMERIC,
    Transaction_DateTime TIMESTAMP WITHOUT TIME ZONE,
    Transaction_Store_ID BIGINT
);

CREATE TABLE IF NOT EXISTS Checks
(
    Transaction_ID BIGINT REFERENCES Transactions (Transaction_ID) ON DELETE CASCADE,
    SKU_ID         BIGINT REFERENCES SKU (SKU_ID) ON DELETE CASCADE,
    SKU_Amount     NUMERIC NOT NULL CHECK (SKU_Amount > 0),
    SKU_Summ       NUMERIC NOT NULL CHECK (SKU_Summ >= 0),
    SKU_Summ_Paid  NUMERIC NOT NULL CHECK (SKU_Summ_Paid >= 0),
    SKU_Discount   NUMERIC NOT NULL CHECK (SKU_Discount >= 0)
);

CREATE TABLE IF NOT EXISTS Date_Of_Analysis_Formation
(
    Analysis_Date TIMESTAMP WITHOUT TIME ZONE
);

CREATE TABLE IF NOT EXISTS Segments
(
    Segment            SERIAL PRIMARY KEY,
    Average_Check      VARCHAR(50) NOT NULL CHECK (Average_Check IN ('Low', 'Medium', 'High')),
    Purchase_Frequency VARCHAR(50) NOT NULL CHECK (Purchase_Frequency IN ('Often', 'Occasionally', 'Rarely')),
    Churn_Probability  VARCHAR(50) NOT NULL CHECK (Churn_Probability IN ('Low', 'Medium', 'High')),

    CONSTRAINT unique_Average_Check_Purchase_Frequency_Churn_Probability UNIQUE (Average_Check, Purchase_Frequency, Churn_Probability)
);

