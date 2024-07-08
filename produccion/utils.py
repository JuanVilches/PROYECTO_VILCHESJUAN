import os
import requests
from datetime import datetime
from django.db.models import Sum
from produccion.models import RegistroProduccion

def send_slack_message(instance):#Esta función toma una instancia de RegistroProduccion como argumento y envía un mensaje a Slack con información sobre el nuevo registro de producción.
    slack_webhook_url = os.getenv('SLACK_WEBHOOK_URL')#Obtiene la URL del webhook de Slack desde las variables de entorno.
    if not slack_webhook_url:
        raise ValueError("Slack webhook URL is not set in the environment variables.")
    
    #Filtra los registros de producción para obtener solo aquellos que corresponden al mismo producto que la instancia proporcionada.
    #Luego, calcula la suma de los litros almacenados en todos los registros de producción filtrados.
    #Esto proporciona el total de litros almacenados para el producto en cuestión.
    total_almacenado = RegistroProduccion.objects.filter(
        producto=instance.producto
    ).aggregate(Sum('litros'))['litros__sum']
    
    #Crea un mensaje con la información del nuevo registro de producción y el total de litros almacenados.
    message = (
        f"{datetime.now().strftime('%d-%m-%Y %H:%M')} - {instance.producto.planta.codigo} - "
        f"Nuevo Registro de Producción - {instance.producto.codigo} {instance.litros} lts. | "
        f"Total Almacenado: {total_almacenado} lts."
    )
    
    #Envía el mensaje a Slack utilizando la URL del webhook.
    payload = {'text': message}#Crea el payload (diccionario que contiene el mensaje que se enviará a Slack) para la solicitud HTTP, que es un diccionario con la clave 'text' y el mensaje como valor
    response = requests.post(slack_webhook_url, json=payload)#Realiza una solicitud POST a la URL del webhook de Slack con el payload JSON. 
    if response.status_code != 200: #    #Verifica si la solicitud fue exitosa (código de estado 200) y, de lo contrario, lanza una excepción con el código de estado y el texto de respuesta que se recibe luego de evniar el mensaje.
        raise ValueError(f'Request to Slack returned an error {response.status_code}, the response is: {response.text}')


