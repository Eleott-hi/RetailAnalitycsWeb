from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from services.JWT import JWTBearer
from routers.GraphQL import router as graphql_router
from routers.Authentication import router as auth_router
from routers.Functions import router as function_router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # database.init_db()
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Retail Analytics Api",
    description="Api for CRUD on Retail Analytics SQL project",
    version="1.0.0",
    docs_url="/",
    openapi_url="/openapi.json",
    root_path="/api/v1",
)


app.include_router(
    auth_router,
)

app.include_router(
    function_router,
    dependencies=[Depends(JWTBearer())],
)

app.include_router(
    graphql_router,
    prefix=f"/graphql",
    tags=["GraphQL"],
    dependencies=[Depends(JWTBearer())],
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True,)
