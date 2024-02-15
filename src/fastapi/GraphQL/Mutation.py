import strawberry
import GraphQL.Models as GQLModels


@strawberry.type
class Mutation:

    @strawberry.mutation
    def create_personal_data(self, name: str, surname: str, email: str, phone: str) -> GQLModels.PersonalData:
        return GQLModels.PersonalData.create(name=name, surname=surname, email=email, phone=phone)

    @strawberry.mutation
    def update_personal_data(self, id: int, name: str, surname: str, email: str, phone: str) -> GQLModels.PersonalData:
        return GQLModels.PersonalData.update(id=id, name=name, surname=surname, email=email, phone=phone)

    @strawberry.mutation
    def delete_personal_data(self, id: int) -> str:
        return GQLModels.PersonalData.delete(id=id)
