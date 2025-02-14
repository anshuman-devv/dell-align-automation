# FastAPI Blog Application

## Overview
## This is a FastAPI-based Blog Application that allows users to manage users, blogs, and comments. It provides full CRUD operations with proper validation, authentication, and authorization.

---

## Tech Stack
- *FastAPI* - Web framework  
- *Pydantic* - Data validation  
- *MongoDB* - Database  
- *Pytest* - Unit testing  
- *Swagger UI* - API Documentation  

---

## API Endpoints

### Authentication API
| Method | Endpoint | Description |
|--------|----------|-------------|
| *POST* | /auth/signup | Create a new user (Signup) |
| *POST* | /auth/login | User login (returns JWT token) |

---

### Blog API
| Method | Endpoint | Description |
|--------|----------|-------------|
| *POST* | /blogs/ | Create a new blog (requires authentication) |
| *GET*  | /blogs/ | Get all blogs |
| *GET*  | /blogs/{blog_id} | Get blog details by ID |
| *PUT*  | /blogs/{blog_id} | Update blog details (requires authentication) |
| *DELETE* | /blogs/{blog_id} | Delete a blog (requires authentication) |

---

### Comments API
| Method | Endpoint | Description |
|--------|----------|-------------|
| *POST* | /comments/blog/{blog_id}/create | Add a comment to a blog |
| *GET*  | /comments/{comment_id} | Get comment details by ID |
| *PUT*  | /comments/{comment_id}/update | Update comment details by ID |
| *DELETE* | /comments/{comment_id} | Delete a comment (requires authentication) |


---

## Testing Overview
- **Pytest** is used for unit testing.
- Mocking is implemented using `unittest.mock` and `pytest-mock`.
- Fixtures are defined for sample users, blogs, and comments.

### Test Cases Implemented:
- User Signup Test
- User Login Test
- Create Blog Test
- Read Blog Test
- Create Comment Test
- Read Comment Test

---


## Conclusion
This project demonstrates a robust backend implementation with FastAPI, including API endpoints, authentication, authorization, and automated testing. It uses best practices with modular code structure and proper error handling.