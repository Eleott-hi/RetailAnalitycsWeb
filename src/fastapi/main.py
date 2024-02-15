from fastapi import FastAPI
import strawberry
from strawberry.fastapi import GraphQLRouter
from fastapi.responses import FileResponse
from GraphQL.Mutation import Mutation
from GraphQL.Query import Query
from GraphQL.Subscription import Subscription

schema = strawberry.Schema(
    query=Query,
    mutation=Mutation,
    subscription=Subscription
)
graphql_app = GraphQLRouter(schema)

app = FastAPI()
app.include_router(graphql_app, prefix="/graphql")


@app.get("/")
async def root() -> FileResponse:
    return FileResponse("index.html")


@app.get("/add")
async def add_user_url() -> FileResponse:
    return FileResponse("add-user.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="fastapi", port=8000, reload=True)
