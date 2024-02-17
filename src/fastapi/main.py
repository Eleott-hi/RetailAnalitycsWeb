from fastapi import FastAPI
from fastapi import Depends
from services.JWT import JWTBearer
from routers.GraphQL import router as graphql_router
from routers.Authentication import router as auth_router

app = FastAPI()
app.include_router(auth_router)
app.include_router(
    graphql_router,
    prefix="/graphql",
    tags=["GraphQL"],
    # dependencies=[Depends(JWTBearer())]
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="fastapi", port=8000, reload=True)
