from fastapi import APIRouter, Depends
from services.Functions import FunctionService
import schemas.Functions.schemas as schemas
router = APIRouter(prefix="/functions", tags=['Functions'])


@router.get("/", response_model=dict)
async def index():
    return {
        'functions': [
            'fnc_grow_avg_check',
            'fnc_personal_offers_aimed_at_increasing_frequency_of_visits',
            'fnc_personal_offers_aimed_at_cross_selling'
        ],
        'readable_names': [
            'Average Check',
            'Frequency of Visits',
            'Cross Selling'
        ]
    }


@router.get("/fnc_grow_avg_check", response_model=list[schemas.fnc_grow_avg_check_output])
async def fnc_1(input: schemas.fnc_grow_avg_check_input = Depends(schemas.fnc_grow_avg_check_input)):
    return FunctionService.fnc_grow_avg_check(input)


@router.get("/fnc_personal_offers_aimed_at_increasing_frequency_of_visits", response_model=list[schemas.fnc_personal_offers_aimed_at_increasing_frequency_of_visits_output])
async def fnc_2(input: schemas.fnc_personal_offers_aimed_at_increasing_frequency_of_visits_input = Depends(schemas.fnc_personal_offers_aimed_at_increasing_frequency_of_visits_input)):
    return FunctionService.fnc_personal_offers_aimed_at_increasing_frequency_of_visits(input)


@router.get("/fnc_personal_offers_aimed_at_cross_selling", response_model=list[schemas.fnc_personal_offers_aimed_at_cross_selling_output])
async def fnc_3(input: schemas.fnc_personal_offers_aimed_at_cross_selling_input = Depends(schemas.fnc_personal_offers_aimed_at_cross_selling_input)):
    return FunctionService.fnc_personal_offers_aimed_at_cross_selling(input)
