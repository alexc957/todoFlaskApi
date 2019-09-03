from flaskTodoAPi.models import Tag
from flask import Blueprint, jsonify
from flaskTodoAPi.schemas import TagSchema

tags_schema = TagSchema(many=True,strict=True)

tags = Blueprint('tags',__name__)

@tags.route('/api/tags/tag',methods=['GET'])
def get_tags():
    all_tags = Tag.query.all()
    result = tags_schema.dump(all_tags)
    return jsonify(result.data)
    