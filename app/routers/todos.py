from fastapi import APIRouter, Request, HTTPException, Response
from app.models.todo import Todo, CreateTodo, UpdateTodo

router = APIRouter(prefix = '/todos')

@router.get('/')
async def get_todos(request: Request):
    async with request.app.pool.acquire() as con:
        result = await con.fetch('''
            SELECT *
            FROM todos;
        ''')
    return [Todo(**dict(record)) for record in result]


@router.post('/', status_code = 201)
async def create_todo(request: Request, todo: CreateTodo):
    async with request.app.pool.acquire() as con:
        result = await con.execute('''
            INSERT INTO todos (name, description)
            VALUES ($1, $2)
        ''', todo.name, todo.description)
    return todo


@router.put('/{id}')
async def update_todo(id: str, request: Request, todo: UpdateTodo):

    async with request.app.pool.acquire() as con:
        result = await con.fetchrow('''
            SELECT * 
            FROM todos
            WHERE id = $1
        ''', int(id))

        if not result:
            raise HTTPException(status_code = 404, detail = 'Todo with ID ' + id + ' not found!')

        result_todo = Todo(**dict(result))
        update_data = todo.dict(exclude_unset = True)
        updated_todo = result_todo.copy(update = update_data)

        result = await con.execute('''
            UPDATE todos
            SET name = $1,
                description = $2
            WHERE id = $3
        ''', updated_todo.name, updated_todo.description, int(id))

    return updated_todo


@router.put('/{id}')
async def update_todo(id: str, request: Request, todo: UpdateTodo):

    async with request.app.pool.acquire() as con:
        result = await con.fetchrow('''
            SELECT * 
            FROM todos
            WHERE id = $1
        ''', int(id))

        if not result:
            raise HTTPException(status_code = 404, detail = 'Todo with ID ' + id + ' not found!')

        result_todo = Todo(**dict(result))
        update_data = todo.dict(exclude_unset = True)
        updated_todo = result_todo.copy(update = update_data)

        result = await con.execute('''
            UPDATE todos
            SET name = $1,
                description = $2
            WHERE id = $3
            RETURNING name
        ''', updated_todo.name, updated_todo.description, int(id))

    return updated_todo


@router.delete('/{id}')
async def delete_todo(id: str, request: Request):

    async with request.app.pool.acquire() as con:
        result = await con.fetchval('''
            DELETE FROM todos
            WHERE id = $1
            RETURNING id
        ''', int(id))

        if not result:
            raise HTTPException(status_code = 404, detail = 'Todo with ID ' + id + ' not found!')

    return Response(status_code = 204)