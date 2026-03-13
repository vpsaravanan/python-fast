from typing import Annotated, Literal
from fastapi import APIRouter, Depends, Request, HTTPException, Query
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Post, User
import sys
from pprint import pprint
import gc

gc.enable()
all_objects = gc.get_objects()
print(f"Number of tracked objects: {len(all_objects)}")
unreachable_objects = gc.collect()
print(f"Unreachable objects: {unreachable_objects}")


blogrouter = APIRouter()


# Task 1: Create a new blog post
# Insert a post with title, content, and link to existing user
# Set published=False initially
# Verify auto-generated fields (id, created_at)

class PostResponse(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    user_id: int

class BlogCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Title is required")
    content: str
    published: int
    user_id: int

@blogrouter.post("/blogs", response_model=PostResponse)
# Insert a post with title, content, and link to existing user
# Set published=False initially
# Verify auto-generated fields (id, created_at)

async def createblog(blog: BlogCreate, db:Session = Depends(get_db) ):
    # data = await request.json()
    # print(type(data))
    # print(data)
    # title = data.get('title')
    # if title == '':
    #     return "title is not mandatory"
    # if title == '' or not isinstance(title, str):
    #     raise HTTPException(400, detail = 'Title field is required')
    # blogstatus = data.get('published')
    # if not isinstance(blogstatus, int):
    #     raise HTTPException(400, 'Blog status should be 1 or 0')
    # print(db.query(User.username, User.email).filter(User.id == data.get('user_id')).first())
    # pass
    newblog = Post(**blog.dict())
    # print(newblog)
    # newblog = Post(title=blog.title, content=blog.content, published=blog.published, user_id=blog.user_id)
    db.add(newblog)
    db.commit()
    db.refresh(newblog)
    return newblog


# Task 2: Get all published posts
# Fetch only posts where published=True
# Order by created_at (newest first)
# Return title, content preview (first 100 chars), and author name

class PublishedPostResponse(BaseModel):
    # published: int
    # created_at: int
    title: str
    content: str
# response_model=PublishedPostResponse
@blogrouter.get('/get-published-blogs', response_model=list[PublishedPostResponse])
async def getpublishedblogs(status:int, db:Session = Depends(get_db)):
    query = db.query(Post).filter(Post.published == status).order_by(Post.created_at.desc()).all()
    # print(db.query(Post).filter(Post.published == status).order_by(Post.created_at.desc()).statement)
    output = []
    for data in query:
        # pprint (vars(data))
        # print(data.__dict__)
        # print({k: v for k, v in data.__dict__.items() if not k.startswith('_sa_')})
        output.append({"title":data.title, "content":data.content})
        # output.append(result)
    # print(output)
    return output


# Task 3: Update post views
# When someone reads a post, increment views count by 1
# Don't update the updated_at timestamp (only views changes)

class updateblogcontent(BaseModel):
    # blog_id:int
    content:str
    title:str
@blogrouter.put('/blogs/{blog_id}')
async def updateblogdata(blog:updateblogcontent, blog_id:int, db:Session = Depends(get_db)):
        #   print (blog_id)
        #   return None
        # updateblogcontentdata = User(title=blog.title, content = blog.content)
            blogidcontent = db.query(Post).filter(Post.id == blog_id).first()
            # print(blog.dict())
            if not blogidcontent:
                raise HTTPException(400, 'Blog id not exists')
            blogidcontent.title = blog.title
            blogidcontent.content = blog.content
            db.commit()
            db.refresh(blogidcontent)
            return {'message': 'updated successfully', 'blog' : blogidcontent}


# Task 5: Get author dashboard stats
# For a specific user, return:
# Total posts written
# Total views across all posts
# Most viewed post (title + views)
# List of unpublished drafts (title + created_at)
# Group and aggregate data efficiently

class userblogssummary(BaseModel):
    total_posts: int
    total_views: int
    most_viewed_post: dict
    unpublished_posts: list

@blogrouter.get("/blogs/{user_id}", response_model=userblogssummary)

async def getallblogsforuser(user_id: int, db: Session = Depends(get_db)):
    if user_id == '':
        raise HTTPException(status_code=400, detail='User id not exists')

    Useridexists = db.query(User).filter(User.id == user_id).first()

    if Useridexists is None:
        raise HTTPException(status_code=400, detail='User id not exists')

    noofblogs = db.query(Post).filter(Post.user_id == user_id).count()

    totalviews = db.query(func.sum(Post.views)).filter(Post.user_id == user_id).scalar()
    # result = (
    # db.query(
    #     func.count(Post.id).label("total_posts"),
    #     func.sum(Post.views).label("total_views")
    # )
    # .filter(Post.user_id == user_id)
    # .first()
    # )

    most_viewed_post = (
        db.query(Post.title, Post.views)
        .filter(Post.user_id == user_id)
        .order_by(Post.views.desc())
        .first()
    )

    unpublishedblogs = (
        db.query(Post.title, Post.created_at)
        .filter(Post.published == 0, Post.user_id == user_id)
        .all()
    )
    # print(unpublishedblogs)
    unpublished_posts = [ {"title": blog.title, "created_at": blog.created_at} for blog in unpublishedblogs ]

    most_viewed_post = {'title' : most_viewed_post.title, 'views': most_viewed_post.views}

    output = {
        "total_posts": noofblogs,
        "total_views": totalviews,
        "most_viewed_post": most_viewed_post,
        "unpublished_posts": unpublished_posts
    }
    # # Create a string object
    # name = "Tutorialspoint"
    # print("Initial reference count:", sys.getrefcount(name))  

    # # Assign the same string to another variable
    # other_name = "Tutorialspoint"
    # print("Reference count after assignment:", sys.getrefcount(name)) 

    # # # Concatenate the string with another string
    # string_sum = name + ' Python'
    # # string_sum = name
    # print("Reference count after concatenation:", sys.getrefcount(name)) 
    # print("Reference count of new concatenation string:", sys.getrefcount(string_sum)) 

    # # # Put the name inside a list multiple times
    # list_of_names = [name, name, name]
    # print("Reference count after creating a list with 'name' 3 times:", sys.getrefcount(name)) 

    # # # Deleting one more reference to 'name'
    # del other_name
    # print("Reference count after deleting 'other_name':", sys.getrefcount(name))  

    # # # Deleting the list reference
    # del list_of_names
    # a = "Tutorialspoint"
    # print("Reference count after deleting the list:", sys.getrefcount(name)) 

    return output
# async def getallblogsforuser(user_id:int, db:Session = Depends(get_db)):
#     # print(user_id)
#     if user_id == '':
#         raise HTTPException (400, 'User id not exists')
#     Useridexists = db.query(User).filter(User.id == user_id).first()
#     # print(type(Useridexists)
#     if Useridexists is None:
#         raise HTTPException(status_code=400, detail = 'User id not exists')
#     noofblogs = db.query(Post).filter(Post.user_id == user_id).count()
#     # print(noofblogs)
#     totalviews = db.query( func.sum(Post.views)).group_by(Post.user_id).all()
#     # print(totalviews)
#     mostviewedblog = db.query(Post.title, Post.views).filter(Post.user_id == user_id).order_by(Post.views.desc()).first()
#     print(type(mostviewedblog))
#     unpublishedblogs = db.query(Post.title, Post.created_at).filter(Post.published == 0 and Post.user_id == user_id).all()
#     print(unpublishedblogs)
#     for i in unpublishedblogs:
#         print(i.title)
#     output = None
#     # output = {
#     #     'total_posts' : noofblogs,
#     #     'total_views' : totalviews,
#     #     # 'most_viewed_post' : mostviewedblog,
#     #     # 'unpublished_posts' : unpublishedblogs,
#     # }
#     return output
# #     For a specific user, return:
# # Total posts written
# # Total views across all posts
# # Most viewed post (title + views)
# # List of unpublished drafts (title + created_at)
# # Group and aggregate data efficiently

# Task 4: Search posts with filters
# Search by keyword in title OR content
# Filter by:
# Published status (optional)
# Date range (optional)
# Minimum views (optional)
# Return paginated results (5 per page)

class FilterParams(BaseModel):
    limit: int = Field(100, gt=0, le=100)
    offset: int = Field(0, ge=0)
    order_by: Literal["created_at", "updated_at"] = "created_at"
    tags: list[str] = []
    keyword: str
class SearchResponse(BaseModel):
    title: str
    content: str
    username: str

@blogrouter.get('/search')
async def search(filter_query: FilterParams = Depends(), db:Session = Depends(get_db)):
    # print(keyword)
    # print(filter_query)
    query = db.query(Post).join(User, Post.user_id == User.id).filter(Post.content.ilike('%'+filter_query.keyword+'%'))
    # print(db.query(Post).filter(Post.content.ilike('%'+filter_query.keyword+'%')).offset(filter_query.offset).statement)
    query = query.offset(filter_query.offset).limit(filter_query.limit).all()
    return query
    # for result in query:
    #     # pprint(vars(result))
    #     if(isinstance(result, dict)):
    #         pprint(vars(result))
    #     else:
    #        print(type(query),'else')
    #        print(query)