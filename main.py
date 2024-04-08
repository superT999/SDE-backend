from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from database.database import get_db
from sqlalchemy import text
from sqlalchemy.orm import Session

app = FastAPI()

# allow CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/docs", include_in_schema=False)
async def get_documentation():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
    )

# Define test API
@app.get("/")
async def root():
    return {"message": "Hello World"}

"""
Get Schemas Endpoint
Get the list of schemas from the connected Postgres database.
Query Parameters:
    - db_user
    - db_password
    - db_host
    - db_port
    - db_name
Returns: JSON array of schemas
"""
@app.get("/schemas")
async def connectdb(db_user, db_password, db_host, db_port, db_name):
    try:
        db = get_db(db_user, db_password, db_host, db_port, db_name)
        schemas = await get_schemas(db)
        return {"schemas": schemas}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting schemas")

# Get Schemas Helper Method
async def get_schemas(db: Session):
    query = text("SELECT schema_name FROM information_schema.schemata")
    result = db.execute(query)
    schemas = [
        dict(zip(result.keys(), row))
        for row in result.fetchall()
    ]
    return schemas

"""
Get Tables Endpoint
Get the list of tables from the connected Postgres database schema.
Query Parameters:
    - schema
    - db_user
    - db_password
    - db_host
    - db_port
    - db_name
    - pagination(optional)
        - page = 1
        - per_page = 5
Returns: Array of table names
"""
@app.get("/tables")
async def get_tables(schema: str, page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    try:
        tables = await get_tables_for_schema(schema, page, per_page, db)
        return {"tables": tables}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting tables")

# Get Tables Helper Method
async def get_tables_for_schema(schema: str, page: int, per_page: int, db: Session):
    query = text(f"SELECT table_name FROM information_schema.tables WHERE table_schema = :schema LIMIT {per_page} OFFSET {(page - 1) * per_page}") 
    result = db.execute(query, params={"schema": schema})
    return [row[0] for row in result.fetchall()]

"""
Get Tables Count Endpoint
Get the total count of tables from the connected Postgres database schema.
Query Parameters:
    - schema
    - db_user
    - db_password
    - db_host
    - db_port
    - db_name
Returns: Number of tables
"""
@app.get("/tables/count")
async def get_tables_count(schema: str, db: Session = Depends(get_db)):
    try:
        count = await get_tables_count_for_schema(schema, db)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting tables count")

# Get Tables Count Helper Method
async def get_tables_count_for_schema(schema: str, db: Session):
    query = text(f"SELECT count(*) FROM information_schema.tables WHERE table_schema = :schema")
    result = db.execute(query, params={"schema": schema})
    return result.one()[0]

"""
Get Table Content Endpoint
Get the list of rowss from the connected Postgres database table.
Query Parameters:
    - table
    - db_user
    - db_password
    - db_host
    - db_port
    - db_name
    - pagination(optional)
        - page = 1
        - per_page = 5
Returns: Array of row data
"""
@app.get("/table_data") 
async def get_table_data(table: str, page: int  = 1, per_page: int = 10, db: Session = Depends(get_db)):
    try:
        data = await get_table_contents(table, page, per_page, db)
        return data 
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting table data")

# Get Table Content Helper Method
async def get_table_contents(table: str, page: int, per_page: int, db: Session):
    query = text(f"SELECT * FROM {table} LIMIT {per_page} OFFSET {(page - 1) * per_page}") 
    result = db.execute(query)
    return result.mappings().all()

"""
Get Table Data Count Endpoint
Get the total count of rows from the connected Postgres database table.
Query Parameters:
    - table
    - db_user
    - db_password
    - db_host
    - db_port
    - db_name
Returns: Number of rows
"""
@app.get("/table_data/count")
async def get_table_data_count(table: str, db: Session = Depends(get_db)):
    try:
        count = await get_table_contents_count(table, db)
        return {"count": count}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error getting table data count")

# Get Table Contents Count Heloper Method
async def get_table_contents_count(table: str, db: Session):
    query = text(f"SELECT count(*) FROM {table}")
    result = db.execute(query)
    return result.one()[0]
