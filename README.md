# Development and tools

## Tech stack :

Frontend : Flutter

API : Flask

Backend : Python

Database : MongoDB

## Login page :
*Components*

1. Email input box
2. Password input box
3. Submit button (POST)

&nbsp;

```http
  https://dh-oyl4.onrender.com/login
```

| Parameter | Return Type     | Return Object                  |
| :-------- | :------- | :-------------------------------- |
| `if logged in`      | `json` | {”authentication”: True}|
| `else`      | `json` | {”authentication”: False}|



## Sign up page:

*Components*

1. Email input box
2. Password input box
3. Repeat password input box
4. Name input box
5. Profession dropdown menu :
    - Student
    - Faculty
    - Working professional
6. Year of study (If student) dropdown menu :
    - Year 1
    - Year 2
    - Year 3
    - Year 4
7. Interest drop down menu :
    - Projects
    - Research work
    - Group study
8. Collaboratoin with
    - Student
    - Faculty
    - Working professional
9. Topic of collaboration input box
10. User’s skillset input box
11. Experience (If professional) number menu 
12. Submit button (POST)

&nbsp;

```http
  https://dh-oyl4.onrender.com/login
```

| Parameter | Return Type     | Return Object                      |
| :-------- | :------- | :-------------------------------- |
| `If email already exists`      | `json` | {"signup":"exists"} |
| `elseif password mismatch`      | `json` | {"signup":"mismatch"} |
| `else`      | `json` | {"signup":"success"} |
