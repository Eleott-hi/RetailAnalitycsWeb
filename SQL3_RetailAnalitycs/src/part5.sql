CREATE OR REPLACE FUNCTION fnc_personal_offers_aimed_at_increasing_frequency_of_visits(first_date TIMESTAMP,
                                                                                       last_date TIMESTAMP,
                                                                                       add_transactions INT,
                                                                                       max_churn_rate NUMERIC,
                                                                                       max_discount_share NUMERIC,
                                                                                       margin NUMERIC)
    RETURNS TABLE
            (
                Customer_ID                 BIGINT,
                Start_Date                  TIMESTAMP,
                End_Date                    TIMESTAMP,
                Required_Transactions_Count NUMERIC,
                Group_Name                  VARCHAR,
                Offer_Discount_Depth        NUMERIC
            )
AS $$
BEGIN RETURN QUERY
        WITH X AS (SELECT VC.Customer_ID,
                          VG.Group_ID,
                          VG.Group_Affinity_Index,
                          ceil(VG.group_minimum_discount * 20) / 20                                                         AS Offer_Discount_Depth,
                          margin / 100.0 * Group_Margin / sum(Group_Cost) OVER (PARTITION BY VC.Customer_ID, VG.Group_ID)   AS Max_Discount,
                          round(fnc_get_days(last_date - first_date) / Customer_Frequency) + add_transactions               AS Required_Transactions_Count
                   FROM v_Customers AS VC
                            JOIN v_Groups AS VG ON VG.Customer_ID = VC.Customer_ID
                            JOIN v_Purchase_History AS PH ON PH.Customer_ID = VC.Customer_ID
                                                         AND PH.Group_ID = VG.Group_ID
                   WHERE Group_Churn_Rate <= max_churn_rate
                     AND Group_Discount_Share <= max_discount_share / 100.0)

        SELECT DISTINCT X.Customer_ID,
                        first_date,
                        last_date,
                        first_value(X.Required_Transactions_Count)          OVER (PARTITION BY X.Customer_ID ORDER BY Group_Affinity_Index DESC),
                        first_value(GS.Group_Name)                          OVER (PARTITION BY X.Customer_ID ORDER BY Group_Affinity_Index DESC),
                        first_value(round(X.Offer_Discount_Depth * 100))    OVER (PARTITION BY X.Customer_ID ORDER BY Group_Affinity_Index DESC)
        FROM X
            JOIN Group_SKU AS GS ON X.Group_ID = GS.Group_ID
        WHERE X.Offer_Discount_Depth < Max_Discount
          AND X.Offer_Discount_Depth > 0
        ORDER BY 1;

END;
$$ LANGUAGE plpgsql;


-- Test query

SELECT *
FROM fnc_personal_offers_aimed_at_increasing_frequency_of_visits(
    first_date           := '2022-08-18 00:00:00',
    last_date            := '2022-08-18 00:00:00',
    add_transactions     := 1, 
    max_churn_rate       := 3,
    max_discount_share   := 70,
    margin               := 30
);
