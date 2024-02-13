-- DROP OWNED BY Administrator;
-- DROP OWNED BY Visitor;

DROP ROLE IF EXISTS Administrator;
DROP ROLE IF EXISTS Visitor;

CREATE ROLE Administrator LOGIN PASSWORD 'super';
CREATE ROLE Visitor LOGIN PASSWORD 'user';

GRANT postgres TO Administrator;
GRANT pg_read_all_data TO Visitor;

SELECT rolname
FROM pg_roles;


-- tests {
SET ROLE Visitor;
INSERT INTO personal_data (customer_name, customer_surname)
VALUES ('Посетитель', 'Посетитель');
--
SET ROLE Administrator;
INSERT INTO personal_data (customer_id, customer_name, customer_surname)
VALUES (1001, 'Админ', 'Админ');
DELETE
FROM personal_data
WHERE customer_id = 1001;
--
SET ROLE postgres;
-- tests }
