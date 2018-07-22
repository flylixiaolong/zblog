from ..models import Admin, Catalog, Tag
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