from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required

import graphene
from graphene_django import DjangoObjectType


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
        only_fields = ('id', 'username', 'email',)


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, id=graphene.ID(required=True))
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    @login_required
    def resolve_user(self, info, id: str):
        return get_user_model().objects.get(id=id)

    @login_required
    def resolve_users(self, info):
        return get_user_model().objects.all()

    @login_required
    def resolve_me(self, info: graphene.ResolveInfo):
        user: UserType = info.context.user
        return user


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username: str, password: str, email: str):
        user = get_user_model()(username=username, password=password)
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
