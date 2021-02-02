from graphene import ObjectType, List
from graphene_django import DjangoObjectType

from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo


class Query(ObjectType):
    todos = List(TodoType)

    def resolve_todos(self, info):
        return Todo.objects.all()
