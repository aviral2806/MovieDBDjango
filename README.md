# Movies and TV Shows Database API

This project is a backend service built using **Django REST Framework** that provides a set of APIs for managing a Movies and TV Shows database. It supports full CRUD operations and implements a permission-based system with token authentication.

## Features

### CRUD APIs:
Supports full Create, Read, Update, and Delete operations for:
- **Movies**
- **TV Shows**
- **User Reviews**

### Token-Based Authentication:
Implements token authentication using Django's built-in token authentication system.  
Only authorized users can access specific APIs.

### Permission-Based Access Control:
Ensures that only users with the necessary permissions can create, edit, or delete resources.

### Pagination, Filtering, and Sorting:
Provides built-in pagination and allows filtering and sorting of Movies, TV Shows, and Reviews based on various attributes (e.g., release date, ratings, genres).
