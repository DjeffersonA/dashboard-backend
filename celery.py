from __future__ import absolute_import
import os
from celery import Celery

# Define o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

# Carrega as configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre tarefas automaticamente em todos os apps instalados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')