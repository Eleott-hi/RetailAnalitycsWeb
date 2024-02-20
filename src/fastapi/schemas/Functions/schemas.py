from pydantic import BaseModel
from datetime import date, datetime


class fnc_grow_avg_check_input(BaseModel):
    calc_method: int
    first_date: date | None
    last_date: date | None
    tr_count: int
    grow_coef: float
    max_churn_rate: float
    tr_with_discount: float
    margin_rate: float


class fnc_grow_avg_check_output(BaseModel):
    customer_id: int
    required_check_measure: float
    group_name: str
    offer_discount_depth: float

    class Config:
        from_attributes = True


class fnc_personal_offers_aimed_at_increasing_frequency_of_visits_input(BaseModel):
    first_date: datetime
    last_date: datetime
    add_transactions: int
    max_churn_rate: float
    max_discount_share: float
    margin: float


class fnc_personal_offers_aimed_at_increasing_frequency_of_visits_output(BaseModel):
    customer_id: int
    start_date: datetime
    end_date: datetime
    required_transactions_count: float
    group_name: str
    offer_discount_depth: float

    class Config:
        from_attributes = True


class fnc_personal_offers_aimed_at_cross_selling_input(BaseModel):
    groups: int
    max_churn_rate: int
    max_stability_index: float
    max_sku_share: int
    max_margin_share: int


class fnc_personal_offers_aimed_at_cross_selling_output(BaseModel):
    customer_id: int
    sku_names: str
    offer_discount_depth: float

    class Config:
        from_attributes = True
