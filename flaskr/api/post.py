from flask import jsonify
from flask.views import MethodView

from ..db import Post, sql


class PostAPI(MethodView):
    def get(self, post_id):
        if post_id is None:
            return jsonify([post.to_json() for post in Post.query.all()])
        else:
            return jsonify(Post.query.get(post_id).to_json())

    def post(self):
        title, body = request.json['title'], request.json['body']
        post = Post(title=title, body=body, author_id=author_id)
        sql.session.add(post)
        sql.session.commit()
        return jsonify(post.to_json())
    
    def delete(self, post_id):
        post = Post.query.get(post_id)
        sql.session.delete(post)
        sql.session.commit()
        return json.dumps({}), 204, 'application/json'

    
    def put(self, post_id):        
        post = Post.query.get(post_id)
        post.title = request.json['title']
        post.body = request.json['body']
        sql.session.add(post)
        sql.session.commit()
        return jsonify(post.to_json()