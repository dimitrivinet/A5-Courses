import datetime
import json

import bson.errors
import httpx
import pymongo
from bson.objectid import ObjectId
from fastapi import FastAPI, File, Form, HTTPException, UploadFile, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Article(BaseModel):
    author: str
    date: datetime.datetime
    title: str
    subtitle: str
    cover: str
    content_url: str


MONGODB_USERNAME = "root"
MONGODB_PASSWORD = "root"
MONGODB_HOST = "mongodb"
DATABASE_NAME = "MDT02"
COLLECTION_NAME = "Articles"


uri = f"mongodb://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@{MONGODB_HOST}"
client = pymongo.MongoClient(uri, 27017, serverSelectionTimeoutMS=5000)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]


@app.get("/")
async def root():
    return {"message": "Hello, World! (from python with FastAPI)"}


@app.get("/mongodb/serverInfo")
async def get_server_info():
    server_info = client.server_info()

    return {"info": server_info}


@app.get("/mongodb/collections")
async def get_database_info():
    collections = db.list_collection_names()

    return {"collections": collections}


@app.get("/mongodb/articles")
async def get_all_articles():
    collection = db[COLLECTION_NAME]

    cursor = collection.find({})
    articles_list = [
        {"id": str(document["_id"]), "title": document["title"]} for document in cursor]

    return {"all_articles": articles_list}


@app.delete("/mongodb/articles")
async def delete_all_articles():
    x = collection.delete_many({})

    return {"deleted_count": x.raw_result}


@app.get("/mongodb/article/{article_id}")
async def get_article_by_id(article_id: str):
    try:
        article = collection.find_one({"_id": ObjectId(article_id)})
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid article_id: {article_id}")

    article["_id"] = str(article["_id"])

    return {"article": article}


@app.post("/mongodb/article")
async def add_article(article: Article):
    article = article.dict()

    async with httpx.AsyncClient() as client:
        try:
            r = await client.get(article["content_url"])
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Content not found at content_url: {article['content_url']}")

    article["content"] = r.content

    x = collection.insert_one(article)

    return {"inserted": str(x.inserted_id)}


@app.delete("/mongodb/article/{article_id}")
async def delete_all_articles(article_id: str):
    try:
        x = collection.delete_one({"_id": ObjectId(article_id)})
    except bson.errors.InvalidId:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid article_id: {article_id}")
    return {"deleted_count": x.raw_result}


@app.post("/mongodb/articles")
async def add_articles(file: UploadFile = File(...)):
    to_insert = json.load(file.file)

    x = collection.insert_many(to_insert)

    inserted_ids = [{"id": str(inserted)} for inserted in x.inserted_ids]

    return {"inserted": inserted_ids}
