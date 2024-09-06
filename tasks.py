from celery import Celery
from flask_mail import Message

from config.extends import mail


def send_mail(recipient, subject, body):
    message = Message(subject=subject, recipients=[recipient], body=body)
    mail.send(message)
    return {"status": "SUCCESS"}


def test_sleep():
    print(f"Sleeping for 20 seconds...")
    import time
    time.sleep(20)
    print("Task completed")
    return {"status": "SUCCESS", "message": f"Slept for {20} seconds"}


def create_celery(app):

    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.celery = celery

    # 添加任务
    celery.task(name="send_mail")(send_mail)
    celery.task(name="test_sleep")(test_sleep)

    return celery


