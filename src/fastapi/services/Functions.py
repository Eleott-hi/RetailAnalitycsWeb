from repositories.Functions import  execute_function
import schemas.Functions.schemas as schemas
from typing import Any, List
from dataclasses import dataclass
from sqlalchemy import func


@dataclass
class FunctionInfo:
    name: str
    func: Any
    input_schema: Any
    output_schema: Any


class FunctionService:
    @staticmethod
    def fnc_grow_avg_check(input: schemas.fnc_grow_avg_check_input) -> List[schemas.fnc_grow_avg_check_output]:
        res = execute_function('fnc_grow_avg_check', **input.dict())
        return res

    @staticmethod
    def fnc_personal_offers_aimed_at_increasing_frequency_of_visits(input: schemas.fnc_personal_offers_aimed_at_increasing_frequency_of_visits_input) -> List[schemas.fnc_personal_offers_aimed_at_increasing_frequency_of_visits_output]:
        res = execute_function('fnc_personal_offers_aimed_at_increasing_frequency_of_visits',
                               **input.dict())
        return res

    @staticmethod
    def fnc_personal_offers_aimed_at_cross_selling(input: schemas.fnc_personal_offers_aimed_at_cross_selling_input) -> List[schemas.fnc_personal_offers_aimed_at_cross_selling_output]:
        res = execute_function('fnc_personal_offers_aimed_at_cross_selling',
                               **input.dict())
        return res
