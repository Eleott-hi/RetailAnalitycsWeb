DROP MATERIALIZED VIEW IF EXISTS v_Customers;
DROP MATERIALIZED VIEW IF EXISTS v_Groups;
DROP FUNCTION IF EXISTS fnc_calc_group_margin;
DROP MATERIALIZED VIEW IF EXISTS v_Periods_Purchase_History;
DROP MATERIALIZED VIEW IF EXISTS v_Purchase_History;
DROP MATERIALIZED VIEW IF EXISTS v_Periods;
DROP MATERIALIZED VIEW IF EXISTS v_Info;
DROP FUNCTION IF EXISTS fnc_get_days;

CREATE OR REPLACE FUNCTION fnc_get_days(data interval)
    RETURNS NUMERIC
AS $$
    SELECT extract(EPOCH FROM data) / 86400.0 AS days;
$$ LANGUAGE SQL;

CREATE MATERIALIZED VIEW v_Info AS
SELECT TR.Transaction_ID,
       SKU.SKU_ID,
       CK.SKU_Summ,
       SKU.Group_ID,
       SKU.SKU_Name,
       CK.SKU_Amount,
       CR.Customer_ID,
       CK.SKU_Discount,
       CK.SKU_Summ_Paid,
       TR.Transaction_Summ,
       SR.SKU_Retail_Price,
       SR.SKU_Purchase_Price,
       TR.Transaction_DateTime,
       TR.Transaction_Store_ID
FROM Transactions AS TR
         JOIN Checks AS CK ON TR.Transaction_ID = CK.Transaction_ID
         JOIN Cards AS CR ON CR.Customer_Card_ID = TR.Customer_Card_ID
         JOIN SKU ON SKU.SKU_ID = CK.SKU_ID
         JOIN Stores AS SR ON SKU.SKU_ID = SR.SKU_ID AND TR.Transaction_Store_ID = SR.Transaction_Store_ID;

-- View 1
CREATE MATERIALIZED VIEW v_Customers AS
WITH table_grouped_customers AS
         (SELECT Customer_ID,
                 avg(Transaction_Summ)                                                                                                     AS Customer_Average_Check,
                 array_agg(Transaction_Store_ID ORDER BY Transaction_DateTime desc)                                                        AS Array_Stores,
                 fnc_get_days (max(Transaction_DateTime) - min(Transaction_DateTime))/ count(Transaction_ID)                               AS Customer_Frequency,
                 fnc_get_days ((SELECT Analysis_Date from Date_Of_Analysis_Formation ORDER BY 1 DESC LIMIT 1) - max(Transaction_DateTime)) AS Customer_Inactive_Period
          FROM v_Info
          GROUP BY Customer_ID),

     table_grouped_customers_segments AS
         (SELECT *,
                 Customer_Inactive_Period / Customer_Frequency AS Customer_Churn_Rate,
                 (CASE
                      WHEN (Customer_Inactive_Period / Customer_Frequency < 2) THEN 'Low'
                      WHEN (Customer_Inactive_Period / Customer_Frequency < 5) THEN 'Medium'
                      ELSE 'High' END)                         AS Customer_Churn_Segment,
                 (CASE
                      WHEN (percent_rank() OVER (ORDER BY Customer_Frequency, Customer_ID) <= 0.1) THEN 'Often'
                      WHEN (percent_rank() OVER (ORDER BY Customer_Frequency, Customer_ID) <= 0.35) THEN 'Occasionally'
                      ELSE 'Rarely' END)                       AS Customer_Frequency_Segment,
                 (CASE
                      WHEN (percent_rank() OVER (ORDER BY (CASE
                                                               WHEN Customer_Average_Check IS NULL THEN 0
                                                               ELSE Customer_Average_Check END) DESC, Customer_ID) <=
                            0.1) THEN 'High'
                      WHEN (percent_rank() OVER (ORDER BY (CASE
                                                               WHEN Customer_Average_Check IS NULL THEN 0
                                                               ELSE Customer_Average_Check END) DESC, Customer_ID) <=
                            0.35) THEN 'Medium'
                      ELSE 'Low' END)                          AS Customer_Average_Check_Segment
          FROM table_grouped_customers)

