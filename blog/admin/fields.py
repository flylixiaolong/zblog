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

tags_fields = {
    'data': fields.List(fields.Nested(tag_fields))
}