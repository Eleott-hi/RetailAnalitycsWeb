-- Средний чек по заданному периоду.
--
CREATE OR REPLACE FUNCTION fn_avg_check_by_period(customer BIGINT, first_date DATE, last_date DATE)
    RETURNS NUMERIC
    LANGUAGE sql
AS
$$
SELECT sum(t.transaction_summ) / count(t.transaction_id) AS avg_check_sum
FROM transactions t
         INNER JOIN cards c ON c.customer_card_id = t.customer_card_id
WHERE t.transaction_datetime BETWEEN first_date AND last_date
  AND c.customer_id = customer
$$;

-- Средний чек по заданному количеству последних транзакций.
--
CREATE OR REPLACE FUNCTION fn_avg_check_by_tr_count(customer BIGINT, tr_count INT)
    RETURNS NUMERIC
    LANGUAGE sql
AS
$$
SELECT avg(t.transaction_summ) AS avg_check_sum
FROM transactions t
         INNER JOIN cards c ON c.customer_card_id = t.customer_card_id
WHERE c.customer_id = customer
GROUP BY customer_id
ORDER BY customer_id
LIMIT tr_count;
$$;

-- Округление в верхнюю сторону с шагом в 5%
--
CREATE OR REPLACE FUNCTION fn_round_ceil(n NUMERIC)
    RETURNS NUMERIC
    LANGUAGE plpgsql
AS
$$
BEGIN
    RETURN ceil(n * 20) / 20.0;
END
$$;

-- Вспомогательная функция (общая часть).
--
CREATE OR REPLACE FUNCTION fn_common_part(customer BIGINT,
                                            max_churn_rate NUMERIC,
                                            tr_with_discount NUMERIC,
                                          margin_rate NUMERIC,
                                          OUT group_name VARCHAR, OUT discount NUMERIC)
    LANGUAGE sql
AS
$$
SELECT gs.group_name                            AS group_name,
       fn_round_ceil(vg.group_minimum_discount) AS discount
FROM v_groups vg
         INNER JOIN group_sku gs ON vg.group_id = gs.group_id
        JOIN (SELECT customer_id,
                     group_id,
                     SUM(group_cost) AS group_cost
              FROM v_purchase_history
              GROUP BY customer_id,
                       group_id) AS foo
             ON foo.customer_id = vg.customer_id
                 AND foo.group_id = vg.group_id
WHERE vg.customer_id = customer
  AND vg.group_churn_rate <= max_churn_rate
  AND vg.group_discount_share < tr_with_discount
  AND fn_round_ceil(vg.group_minimum_discount) < vg.group_margin / group_cost * margin_rate
ORDER BY vg.group_affinity_index DESC
LIMIT 1;
$$;

-- Выбор группы для вознаграждения.
--
CREATE OR REPLACE FUNCTION fn_group(customer BIGINT, max_churn_rate NUMERIC, tr_with_discount NUMERIC,
                                    margin_rate NUMERIC)
    RETURNS VARCHAR
    LANGUAGE sql
AS
$$
SELECT group_name
FROM fn_common_part(customer, max_churn_rate, tr_with_discount, margin_rate);
$$;

-- Определение размера скидки.
--
CREATE OR REPLACE FUNCTION fn_discount(customer BIGINT, max_churn_rate NUMERIC, tr_with_discount NUMERIC,
                                       margin_rate NUMERIC)
    RETURNS NUMERIC
    LANGUAGE sql
AS
$$
SELECT discount
FROM fn_common_part(customer, max_churn_rate, tr_with_discount, margin_rate);
$$;

-- Функция, определяющая предложения, ориентированные на рост среднего чека.
--
-- @param calc_method: метод расчета среднего чека (1 - за период, 2 - за количество)
-- @param first_date: первая дата периода (для 1 метода)
-- @param last_date: последняя дата периода (для 1 метода)
-- @param tr_count: количество транзакций (для 2 метода)
-- @param grow_coef: коэффициент увеличения среднего чека
-- @param max_churn_rate: максимальный индекс оттока
-- @param tr_with_discount: максимальная доля транзакций со скидкой (в процентах)
-- @param margin_rate: допустимая доля маржи (в процентах)
--
CREATE OR REPLACE FUNCTION fn_grow_avg_check(calc_method INT, 
                                            first_date DATE, 
                                            last_date DATE, 
                                            tr_count INT,
                                            grow_coef NUMERIC, 
                                            max_churn_rate NUMERIC, 
                                            tr_with_discount NUMERIC,
                                            margin_rate NUMERIC)
    RETURNS TABLE
            (
                Customer_ID            BIGINT,
                Required_Check_Measure NUMERIC,
                Group_Name             VARCHAR,
                Offer_Discount_Depth   NUMERIC
            )
    LANGUAGE plpgsql
AS $$
BEGIN RETURN QUERY
        SELECT p.customer_id,
               round(CASE
                         WHEN calc_method = 1
                             THEN fn_avg_check_by_period(p.customer_id, first_date, last_date)
                         WHEN calc_method = 2
                             THEN fn_avg_check_by_tr_count(p.customer_id, tr_count)
                         END * grow_coef, 2)                                                                                AS Required_Check_Measure,
               fn_group(p.customer_id, max_churn_rate, tr_with_discount / 100.0, margin_rate / 100.0)                       AS Group_Name,
               round(fn_discount(p.customer_id, max_churn_rate, tr_with_discount / 100.0, margin_rate / 100.0) * 100, 2)    AS Offer_Discount_Depth
        FROM personal_data p
        WHERE CASE
                  WHEN calc_method = 1
                      THEN fn_avg_check_by_period(p.customer_id, first_date, last_date)
                  WHEN calc_method = 2
                      THEN fn_avg_check_by_tr_count(p.customer_id, tr_count)
            END IS NOT NULL
          AND fn_group(p.customer_id, max_churn_rate, tr_with_discount / 100.0, margin_rate / 100.0) IS NOT NULL
          AND fn_discount(p.customer_id, max_churn_rate, tr_with_discount / 100.0, margin_rate / 100.0) IS NOT NULL
          AND fn_discount(p.customer_id, max_churn_rate, tr_with_discount / 100.0, margin_rate / 100.0) > 0
        ORDER BY 1;
END
$$;


-- tests {
SELECT *
FROM fn_grow_avg_check(
    calc_method         := 1,
    first_date          := '2020-01-01',
    last_date           := '2020-12-31',
    tr_count            := 0,
    grow_coef           := 1.15,
    max_churn_rate      := 3,
    tr_with_discount    := 70,
    margin_rate         := 30
);
--
SELECT *
FROM fn_grow_avg_check(
    calc_method         := 2,
    first_date          := null,
    last_date           := null,
    tr_count            := 100,
    grow_coef           := 1.15,
    max_churn_rate      := 3,
    tr_with_discount    := 70,
    margin_rate         := 30
);
-- tests }