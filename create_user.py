try:
    import unzip_requirements
except ImportError:
    pass

import json
import uuid
import re

def is_valid_pan(pan_num):
    pan_pattern = re.compile(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$')
    return bool(pan_pattern.match(pan_num))

def is_valid_mobile(mob_num):
    mob_pattern = re.compile(r'^\d{10}$')
    return bool(mob_pattern.match(mob_num))

def create_user(event, context):
    try:
        body = json.loads(event['body'])

        full_name = body.get('full_name')
        mob_num = body.get('mob_num')
        pan_num = body.get('pan_num')

        if not full_name or not mob_num or not pan_num:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        # Validate PAN card format
        if not is_valid_pan(pan_num):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid PAN card format'})
            }

        # Validate mobile number format
        if not is_valid_mobile(mob_num):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Invalid mobile number format'})
            }
        # Generate a UUID for user_id
        user_id = str(uuid.uuid4())

        # Store user data in a database (you can add this part later)

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({'user_id': user_id, 'full_name': full_name, 'mob_num': mob_num, 'pan_num': pan_num})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }