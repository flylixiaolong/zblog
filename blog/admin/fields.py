from flask_restful import fields


catalog_fields = {
    'id': fields.Integer,
    'catalog': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
}

catalogs_fields = {
    'data': fields.List(fields.Nested(catalog_fields))
}


tag_fields = {
    'id': fields.Integer,
    'tag': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
}

post_fields = {
    'id': fields.Integer,
    'title': fields.String,
    'summary': fields.String,
    'content': fields.String,
    'created_at': fields.DateTime(dt_format='iso8601'),
    'updated_at': fields.DateTime(dt_format='iso8601')
}


comment_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'content': fields.String
}