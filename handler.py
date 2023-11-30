try:
    import unzip_requirements
except ImportError:
    pass

import json
import uuid
import re
import psycopg2
from psycopg2 import sql

db_params = {
    'dbname': 'backendtask',
    'user': 'tasks',
    'password': 'password',
    'host': 'tasks.cimwffl3uo0u.ap-south-1.rds.amazonaws.com',
    'port': '5432'
}

# /create_user

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
        
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Store user data in a database 
        query = sql.SQL("INSERT INTO users (user_id, full_name, mob_num, pan_num) VALUES ({}, {}, {}, {})").format(
            sql.Literal(user_id),
            sql.Literal(full_name),
            sql.Literal(mob_num),
            sql.Literal(pan_num)
        )
        cursor.execute(query)
        conn.commit()

        # Close the database connection
        cursor.close()
        conn.close()

        # Return response
        return {
            'statusCode': 200,
            'body': json.dumps('User created successfully')
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }