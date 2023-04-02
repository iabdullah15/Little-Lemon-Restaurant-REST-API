# Little-Lemon-Restaurant-REST-API

The admin panel username is admin and password is 123. (http://127.0.0.1:8000/admin/)

The app consists of two groups of users. The users are divided into these groups using the built-in Django Group model. 
Manager
Delivery crew

For user authentication, the Djoser library for Django REST Framework has been used for token authentication.
Following are some of the useful api endpoints for user registration and token generation: 

i) /api/users, METHOD: POST, Creates a new user with name, email and password.
ii) /api/users/me, METHODS: GET, PUT, PATCH, Use this endpoint to retrieve/update the authenticated user.
iii) /token/login/, METHOD: POST, Generates access tokens that can be used in other API calls in this project.


# The Rest of the api endpoints below are formatted in the following way:
API Endpoint
Role
Method
Purpose


Menu-items endpoints

/api/menu-items
Customer, delivery crew
GET
Lists all menu items. Return a 200 – Ok HTTP status code

/api/menu-items
Customer, delivery crew
POST, PUT, PATCH, DELETE
Denies access and returns 403 – Unauthorized HTTP status code


/api/menu-items/{menuItem}
Customer, delivery crew
GET
Lists single menu item

/api/menu-items/{menuItem}
Customer, delivery crew
POST, PUT, PATCH, DELETE
Returns 403 - Unauthorized

 
/api/menu-items
Manager
GET
Lists all menu items


/api/menu-items
Manager
POST
Creates a new menu item and returns 201 - Created


/api/menu-items/{menuItem}
Manager
GET
Lists single menu item


/api/menu-items/{menuItem}
Manager
PUT, PATCH
Updates single menu item


/api/menu-items/{menuItem}
Manager
DELETE
Deletes menu item



User group management endpoints


/api/groups/manager/users
Manager
GET
Returns all managers



/api/groups/manager/users
Manager
POST
Assigns the user in the payload to the manager group and returns 201-Created




/api/groups/manager/users/{userId}
Manager
DELETE
Removes this particular user from the manager group and returns 200 – Success if everything is okay.
If the user is not found, returns 404 – Not found



/api/groups/delivery-crew/users
Manager
GET
Returns all delivery crew



/api/groups/delivery-crew/users
Manager
POST
Assigns the user in the payload to delivery crew group and returns 201-Created HTTP



/api/groups/delivery-crew/users/{userId}
Manager
DELETE
Removes this user from the manager group and returns 200 – Success if everything is okay.
If the user is not found, returns  404 – Not found





Cart management endpoints 

/api/cart/menu-items
Customer
GET
Returns current items in the cart for the current user token



/api/cart/menu-items
Customer
POST
Adds the menu item to the cart. Sets the authenticated user as the user id for these cart items


/api/cart/menu-items
Customer
DELETE
Deletes all menu items created by the current user token




Order management endpoints

/api/orders
Customer
GET
Returns all orders with order items created by this user



/api/orders
Customer
POST
Creates a new order item for the current user. Gets current cart items from the cart endpoints and adds those items to the order items table. Then deletes all items from the cart for this user.



/api/orders/{orderId}
Customer
GET
Returns all items for this order id. If the order ID doesn’t belong to the current user, it displays an appropriate HTTP error status code.



/api/orders
Manager
GET
Returns all orders with order items by all users




/api/orders/{orderId}
Manager
PUT, PATCH
Updates the order. A manager can use this endpoint to set a delivery crew to this order, and also update the order status to 0 or 1.
If a delivery crew is assigned to this order and the status = 0, it means the order is out for delivery.
If a delivery crew is assigned to this order and the status = 1, it means the order has been delivered.


/api/orders/{orderId}
Manager
DELETE
Deletes this order



/api/orders
Delivery crew
GET
Returns all orders with order items assigned to the delivery crew



/api/orders/{orderId}
Delivery crew
PATCH
A delivery crew can use this endpoint to update the order status to 0 or 1. The delivery crew will not be able to update anything else in this order.
