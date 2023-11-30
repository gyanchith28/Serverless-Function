try:
    import unzip_requirements
except ImportError:
    pass

import json
import uuid

def create_user(event, context):
    try:
        body = json.loads(event['body'])

        full_name = body.get('full_name')
        mob_num = body.get('mob_num')
        pan_num = body.get('pan_num')

        # Validate inputs
        if not full_name or not mob_num or not pan_num:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing required fields'})
            }

        # Perform additional validations (e.g., mobile number and PAN format)

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