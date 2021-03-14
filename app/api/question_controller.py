from app.db.db_search import QueryProcessor
from app.db.models import Note
from .utils import checkModifiedFields
from flask import request
from flask_restplus import Namespace, Resource, fields
from sqlalchemy import Sequence
import json
import logging

questions = Namespace('questions', description='Questions related operations')
LOG = logging.getLogger(__name__)

modify_question_swagger_model = questions.model('Modify question', {
    'question_text': fields.String(required=True, description=' Specify question_txt'),
    'answer_text': fields.String(required=True, description=' Specify answer_txt'),
    'mark': fields.Integer(required=False, description=' Specify mark'),
    'max_attempts': fields.Integer(required=False, description=' Specify max_attempts')
})

add_questions_swagger_model = questions.clone('Add question', modify_question_swagger_model, {
    'task_id': fields.Integer(required=True, description=' Specify task_id')
})

@notes.route('/')
class NotesList(Resource):
    def get(self):
        return QueryProcessor().getEntities(Note)

    def post(self):
        request_dict = request.get_json()
        try:
            id = request_dict['id']
            title = request_dict['title']
            content = request_dict['content']
        except:
            return {"Status": "Wrong parameters"}, 400
        note = Note(id=id, title=title, content=content)
        QueryProcessor().addEntity()

@notes.route('/<int:id>')
class NotesById(Resource):

    @notes.doc('Modify Note')
    def put(self, id):
        if not id:
            return {"Status": "No id provided"}, 400
        note = QueryProcessor().findEntity('id', id, Note)
        if not note:
            return {"Status": "No Note"}, 404
        request_dict = request.get_json()
        try:
            title = request_dict['title']
            note.title = title
        except:
            print("No field")
        try:
            content request_dict['content']
            note.content = content
        except:
            print("No field")
        
        QueryProcessor().session.commit()

    @notes.doc('Delete Note')
    def delete(self, id):
        if not id:
            return {"Status": "No id provided"}, 400
        note = QueryProcessor().findEntity('id', id, Note)
        if not note:
            return {"Status": "No Note"}, 404

class NotesByQuery('/<string:query>')
    def get(self, query):
        return QueryProcessor().getEntities(content, query, Note)
