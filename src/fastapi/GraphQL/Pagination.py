
from base64 import b64encode, b64decode
from typing import List, Optional, Generic, TypeVar

import strawberry

user_data = [
    {
        "id": 1,
        "name": "Norman Osborn",
        "occupation": "Founder, Oscorp Industries",
        "age": 42,
    },
    {
        "id": 2,
        "name": "Peter Parker",
        "occupation": "Freelance Photographer, The Daily Bugle",
        "age": 20,
    },
    {
        "id": 3,
        "name": "Harold Osborn",
        "occupation": "President, Oscorp Industries",
        "age": 19,
    },
    {
        "id": 4,
        "name": "Eddie Brock",
        "occupation": "Journalist, The Eddie Brock Report",
        "age": 20,
    },
]


def encode_user_cursor(id: int) -> str:
    """
    Encodes the given user ID into a cursor.

    :param id: The user ID to encode.

    :return: The encoded cursor.
    """
    return b64encode(f"user:{id}".encode("ascii")).decode("ascii")


def decode_user_cursor(cursor: str) -> int:
    """
    Decodes the user ID from the given cursor.

    :param cursor: The cursor to decode.

    :return: The decoded user ID.
    """
    cursor_data = b64decode(cursor.encode("ascii")).decode("ascii")
    return int(cursor_data.split(":")[1])


GenericType = TypeVar("GenericType")


@strawberry.type
class Connection(Generic[GenericType]):
    page_info: "PageInfo" = strawberry.field(
        description="Information to aid in pagination."
    )

    edges: list["Edge[GenericType]"] = strawberry.field(
        description="A list of edges in this connection."
    )


@strawberry.type
class PageInfo:
    has_next_page: bool = strawberry.field(
        description="When paginating forwards, are there more items?"
    )

    has_previous_page: bool = strawberry.field(
        description="When paginating backwards, are there more items?"
    )

    start_cursor: Optional[str] = strawberry.field(
        description="When paginating backwards, the cursor to continue."
    )

    end_cursor: Optional[str] = strawberry.field(
        description="When paginating forwards, the cursor to continue."
    )


@strawberry.type
class Edge(Generic[GenericType]):
    node: GenericType = strawberry.field(
        description="The item at the end of the edge.")

    cursor: str = strawberry.field(
        description="A cursor for use in pagination.")


@strawberry.type
class User:
    id: int = strawberry.field(description="The id of the user.")

    name: str = strawberry.field(description="The name of the user.")

    occupation: str = strawberry.field(
        description="The occupation of the user.")

    age: int = strawberry.field(description="The age of the user.")


@strawberry.type
class Query:
    @strawberry.field(description="Get a list of users.")
    def get_users(
        self, limit: int = 2, offset: Optional[str] = None
    ) -> Connection[User]:
        if offset is not None:
            # decode the user ID from the given cursor.
            user_id = decode_user_cursor(cursor=offset)
        else:
            # no cursor was given (this happens usually when the
            # client sends a query for the first time).
            user_id = 0

        # filter the user data, going through the next set of results.
        filtered_data = list(
            filter(lambda user: user["id"] > user_id, user_data))

        # slice the relevant user data (Here, we also slice an
        # additional user instance, to prepare the next cursor).
        sliced_users = filtered_data[: limit + 1]

        if len(sliced_users) > limit:
            # calculate the client's next cursor.
            last_user = sliced_users.pop(-1)
            next_cursor = encode_user_cursor(id=last_user["id"])
            has_next_page = True
        else:
            # We have reached the last page, and
            # don't have the next cursor.
            next_cursor = None
            has_next_page = False

        # We know that we have items in the
        # previous page window if the initial user ID
        # was not the first one.
        has_previous_page = user_id > 0

        # build user edges.
        edges = [
            Edge(
                node=User(**user),
                cursor=encode_user_cursor(id=user["id"]),
            )
            for user in sliced_users
        ]

        if edges:
            # we have atleast one edge. Get the cursor
            # of the first edge we have.
            start_cursor = edges[0].cursor
        else:
            # We have no edges to work with.
            start_cursor = None

        if len(edges) > 1:
            # We have atleast 2 edges. Get the cursor
            # of the last edge we have.
            end_cursor = edges[-1].cursor
        else:
            # We don't have enough edges to work with.
            end_cursor = None

        return Connection(
            edges=edges,
            page_info=PageInfo(
                has_next_page=has_next_page,
                has_previous_page=has_previous_page,
                start_cursor=start_cursor,
                end_cursor=end_cursor,
            ),
        )
