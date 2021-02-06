import graphene
from graphene_django import DjangoObjectType
from django.utils import timezone

from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        exclude = ("deleted",)


class Query(graphene.ObjectType):
    todos = graphene.List(TodoType)

    def resolve_todos(self, info):
        return Todo.objects.all()


class CreateTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        text = graphene.String(required=True)

    def mutate(self, info, text: str):
        todo = Todo(text=text)
        todo.save()
        return CreateTodo(todo=todo)


class DeleteTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)

    def mutate(self, info, id: str):
        todo: Todo = Todo.objects.get(id=id)
        todo.deleted = True
        todo.save()
        return DeleteTodo(todo=todo)


class EditTodo(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)
        text = graphene.String(required=True)

    def mutate(self, info, id: str, text: str):
        todo: Todo = Todo.objects.get(id=id)
        todo.text = text
        todo.date_updated = timezone.now()
        todo.save()
        return DeleteTodo(todo=todo)


class MarkTodoAsDone(graphene.Mutation):
    todo = graphene.Field(TodoType)

    class Arguments:
        id = graphene.ID(required=True)
        status = graphene.Boolean()

    def mutate(self, info, id: str, status=None):
        todo: Todo = Todo.objects.get(id=id)
        todo.completed = status if status is not None else not todo.completed
        todo.date_updated = timezone.now()
        todo.save()
        return MarkTodoAsDone(todo=todo)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    delete_todo = DeleteTodo.Field()
    edit_todo = EditTodo.Field()
    mark_as_done = MarkTodoAsDone.Field()
