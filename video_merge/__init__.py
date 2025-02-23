#type: don't ignore
from contextlib import asynccontextmanager

from typing import Optional, Any
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from nest_asyncio import apply

from video_merge.routers import router
from video_merge.configs.index import CONFIG

import os

from dotenv import load_dotenv
load_dotenv()

apply()
# # enable nested async using asyncio
# import fastapi deps


# initiate lifespan context
@asynccontextmanager
async def lifespan(app: FastAPI):

    yield

    # cleanup
    # de init prisma


# initiate fastapi
app = FastAPI(
    lifespan=lifespan,
    title=f"python server for ai show",
    description="""
    You can use https://openapi-ts.pages.dev/openapi-fetch/ to generate typesafe clients for these resources.
    Auth routes here are just for debugging, use supabase sdk for the auth.
""",
)

# public static files
app.mount(
    "/public",
    StaticFiles(directory="public"),
    name="public",
)

app.include_router(router=router)


# add middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time

    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# listen to root
@app.get("/", include_in_schema=False)
def read_root():
    return RedirectResponse("/docs")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
