from typing import List, Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy import func

router = APIRouter(prefix="/posts", tags=['Posts'])

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0,
              search: Optional[str] = ""):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
# getting posts w/out sqlalchemy:
#@app.get("/posts")
#def get_posts():
    # with conn.cursor() as cur:
    #    cur.execute("""SELECT * FROM posts""")
    #    posts = cur.fetchall()
    #results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, #models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()


    # Map the results to the PostOut schema
    posts_out = [schemas.PostOut(post=result[0], vote=result[1]) for result in results]

    return posts_out

@router.get("/posts_by_logged_user", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.user_id == current_user.user_id)
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db: Session = Depends(get_db), 
                 current_user: int = Depends(oauth2.get_current_user)):
    print("Inside create_posts function")
    print(f"Current user: {current_user.email}")
    new_post=models.Post(user_id=current_user.user_id, **post.model_dump())
    print(f"New post: {new_post}")
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(f"Post after commit: {new_post}")
    return new_post

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id:int, db: Session = Depends(get_db)):
    # with conn.cursor() as cur:
    #     cur.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    #     post = cur.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()
    result = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found")
    
        # Map the result to the PostOut schema
    post_out = schemas.PostOut(post=result[0], vote=result[1])

    return post_out

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # with conn.cursor() as cur:
    #     cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    #     deleted_post = cur.fetchone()
    #     conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} doesn't exist")

    if post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id:int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # with conn.cursor() as cur:
    #     cur.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                 (post.title, post.content, post.published, str(id)))
    #     updated_post = cur.fetchone()
    #     conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} doesn't exist")
    
    if post.user_id != current_user.user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()