SELECT Customer_ID,
       Customer_Average_Check,
       Customer_Average_Check_Segment,
       Customer_Frequency,
       Customer_Frequency_Segment,
       Customer_Inactive_Period,
       Customer_Churn_Rate,
       Customer_Churn_Segment,
       Segment AS Customer_Segment,
       (CASE
            WHEN Array_Stores[1] = Array_Stores[2] AND Array_Stores[2] = Array_Stores[3]
                THEN Array_Stores[1]
            ELSE (SELECT Store
                  FROM (SELECT row_number() OVER () AS Row, * FROM (SELECT unnest(Array_Stores) AS Store) X) Y
                  ORDER BY count(*) OVER (PARTITION BY Store) DESC, row
                  LIMIT 1) END) AS Customer_Primary_Store
FROM table_grouped_customers_segments
         LEFT JOIN Segments  ON Segments.Average_Check = Customer_Average_Check_Segment
                            AND Segments.Purchase_Frequency = Customer_Frequency_Segment
                            AND Segments.Churn_Probability = Customer_Churn_Segment
ORDER BY 1;

-- View 2

CREATE MATERIALIZED VIEW v_Purchase_History AS
SELECT Transaction_ID,
       Customer_ID,
       Group_ID,
       Transaction_DateTime,
       sum(SKU_Purchase_Price * SKU_Amount) AS Group_Cost,
       sum(SKU_Summ)                        AS Group_Summ,
       sum(SKU_Summ_Paid)                   AS Group_Summ_Paid
FROM v_Info
GROUP BY Customer_ID, Transaction_ID, Transaction_DateTime, Group_ID;

-- View 3

CREATE MATERIALIZED VIEW v_Periods AS
SELECT *,
       (fnc_get_days (Last_Group_Purchase_Date - First_Group_Purchase_Date) + 1) / Group_Purchase AS Group_Frequency
FROM (SELECT Customer_ID,
             Group_ID,
             min(Transaction_DateTime)                                                      AS First_Group_Purchase_Date,
             max(Transaction_DateTime)                                                      AS Last_Group_Purchase_Date,
             count(Transaction_ID)                                                          AS Group_Purchase,
             coalesce(min(CASE WHEN SKU_Discount > 0 THEN SKU_Discount / SKU_Summ END), 0)  AS Group_Min_Discount
      FROM v_Info
      GROUP BY Customer_ID, Group_ID) X;

CREATE MATERIALIZED VIEW v_Periods_Purchase_History AS
SELECT VH.Group_ID,
       VH.Group_Cost,
       VH.Group_Summ,
       VH.Customer_ID,
       VH.Transaction_ID,
       VP.Group_Purchase,
       VP.Group_Frequency,
       VH.Group_Summ_Paid,
       VP.Group_Min_Discount,
       VH.Transaction_DateTime,
       VP.Last_Group_Purchase_Date,
       VP.First_Group_Purchase_Date
FROM v_Periods AS VP
         JOIN v_Purchase_History AS VH ON VH.Customer_ID = VP.Customer_ID
    AND VH.Group_ID = VP.Group_ID;

-- View 4
CREATE OR REPLACE FUNCTION fnc_calc_group_margin(IN model INT DEFAULT 1,
                                                 IN intrvl INTERVAL DEFAULT '5000 days'::interval,
                                                 IN lmt INT DEFAULT 100)
    RETURNS TABLE
            (
                Customer_ID  BIGINT,
                Group_ID     BIGINT,
                Group_Margin FLOAT
            )
AS
$$
DECLARE
    Analysis_Date TIMESTAMP := (SELECT Analysis_Date
                                FROM Date_Of_Analysis_Formation
                                ORDER BY 1 DESC
                                LIMIT 1);
