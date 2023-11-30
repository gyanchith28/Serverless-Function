try:
    import unzip_requirements
except ImportError:
    pass

import os
import json
import uuid
import re
import psycopg2
from psycopg2 import sql
import credentials

db_params = credentials.db_params

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

def get_users(event, context):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Fetch users
        cursor.execute("SELECT * FROM users;")
        users_record = cursor.fetchall()

        cursor.close()
        conn.close()

        users = []
        for record in users_record:
            user = {
                'user_id': record[0],
                'full_name': record[1],
                'mob_num': record[2],
                'pan_num': record[3]
            }
            users.append(user)

        return {
            'statusCode': 200,
            'body': json.dumps({'users': users})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': e})
        }

def delete_user(event, context):
    try:
        body = json.loads(event['body'])
        user_id = body.get('user_id')

        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE user_id = %s;", (user_id,))
        existing_user = cursor.fetchone()

        if not existing_user:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }

        # Deletion
        query = sql.SQL("DELETE FROM users WHERE user_id = {}").format(
            sql.Literal(user_id)
        )
        cursor.execute(query)
        conn.commit()

        cursor.close()
        conn.close()

        return {
            'statusCode': 200,
            'body': json.dumps('User deleted successfully')
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
