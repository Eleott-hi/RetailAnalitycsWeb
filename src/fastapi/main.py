from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from services.JWT import JWTBearer
from routers.GraphQL import router as graphql_router
from routers.Authentication import router as auth_router
from routers.Functions import router as function_router

base_url = '/api/v1'

app = FastAPI()
app.include_router(auth_router, prefix=base_url)
app.include_router(function_router, prefix=base_url,
                   dependencies=[Depends(JWTBearer())])
app.include_router(
    graphql_router,
    prefix=f"{base_url}/graphql",
    tags=["GraphQL"],
    # dependencies=[Depends(JWTBearer())]
)

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="fastapi", port=8000, reload=True)
