
CREATE OR REPLACE FUNCTION fnc_personal_offers_aimed_at_cross_selling(
    IN groups INT,
    IN max_churn_rate NUMERIC,
    IN max_stability_index NUMERIC,
    IN max_sku_share NUMERIC,
    IN max_margin_share NUMERIC)
RETURNS TABLE (
    Customer_ID BIGINT,
    SKU_Names VARCHAR,
    Offer_Discount_Depth NUMERIC
)
AS
$$
BEGIN
    RETURN QUERY
        WITH Store_Group_PrimeSKU AS (
            SELECT DISTINCT 
                Group_ID,
                SKU_Name,
                transaction_store_id,
                first_value(
                    (sku_retail_price - sku_purchase_price) * max_margin_share / 100.0 / sku_retail_price
                ) OVER (
                    PARTITION by transaction_store_id, Group_ID 
                    ORDER BY sku_retail_price - sku_purchase_price DESC
                ) AS Discount,
                first_value(s.sku_id) OVER (
                    PARTITION BY transaction_store_id, Group_ID 
                    ORDER BY sku_retail_price - sku_purchase_price DESC
                ) AS Prime_SKU
            FROM 
                stores S
            JOIN 
                SKU ON S.sku_id = SKU.sku_id
        ),

        Customer_Groups_PrimeSKU AS (
            SELECT 
                SKU_Name,
                Prime_SKU,
                VG.Group_ID,
                VG.Customer_ID,
                ceil(Group_Minimum_Discount * 20) / 20 AS Offer_Discount_Depth,
                row_number() OVER (
                    PARTITION BY VG.Customer_ID 
                    ORDER BY Group_Affinity_Index, VG.Group_ID DESC
                ) AS Row
            FROM 
                v_Groups AS VG
            JOIN 
                v_Customers AS VC ON VC.Customer_ID = VG.Customer_ID
            JOIN 
                Store_Group_PrimeSKU AS SGP ON VC.Customer_Primary_Store = SGP.transaction_store_id
                                             AND VG.Group_ID = SGP.Group_ID
            WHERE 
                Group_Churn_Rate <= max_churn_rate
                AND Group_Stability_Index < max_stability_index
                AND ceil(Group_Minimum_Discount * 20) / 20 <= SGP.Discount
        ),

        X AS (
            SELECT 
                CGP.SKU_Name,
                CGP.Customer_ID,
                CGP.Offer_Discount_Depth,
                count(Transaction_ID) FILTER (
                    WHERE sku_id = Prime_SKU
                ) OVER (
                    PARTITION BY CGP.Customer_ID, CGP.Group_ID
                ) / count(Transaction_ID) OVER (
                    PARTITION BY CGP.Customer_ID, CGP.Group_ID
                )::float AS part
            FROM 
                Customer_Groups_PrimeSKU AS CGP
            JOIN 
                v_Info ON v_Info.Customer_ID = CGP.Customer_ID 
                        AND CGP.Group_ID = v_Info.Group_ID
            WHERE 
                CGP.Row <= groups
        )

    SELECT DISTINCT 
        X.Customer_ID,
        X.SKU_Name,
        round(X.Offer_Discount_Depth * 100, 2) AS Offer_Discount_Depth
    FROM 
        X
    WHERE 
        X.part <= max_sku_share / 100
    ORDER BY 
        1, 
        2;

END;
$$ LANGUAGE plpgsql;




-- Test query

SELECT *
FROM fnc_personal_offers_aimed_at_cross_selling(
    groups              := 3,
    max_churn_rate      := 3,
    max_stability_index := 0.5,
    max_sku_share       := 100,
    max_margin_share    := 30
);

SELECT fnc_personal_offers_aimed_at_cross_selling('3', '3', '0.5', '100', '30', Customer_ID, SKU_Names, Offer_Discount_Depth)
