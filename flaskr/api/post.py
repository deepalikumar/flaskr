from flask import json, jsonify, request
from flask.views import MethodView

from ..db import Post, sql


class PostAPI(MethodView):
    def get(self, post_id):
        if post_id is None:
            return jsonify([post.to_json() for post in Post.query.all()])
        else:
            return jsonify(Post.query.get(post_id).to_json())

    def post(self):
        title, body, author_id = (request.json['title'], 
        request.json['body'], request.json['author_id'])
        post = Post(title=title, body=body, author_id=author_id)
        sql.session.add(post)
        sql.session.commit()
        return jsonify(post.to_json())
    
    def delete(self, post_id):
        post = Post.query.get(post_id)
        sql.session.delete(post)
        sql.session.commit()
        return jsonify({}), 204
    
    def put(self, post_id):        
        post = Post.query.get(post_id)
        post.title = request.json['title']
        post.body = request.json['body']
        sql.session.add(post)
        sql.session.commit()
        return jsonify(post.to_json())