BEGIN

    IF model NOT IN (1, 2) THEN
        RAISE EXCEPTION 'No such model';
    END IF;
    IF lmt <= 0 THEN
        RAISE EXCEPTION 'lmt <= 0';
    END IF;

    RETURN QUERY
        SELECT VPH.Customer_ID,
               VPH.Group_ID,
               coalesce(CASE
                            WHEN ($1 = 1) THEN
                                        sum(Group_Summ_Paid - Group_Cost)
                                        FILTER (WHERE Transaction_DateTime BETWEEN Analysis_Date - $2 AND Analysis_Date)
                            WHEN ($1 = 2) THEN (SELECT sum(GM)::float
                                                FROM (SELECT Group_Summ_Paid - Group_Cost AS GM
                                                      FROM v_Purchase_History AS VPH_2
                                                      WHERE VPH_2.Customer_ID = VPH.Customer_ID
                                                        AND VPH_2.Group_ID = VPH.Group_ID
                                                      ORDER BY Transaction_DateTime DESC
                                                      LIMIT $3) X) END, 0)
        FROM v_Purchase_History AS VPH
        GROUP BY 1, 2;
END ;
$$ LANGUAGE plpgsql;

CREATE MATERIALIZED VIEW v_Groups AS
WITH calc AS
         (SELECT Customer_ID,
                 Group_ID,
                 Group_Min_Discount                                                                                                     AS Group_Minimum_Discount,
                 sum(Group_Summ_Paid) over (PARTITION by Customer_ID, Group_ID)
                    / sum(Group_Summ) over (PARTITION by Customer_ID, Group_ID)                                                                                      AS Group_Average_Discount,
                 fnc_get_days((SELECT Analysis_Date FROM Date_Of_Analysis_Formation ORDER BY 1 DESC LIMIT 1) - Last_Group_Purchase_Date) / Group_Frequency AS Group_Churn_Rate,
                 abs(fnc_get_days( Transaction_DateTime - lag(Transaction_DateTime, 1)
                                                             OVER (PARTITION BY Customer_ID, Group_ID ORDER BY Transaction_DateTime)) -
                     Group_Frequency) / Group_Frequency                                                                                                        AS Pre_Group_Stability_Index,
                 Group_Purchase::float / (SELECT count(Transaction_ID)
                                          FROM v_Purchase_History AS VH
                                          WHERE VH.Customer_ID = VPPH.Customer_ID
                                            AND VH.Transaction_DateTime BETWEEN First_Group_Purchase_Date AND Last_Group_Purchase_Date) AS Group_Affinity_Index,
                 (SELECT count(Transaction_ID)
                  FROM v_Info
                  WHERE VPPH.Customer_ID = v_Info.Customer_ID
                    AND VPPH.Group_ID = v_Info.Group_ID
                    AND v_Info.SKU_Discount > 0) /
                 Group_Purchase::float                                                                                                  AS Group_Discount_Share
          FROM v_Periods_Purchase_History AS VPPH)

SELECT DISTINCT 
       C.Customer_ID,
       C.Group_ID,
       avg(Group_Affinity_Index)        AS Group_Affinity_Index,
       avg(Group_Churn_Rate)            AS Group_Churn_Rate,
       coalesce( avg(Pre_Group_Stability_Index),0 )  AS Group_Stability_Index,
       avg(Group_Margin)                AS Group_Margin,
       avg(Group_Discount_Share)        AS Group_Discount_Share,
       avg(Group_Minimum_Discount)      AS Group_Minimum_Discount,
       avg(Group_Average_Discount)      AS Group_Average_Discount
FROM calc C
         JOIN fnc_calc_group_margin() GM
              ON GM.Customer_ID = C.Customer_ID AND GM.Group_ID = C.Group_ID
GROUP BY C.Customer_ID, C.Group_ID
ORDER BY 1, 2;

-- Test query
SELECT * FROM v_Customers;
SELECT * from v_Periods ORDER BY 1,2;
SELECT * FROM v_Purchase_History ORDER BY 2,1;
SELECT * FROM v_Groups;
