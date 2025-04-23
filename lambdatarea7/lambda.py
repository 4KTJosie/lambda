import json
import boto3
import uuid
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
tabla = dynamodb.Table('Prestamos')

def lambda_handler(event, context):
    # Parsear el cuerpo del request (JSON)
    try:
        body = json.loads(event['body'])
    except:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Formato de entrada inválido. Debe ser JSON.'})
        }

    # Validación de campos requeridos
    campos_requeridos = ['usuario', 'libro', 'fecha_prestamo', 'fecha_devolucion']
    for campo in campos_requeridos:
        if campo not in body:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': f'Campo obligatorio faltante: {campo}'})
            }

    # Crear item para guardar en DynamoDB
    item = {
        'id': str(uuid.uuid4()),  # ID único
        'usuario': body['usuario'],
        'libro': body['libro'],
        'fecha_prestamo': body['fecha_prestamo'],
        'fecha_devolucion': body['fecha_devolucion'],
        'registrado_en': datetime.now().isoformat()
    }

    # Guardar en la tabla DynamoDB
    tabla.put_item(Item=item)

    return {
        'statusCode': 200,
        'body': json.dumps({'mensaje': 'Préstamo registrado exitosamente', 'id': item['id']})
    }