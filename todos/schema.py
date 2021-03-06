
import graphene
from graphene_django import DjangoObjectType
from django.utils import timezone
from graphql import GraphQLError
from graphql_jwt.decorators import login_required
from typing import List, Optional
from django.core.paginator import Paginator

from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        exclude = ("deleted",)


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType, page=graphene.Int(),
                          count=graphene.Int(), search=graphene.String())

    def resolve_todos(self, info, page: Optional[int] = None, count: int = 5, search: Optional[str] = None) -> List[TodoType]:

        if (search):
            return Todo.objects.filter(deleted=False, text__icontains=search)

        todos = Todo.objects.filter(deleted=False)
        p = Paginator(todos, count)

        if (page):
            return p.page(page).object_list

        return todos


class CreateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        text = graphene.String(required=True)

    @login_required
    def mutate(self, info: graphene.ResolveInfo, text: str):
        user = info.context.user
        todo = Todo(text=text, created_by=user)
        todo.save()
        return CreateTodo(todo=todo)


class DeleteTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)

    @login_required
    def mutate(self, info, id: str):
        try:
            todo: Todo = Todo.objects.get(id=id)
            todo.deleted = True
            todo.save()
            return DeleteTodo(todo=todo)
        except:
            raise GraphQLError('Not found')


class EditTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)
        text = graphene.String(required=True)

    @login_required
    def mutate(self, info, id: str, text: str):
        try:
            todo: Todo = Todo.objects.get(id=id)
            todo.text = text
            todo.date_updated = timezone.now()
            todo.save()
            return DeleteTodo(todo=todo)
        except:
            raise GraphQLError('Not found')


class MarkTodoAsDone(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)
        status = graphene.Boolean()

    @login_required
    def mutate(self, info, id: str, status=None):
        try:
            todo: Todo = Todo.objects.get(id=id)
            todo.completed = status if status is not None else not todo.completed
            todo.date_updated = timezone.now()
            todo.save()
            return MarkTodoAsDone(todo=todo)
        except:
            raise GraphQLError('Not found')


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    delete_todo = DeleteTodo.Field()
    edit_todo = EditTodo.Field()
    mark_as_done = MarkTodoAsDone.Field()
