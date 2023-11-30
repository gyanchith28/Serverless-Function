# Serverless Functions API

Welcome to the Serverless Functions API documentation. This API allows you to perform CRUD operations on user data. Please follow the instructions below to get started.

## Prerequisites

1. Create a free tier account on your preferred cloud provider. I have used AWS here.
2. Enable access to serverless functions and set up a database. AWS users can utilize Lambda and RDS (PostgreSQL) services.

## Endpoints

- **Create User:** `POST - /create_user`
  - Request Body:
    ```json
    {
      "full_name": "John Doe",
      "mob_num": "9876543210",
      "pan_num": "AABCP1234C"
    }
    ```
  - Response (Success):
    ```json
    {
      "statusCode": 200,
      "body": "User created successfully"
    }
    ```
  - Response (Error):
    ```json
    {
      "statusCode": 400,
      "body": "Invalid PAN card format"
    }
    ```

- **Get Users:** `GET - /get_users`
  - Response (Success - Users Found):
    ```json
    {
      "statusCode": 200,
      "body": {
        "users": [
          {
            "user_id": "12345",
            "full_name": "John Doe",
            "mob_num": "9876543210",
            "pan_num": "AABCP1234C"
          },
        ]
      }
    }
    ```
  - Response (Success - No Users Found):
    ```json
    {
      "statusCode": 200,
      "body": {
        "users": []
      }
    }
    ```

- **Delete User:** `DELETE - /delete_user`
  - Request Body:
    ```json
    {
      "user_id": "12345"
    }
    ```
  - Response (Success):
    ```json
    {
      "statusCode": 200,
      "body": "User deleted successfully"
    }
    ```
  - Response (Error):
    ```json
    {
      "statusCode": 404,
      "body": "User not found"
    }
    ```

- **Update User:** `PUT - /update_user`
  - Request Body:
    ```json
    {
      "user_id": "12345",
      "update_data": {
        "full_name": "Updated Name",
        "mob_num": "9876543211"
      }
    }
    ```
  - Response (Success):
    ```json
    {
      "statusCode": 200,
      "body": "User updated successfully"
    }
    ```
  - Response (Error):
    ```json
    {
      "statusCode": 400,
      "body": "Invalid mobile number format"
    }
    ```

Feel free to use the provided endpoints to interact with the Serverless Functions API. If you encounter any issues, refer to the error messages for guidance. Happy coding!
