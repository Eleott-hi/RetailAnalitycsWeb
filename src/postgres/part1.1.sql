SET DATESTYLE TO iso, DMY;

-- Insert into Roles table
INSERT INTO Roles (name) VALUES 
('admin'),
('user');

-- Insert into Users table
INSERT INTO Users (username, password, Role_ID, email) VALUES
('admin', '$2b$12$8/ut7olCV9P0ypwfNc8LpeLbPe3E9DaXayfnb4D5sXVnPhFUrLAEW', 1, 'admin@example.com'),
('user', '$2b$12$./Kyn1h7HaFP3dlBEgQ6M.VMrkLHfZ23T4bwFzbPZ5fbVscrdQXtm', 2, 'user@example.com');

CREATE OR REPLACE PROCEDURE prc_import_table(dir VARCHAR, table_name VARCHAR, del CHAR, mini BOOLEAN) AS
$$
DECLARE
    mini_suffix VARCHAR := (SELECT CASE WHEN mini THEN '_Mini' ELSE '' END);
    extansion   VARCHAR := (SELECT CASE WHEN del = ',' THEN '.csv' WHEN del = E'\t' THEN '.tsv' ELSE '' END);
    str_quary   VARCHAR := 'COPY ' || table_name || ' FROM ''' || dir || '/' || table_name || mini_suffix ||
                           extansion || ''' DELIMITER ''' || del || '''';
BEGIN
    RAISE NOTICE '%', str_quary;
    EXECUTE (str_quary);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE prc_export_table(dir VARCHAR, table_name VARCHAR, del CHAR) AS
$$
DECLARE
    extansion VARCHAR := (SELECT CASE WHEN del = ',' THEN '.csv' WHEN del = E'\t' THEN '.tsv' ELSE '' END);
    str_quary VARCHAR := 'COPY (select * from ' || table_name || ') TO ''' || dir || '/' || table_name || extansion ||
                         ''' DELIMITER ''' || del || '''';
BEGIN
    RAISE NOTICE '%', str_quary;
    EXECUTE (str_quary);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE prc_export(dir VARCHAR, del CHAR) AS
$$
DECLARE
    p_table RECORD;
BEGIN
    SET session_replication_role = replica;

    FOR p_table IN (SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'public')
        LOOP
            CALL prc_export_table(dir, translate(p_table::varchar, '()', ''), del);
        END LOOP;

    SET session_replication_role = origin;
END ;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE PROCEDURE prc_import(dir VARCHAR, del CHAR, mini BOOLEAN) AS
$$
DECLARE
    p_table   RECORD;
    str_table VARCHAR;
BEGIN
    SET session_replication_role = replica;

    FOR p_table IN (SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE table_schema = 'public')
        LOOP
            str_table := translate(p_table::varchar, '()', '');
            IF (str_table IN (lower('Roles'), lower('Users'))) THEN
                CONTINUE;
            ELSEIF (str_table = lower('Date_Of_Analysis_Formation') or str_table = lower('Segments')) THEN
                CALL prc_import_table(dir, str_table, del, false);
            ELSE
                CALL prc_import_table(dir, str_table, del, mini);
            END IF;
        END LOOP;
    SET session_replication_role = origin;

    PERFORM setval('Transactions_Transaction_ID_seq', (SELECT max(Transaction_ID) FROM Transactions), true);
    PERFORM setval('Personal_Data_Customer_ID_seq', (SELECT max(Customer_ID) FROM Personal_Data), true);
    PERFORM setval('Cards_Customer_Card_ID_seq', (SELECT max(Customer_Card_ID) FROM Cards), true);
    PERFORM setval('Group_SKU_Group_ID_seq', (SELECT max(Group_ID) FROM Group_SKU), true);
    PERFORM setval('SKU_SKU_ID_seq', (SELECT max(SKU_ID) FROM SKU), true);
END;
$$ LANGUAGE plpgsql;

CALL prc_import('/docker-entrypoint-initdb.d/datasets/', E'\t', mini := true);
-- CALL prc_export('/project', ',');

