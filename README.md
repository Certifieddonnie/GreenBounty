![image](https://github.com/Certifieddonnie/GreenBounty/assets/98459984/3ae739cb-da0f-475a-b528-840949774437)



# GreenBounty API
Welcome to the documentation of GreenBounty API! This API provides a wide range of information about fruits and vegetables, including boanical names, type of vitamin present, nutritional benefits, PH values, side effects and preservation method. Whether you're a developer building for the food industry, a nutritionist, chef, or simply a fruit and veggie enthusiast, this API will help you access comprehensive data about various fruits and vegetables. It has simply has got you covered.

# Table of Contents

1. [Getting Started](#getting-started)
2. [API Endpoints](#api-endpoints) 
    - [Authentication](#authentication)
        - [Welcome view](#welcome-view)
        - [Register](#register)
        - [Login](#login)
        - [User profile](#user-profile)
        - [Update profile](#update-profile)
        - [Change password](#change-password)
        - [Delete user](#delete-user)
    - [Item Search](#item-search)
        - [All items](#all-items)
        - [One_item](#one-item)
3. [Error Handling](#error-handling)
4. [Examples](#examples)
5. [Contributing](#contributing)
6. [License](#license)

## Getting Started

To begin using the GreenBounty API, you can simply make requests to the available API endpoints listed below. User authentication is required for accessing the basic information about fruits and vegetables.

## API Endpoints

## Authentication

### Welcome view
**Endpoint:** `/api/vi/auth`

**Method:** "GET"

**Example Request**
```
GET /api/vi/auth
```
**Response:** This request leads you to the welcome view.

### Register
**Endpoint:** `/api/vi/auth/register`

**Method:** "POST"

**Example Request**
```
/api/vi/auth/register
```
**Response:** This request enables new users to enter their details and thereafter use to get logged in.

### Login
**Endpoint:** `/api/vi/auth/login`

**Method:** "POST"

**Example Request**
```
/api/vi/auth/login
```
**Response:** This request leads old users to the page where they enter their login details and get logged in to utilise and consume the API.

### User profile
**Endpoint:** `/api/vi/auth/user`

**Method:** "GET"

**Example Request**
```
GET /api/vi/auth/user
```
**Response:**  It serves as a representation of a user's identity and contains details that are relevant to the user's interactions, preferences, and personalization within the given context.

### Update profile
**Endpoint:** `/api/vi/auth/update_profile/<int:pk>/`

**Method:** "POST"

**Example Request**
```
/api/vi/auth/update_profile/<int:pk>/
```
**Response:**  This enables a user to update parameters in their user profile to their preference.

### Change password
**Endpoint:** `/api/vi/auth/change_password/<int:pk>/`

**Method:** "POST"

**Example Request**
```
/api/vi/auth/change_password/<int:pk>/
```
**Response:**  This request gives users the access to change the password associated with their account.

### Delete user
**Endpoint:** `/api/vi/auth/delete_user/<int:pk>/`

**Method:** "DELETE"

**Example Request**
```
/api/vi/auth/delete_user/<int:pk>/
```
**Response:**  This request enables the user to delete their account associated with GreenBounty API


## Item search
Search for fruits or vegetables based on a keyword or partial name.

### All Fruits

**Endpoint:** `/api/vi/fruits`

**Method:** "GET"

```
GET /api/vi/fruits
```
**Example Response**
```
{
  "results": [
    {
      "name": "Banana",
      "botanical name": "Musa spp",
      "Vitamins": "B6 Pyridoxine",
      "ph value": "4.5 - 5.2"
    },
 {
      "name": "Spinach",
      "botanical name": "Spinacia oleracea",
      "Vitamins": "Vitamin K",
      "ph value": "6.0 - 7.0"
    },
  ]
}

```
This request returns all items in the database, according to their id. 

### One item

**Endpoint:** `/api/vi/fruits/search`

**Method:** "GET"

**Parameters:** 
- query (required): The keyword or partial name to search for. (e.g banana)

**Example Request**

**Query search by name**
```
GET /api/vi/fruits/search?name=banana
```
**Example Response**
```
{
  "results": [
    {
      "name": "Banana",
      "botanical name": "Musa spp",
      "Vitamins": "B6 Pyridoxine",
      "ph value": "4.5 - 5.2"
    },
  ]
}

```

**Query search by Botanical name**
```
GET /api/vi/fruits/search?botan=Musa spp
```
**Example Response**
```
{
  "results": [
    {
      "name": "Banana",
      "botanical name": "Musa spp",
      "Vitamins": "B6 Pyridoxine",
      "ph value": "4.5 - 5.2"
    },
  ]
}

```

## Examples

Usage samples and code snippets
```
/api/vi/auth/register
```
![image](https://github.com/Certifieddonnie/GreenBounty/assets/81980032/af3a6c6c-bc4c-404c-82d3-8bd4bc453434)


## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or open a pull request.

## License

This API is released under the MIT License.

