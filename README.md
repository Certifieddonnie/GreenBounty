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
    - [Search](#search)
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

**Method:** "GET"

**Example Request**
```
GET /api/vi/auth/register
```
**Response:** This request enables new users to enter their details and thereafter use to get logged in.

### Login
**Endpoint:** `/api/vi/auth/login`

**Method:** "GET"

**Example Request**
```
GET /api/vi/auth/login
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
**Endpoint:** `/api/vi/auth/update_profile`

**Method:** "GET"

**Example Request**
```
GET /api/vi/auth/update_profile
```
**Response:**  This enables a user to update parameters in their user profile to their preference.

### Change password
**Endpoint:** `/api/vi/auth/change_password`

**Method:** "GET"

**Example Request**
```
GET /api/vi/auth/change_password
```
**Response:**  This request gives users the access to change the password associated with their account.

### Delete user
**Endpoint:** `/api/vi/auth/delete_user`

**Method:** "GET"

**Example Request**
```
GET /api/vi/auth/delete_user
```
**Response:**  This request enables the user to delete their account associated with GreenBounty API


## Search
Search for fruits or vegetables based on a keyword or partial name.

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

## Error Handling

Content for the "Error Handling" section goes here.

## Examples

Usage samples and code snippets

## Contributing

Contributions are welcome! If you find any bugs or have suggestions for improvements, please submit an issue or open a pull request.

## License

This API is released under the MIT License.

