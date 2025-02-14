from fastapi import FastAPI, Depends
from ariadne import gql, QueryType, make_executable_schema, MutationType
from ariadne.asgi import GraphQL
from sqlalchemy.orm import Session
from app.db.Session import get_db, init_tables
from app.services.user_service import get_all , add , update, delete
from .redis.service import get_users, set_users, get_users, update_cache
app = FastAPI()


@app.on_event('startup')
def migrate_tables():
    print("init db")
    init_tables()


type_defs = gql("""
    type Query {
        hello: String!
        users: [User!]!
    }
    
    type Mutation {
        createUser(name: String! , email: String!) : User!,
        updateUser(id: ID!, name: String!) : User!,
        deleteUser( id: ID!) : Boolean!
    }

    type User {
        id: ID!
        name: String!
        email: String!
    }
""")

query = QueryType()
mutation = MutationType()

@query.field("hello")
def resolve_hello(_,info):
    return "Hello World!"


@query.field("users")
async def resolve_users(_, info):
    db = next(get_db())
    cached_users = await get_users()
    if cached_users != []:
        return cached_users
    users = get_all(db)
    await set_users(users)
    #print("users " + users)
    return users


@mutation.field("createUser")
async def resolve_create_user(_,info, name: str, email: str):
    db = next(get_db())
    user = add(db, name, email)
    await update_cache(user=user)
    return user


@mutation.field("updateUser")
async def resolve_update_user(_,info, id: int, name: str):
    db = next(get_db())
    user = update(db, id, name)
    await update_cache(id=id,user=user)
    return user


@mutation.field("deleteUser")
async def resolve_delete_user(_,info, id: int):
    db = next(get_db())
    await update_cache(id=id)
    return delete(db, id)

schema = make_executable_schema(type_defs, query, mutation)
app.add_route("/graphql", GraphQL(schema=schema, debug=True))
