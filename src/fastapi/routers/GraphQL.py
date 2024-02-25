import strawberry
from strawberry.fastapi import GraphQLRouter
from GraphQL.Mutation import Mutation
from GraphQL.Query import Query
from GraphQL.Subscription import Subscription
from strawberry.schema.config import StrawberryConfig

router = GraphQLRouter(
    strawberry.Schema(
        query=Query,
        mutation=Mutation,
        subscription=Subscription,
        config=StrawberryConfig(auto_camel_case=False),
    )
)
