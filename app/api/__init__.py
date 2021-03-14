from flask_restplus import Api
from .task_controller import tasks as task_api
from .question_controller import questions as question_api

api = Api(
    title='API for manage question and tasks in Zulip',
    version='1.0',
    description='API for manage question and tasks in Zulip',
)

api.add_namespace(question_api)
api.add_namespace(task_api)