# Backend Engineering Assessment
Role: Backend Software Engineer (Python/Django)

## Objective

This assessment is designed to evaluate more than your ability to write code.

We are interested in understanding how you think as an engineer.

The project evaluates:

- Software engineering principles
- Problem-solving ability
- Critical thinking
- Database design and normalization
- Backend architecture
- API design
- Business logic modelling
- Authentication & authorization
- Code quality and maintainability
- Performance optimization
- Error handling
- Testing approach
- Documentation
- Git usage
- Ability to make good engineering decisions
- Scalability considerations


# Duration

## 4 Days

Submission Deadline:
## 04/08/2026 

# Project

## Inventory & Order Management System

Build a REST API for a company that manages products, warehouses, customers and orders.

There are multiple warehouses.

Products can exist in multiple warehouses with different stock quantities.

Customers place orders.

Orders should only succeed if inventory is available.

# Functional Requirements

## Authentication

Implement authentication.

You may choose:

- Django Authentication
- JWT
- Session Authentication

Users have roles:

- Admin
- Staff

Only authenticated users should access APIs.

# Product Module

A product has:

- Name
- SKU (must be unique)
- Description
- Unit Price
- Status (Active/Inactive)

Operations:

- Create
- Update
- Delete
- List
- Retrieve

---

# Warehouse Module

Warehouse contains:

- Name
- Address
- Manager Name

Operations:

- CRUD

# Inventory Module

Each warehouse stores products.

Inventory contains:

- Warehouse
- Product
- Quantity Available
- Minimum Stock Level

Operations:

- Increase Stock
- Reduce Stock
- Transfer Stock Between Warehouses

# Customer Module

Customer contains:

- Full Name
- Email
- Phone Number

Operations:

- CRUD

# Order Module

Customers place orders.

Each order contains:

- Customer
- Multiple Products
- Quantity
- Selling Price
- Order Date
- Status

Statuses:

- Pending
- Processing
- Completed
- Cancelled

# Business Rules

### Rule 1

Order cannot be completed if stock is insufficient.

### Rule 2

Inventory should reduce automatically after successful order completion.

### Rule 3

Cancelling a completed order should restore inventory.

### Rule 4

Duplicate SKU should never exist.

### Rule 5

Deleting a product with existing orders should not be allowed.

### Rule 6

Warehouse inventory should never become negative.

# Reporting APIs

Create endpoints for:

- Top selling products
- Products with low stock
- Total inventory value
- Orders by status
- Daily sales summary

# Search & Filtering

Support:

- Product search
- Customer search
- Order filtering
- Warehouse filtering

Pagination required.

# API Documentation

Use either:

- Swagger
- DRF Spectacular
- Postman Collection

# Validation

Examples:

- Email validation
- Phone validation
- Price cannot be negative
- Quantity must be greater than zero
- SKU uniqueness

# Error Handling

Use meaningful HTTP status codes.

Consistent error responses.

Handle edge cases.

# Bonus Challenges (Medium)

Choose as many as possible.

### 1.

Implement soft delete.

### 2.

Audit log for important actions.

Examples:

- Product created
- Stock updated
- Order completed

### 3.

Bulk import products using CSV.

### 4.

Export orders to CSV.

### 5.

Implement caching for product listing.

### 6.

Dockerize the application.

---

### 7.

Background task for sending email after order completion.

(Celery or Django-Q)

# Advanced Challenges (Hard)

These intentionally test engineering maturity.

## Challenge 1

Prevent race conditions.

Example:

Two users place an order simultaneously.

Inventory must remain correct.

## Challenge 2

Use database transactions properly.

No partial updates should occur.


## Challenge 3

Design the database to avoid redundancy.

Explain your modelling decisions.

## Challenge 4

Write an endpoint that returns:

Warehouse Performance Dashboard

Example:

```json
{
    "warehouse": "Lagos",
    "products": 250,
    "inventory_value": 4000000,
    "low_stock": 12,
    "orders_fulfilled": 125
}
````

## Challenge 5

Optimize slow queries.

Use:

* select_related
* prefetch_related

where appropriate.

## Challenge 6

Implement optimistic or pessimistic locking where necessary.

# Testing

Write unit tests for critical business logic.

Minimum:

* Order creation
* Stock deduction
* Stock restoration
* Authentication

# What We Will Evaluate

We are **not** looking for the project with the most features.

We are looking for engineers who make thoughtful technical decisions.

Evaluation criteria:

| Area                  | Weight |
| --------------------- | ------ |
| Database Design       | 20%    |
| Business Logic        | 20%    |
| Software Architecture | 15%    |
| Code Quality          | 15%    |
| Critical Thinking     | 10%    |
| API Design            | 5%     |
| Security              | 5%     |
| Performance           | 5%     |
| Documentation         | 5%     |

# Submission Requirements

Submit a GitHub repository containing:

* Complete source code
* README.md
* API documentation
* ER Diagram
* Database schema explanation
* Setup instructions
* Sample `.env.example`
* Postman Collection (optional)

# README Should Include

* Project overview
* Assumptions made
* Architecture decisions
* Third-party packages used
* Challenges encountered
* Future improvements

# Extra Credit

These are not required but will distinguish exceptional candidates.

* CI/CD (GitHub Actions)
* Type hints throughout the project
* Linting (Ruff/Flake8)
* Formatting (Black)
* Pre-commit hooks
* Logging
* Rate limiting
* API versioning
* OpenAPI documentation
* Health check endpoint
* Monitoring-ready architecture

# Notes

You are free to make reasonable assumptions where requirements are ambiguous.
Document every major engineering decision.
We value clean architecture, maintainability, correctness, and thoughtful design more than the sheer number of implemented features.

