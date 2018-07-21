from ..models import Admin, Catalog
from .. import db

def query_catalog_by_name(catalog):
    catalog = db.session.query(Catalog).filter(Catalog.catalog == catalog).one_or_none()
    return catalog


def create_catalog(catalog, created_id):
    db_catalog = query_catalog_by_name(catalog)
    print(db_catalog)
    if(db_catalog):
        return False, db_catalog

    catalog = Catalog(catalog = catalog, created_id = created_id)
    db.session.add(catalog)
    db.session.commit()
    return True, catalog