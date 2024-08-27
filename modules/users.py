import requests, uuid, jwt, datetime
from flask import jsonify
from modules.sqlite import SQLITE

class USERS:
    def __init__(self):
        self.user_id = None
        self.username = None
        self.password = None
        self.email = None
        self.role = None
        self.max_connection = None
        self.expired_date = None
        self.package_id = None
        self.package_name = None
        
    def register(self):
        try:
            db = SQLITE()
            
            # Check if the username or password already exists
            result = db.query(
                sql="SELECT username FROM users WHERE username = ? OR password = ?",
                args=(self.username, self.password)
            )
            
            if result:
                # Username or password already exists
                response = {
                    "status": "error",
                    "message": "Username or password already exists.",
                    "responseData": None
                }
                return jsonify(response), 409
            
            # Register the new user
            db.execute(
                sql="INSERT INTO users (user_id, username, password, email, role) VALUES (?, ?, ?, ?, ?)",
                args=(str(uuid.uuid4()).replace("-", ""), self.username, self.password, self.email, 'user')
            )
            db.commit()
            
            # Successful registration response
            response = {
                "status": "success",
                "message": "User registered successfully.",
                "responseData": {
                    "username": self.username,
                    "email": self.email
                }
            }
            return jsonify(response), 201
        
        except Exception as e:
            # Handle exceptions
            response = {
                "status": "error",
                "message": f"Error registering user: {str(e)}",
                "responseData": None
            }
            return jsonify(response), 500
        
        finally:
            # Ensure the database connection is closed
            db.close()
            
# ============================================================================================================================================ #

    def login(self):
        try:
            db = SQLITE()
            
            # Query to get the password for the given username
            result = db.query(
                sql="SELECT password FROM users WHERE username = ?",
                args=(self.username,)
            )
            
            # Validate the password
            if result and result[0]['password'] == self.password:
                # Generate JWT token
                token = jwt.encode({
                    'username': self.username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                }, 'IPTV', algorithm='HS256')
                
                response = {
                    "status": "success",
                    "message": "User logged in successfully.",
                    "responseData": {
                        "token": token
                    }
                }
                return jsonify(response), 200
            else:
                response = {
                    "status": "error",
                    "message": "Invalid username or password.",
                    "responseData": None
                }
                return jsonify(response), 401
        
        except Exception as e:
            response = {
                "status": "error",
                "message": f"Error logging in user: {str(e)}",
                "responseData": None
            }
            return jsonify(response), 500
        
        finally:
            db.close()
            
# ============================================================================================================================================ #

    def get_all_users(self):
        try:
            db = SQLITE()
            
            # Query to get all users
            query = "SELECT * FROM users;"
            result = db.query(sql=query)
            
            # Successful response
            response = {
                "status": "success",
                "message": "Users retrieved successfully.",
                "responseData": result
            }
            return jsonify(response), 200
        
        except Exception as e:
            # Handle exceptions
            response = {
                "status": "error",
                "message": f"Error retrieving users: {str(e)}",
                "responseData": None
            }
            return jsonify(response), 500
        
        finally:
            # Ensure the database connection is closed
            db.close()
    
# ============================================================================================================================================ #

    def get_single_users(self):
        try:
            db = SQLITE()
            
            # Query to get a single user by user_id
            query = "SELECT * FROM users WHERE user_id = ?;"
            result = db.query(sql=query, args=(self.user_id,))
            
            if not result:
                # User not found
                response = {
                    "status": "error",
                    "message": "User not found.",
                    "responseData": None
                }
                return jsonify(response), 404
            
            # Successful retrieval
            response = {
                "status": "success",
                "message": "User retrieved successfully.",
                "responseData": result
            }
            return jsonify(response), 200
        
        except Exception as e:
            # Handle exceptions
            response = {
                "status": "error",
                "message": f"Error retrieving user: {str(e)}",
                "responseData": None
            }
            return jsonify(response), 500
        
        finally:
            # Ensure the database connection is closed
            db.close()
            
# ============================================================================================================================================ #

    def delete_single_users(self):
        try:
            db = SQLITE()
            
            # Query to delete a user by user_id
            query = "DELETE FROM users WHERE user_id = ?;"
            db.execute(sql=query, args=(self.user_id,))
            db.commit()
            
            # Successful deletion
            response = {
                "status": "success",
                "message": "User deleted successfully.",
                "responseData": None
            }
            return jsonify(response), 200
        
        except Exception as e:
            # Handle exceptions
            response = {
                "status": "error",
                "message": f"Error deleting user: {str(e)}",
                "responseData": None
            }
            return jsonify(response), 500
        
        finally:
            # Ensure the database connection is closed
            db.close()
            
# ============================================================================================================================================ #

    def update_single_users(self):
        try:
            db = SQLITE()
            
            # Query to update a user by user_id
            update_query = """
            UPDATE users
            SET username = ?, password = ?, email = ?, role = ?
            WHERE user_id = ?;
            """
            
            # Execute the update query
            db.execute(
                sql=update_query,
                args=(self.username, self.password, self.email, self.role, self.user_id)
            )
            db.commit()
            
            # Successful update
            response = {
                "status": "success",
                "message": "User updated successfully.",
                "responseData": None
            }
            return jsonify(response), 200
        
        except Exception as e:
            # Handle exceptions
            response = {
                "status": "error",
                "message": f"Error updating user: {str(e)}",
                "responseData": None
            }
            return jsonify(response), 500
        
        finally:
            # Ensure the database connection is closed
            db.close()
            
# ============================================================================================================================================ #