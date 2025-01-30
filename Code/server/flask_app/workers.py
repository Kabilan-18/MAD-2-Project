from celery import Celery, Task
from celery.schedules import crontab

def celery_init_app(app):
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)

    celery_config = {
        "broker_url": "redis://localhost:6379/1",
        "result_backend": "redis://localhost:6379/2",
        "timezone": "Asia/Kolkata",
        "broker_connection_retry_on_startup": True,
        'beat_schedule': {
            'send-daily-reminders-every-evening': {
                'task': 'flask_app.tasks.daily_remainder',
                'schedule': crontab(hour=21, minute=52),
            },
            'send_monthly_activity_report': {
                'task': 'flask_app.tasks.monthly_activity_report',
                'schedule': crontab(hour=21, minute=52),
            }
        },
    }

    celery_app.config_from_object(celery_config)
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app
