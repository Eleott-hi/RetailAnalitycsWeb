
import strawberry
from strawberry.fastapi import GraphQLRouter
from GraphQL.Mutation import Mutation
from GraphQL.Query import Query
from GraphQL.Subscription import Subscription


router = GraphQLRouter(
    strawberry.Schema(
        query=Query,
        mutation=Mutation,
        subscription=Subscription
    )
)
