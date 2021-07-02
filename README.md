## cornershop-backend-test

### Running the development environment

* `make up`
* `dev up`

##### Rebuilding the base Docker image

* `make rebuild`

##### Resetting the local database

* `make reset`

### Hostnames for accessing the service directly

* Local: http://127.0.0.1:8000



```
To avoid complexity in the front end, I limited the options 
that can be had per menu to three. However, the database
layout could accept more options per menu.

I am using django forms and templates because it is an internal platform 
and We can start as a monolithic.
```


* /employees/login

There are 2 users: super-admin and employees.

Employees can start a session and check the menu to select their option.

Super-admin can create menu with its options and verify what employees selected. We use super-admin django to generate this one.

Logo ut the user

* /employees/signup

In this form the employee can be added

* /orders/ordered/<uuid:menu_id>

This Url creates a new order into db
  
* /orders/list

This displays employees' orders that were selected
  
* /menu/<uuid:menu_id>

This form is used to select a menu option
  
* /menu/create

This forms is to create a menu. Only super-admin has access.

