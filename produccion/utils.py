import os
import requests
from datetime import datetime
from django.db.models import Sum
from produccion.models import RegistroProduccion

def send_slack_message(instance):
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not slack_webhook_url:
        raise ValueError("Slack webhook URL is not set in the environment variables.")
    
    total_almacenado = RegistroProduccion.objects.filter(
        producto=instance.producto
    ).aggregate(Sum('litros'))['litros__sum']
    
    message = (
        f"{datetime.now().strftime('%d-%m-%Y %H:%M')} - {instance.producto.planta.codigo} - "
        f"Nuevo Registro de Producción - {instance.producto.codigo} {instance.litros} lts. | "
        f"Total Almacenado: {total_almacenado} lts."
    )
    
    payload = {'text': message}
    response = requests.post(slack_webhook_url, json=payload)
    if response.status_code != 200:
        raise ValueError(f'Request to Slack returned an error {response.status_code}, the response is: {response.text}')
