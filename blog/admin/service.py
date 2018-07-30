from ..models import Admin, Catalog, Tag, Post, Comment
from .. import db

def query_catalog_by_name(catalog):
    catalog = db.session.query(Catalog).filter(Catalog.catalog == catalog).one_or_none()
    return catalog

def query_catalog_by_id(id):
    catalog = db.session.query(Catalog).get(id)
    return catalog

def create_catalog(catalog, created_id):
    db_catalog = query_catalog_by_name(catalog)
    if(db_catalog):
        return False, db_catalog
    catalog = Catalog(catalog = catalog, created_id = created_id)
    db.session.add(catalog)
    db.session.commit()
    return True, catalog

def query_catalogs():
    catalogs = db.session.query(Catalog).all()
    return catalogs

def query_tag_by_name(tag):
    tag = db.session.query(Tag).filter(Tag.tag == tag).one_or_none()
    return tag

def query_tag_by_id(id):
    tag = db.session.query(Tag).get(id)
    return tag

def create_tag(tag, created_id):
    db_tag = query_tag_by_name(tag)
    if(db_tag):
        return False, db_tag
    tag = Tag(tag = tag, created_id = created_id)
    db.session.add(tag)
    db.session.commit()
    return True, tag

def query_tags():
    tags = db.session.query(Tag).all()
    return tags

def query_tags_by_ids(tags):
    tags = db.session.query(Tag).filter(Tag.id.in_(tags)).all()
    return tags

def query_post_by_id(id):
    post = db.session.query(Post).get(id)
    return post

def query_post_by_title(title):
    post = db.session.query(Post).filter(Post.title == title).one_or_none()
    return post

def create_post(title, summary, content, created_id, catalog, tags):
    db_post = query_post_by_title(title)
    if db_post:
        return False, db_post
    post = Post(title=title, summary=summary, content=content, created_id=created_id, catalog=catalog, tags=tags)
    db.session.add(post)
    db.session.commit()
    return True, post

def query_posts(limit=10, offset=0):
    posts = db.session.query(Post).limit(limit).offset(offset).all()
    return posts

def total_posts():
    count = db.session.query(Post).count()
    return count

def query_comment_by_id(id):
    comment = db.session.query(Comment).get(id)
    return comment

def create_comment(name, email, content, post, reply=None):
    error = {}
    db_post = query_post_by_id(post)
    if(not db_post):
        error['post'] = '`{0}`没找到相应的文章'.format(post)
    if(reply):
        db_reply = query_comment_by_id(reply)
        if(not db_reply):
            error['reply'] = '`{0}`没找到相应的评论'.format(reply)
    if(error):
        return error, None
    comment = Comment(name=name, email=email, content=content, post=db_post, reply=db_reply)
    db.session.add(comment)
    db.session.commit()
    return None, comment

def query_comments(post, limit=10, offset=0):
    comments = db.session.query(Comment).filter(Comment.post==post).limit(limit).offset(offset).all()
    return comments

def total_comments(post):
    count = db.session.query(Comment).filter(Comment.post==post).count()
    return count