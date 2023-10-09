### 0x00. AirBnB clone - The console

- The complete web application will have:
    - A command interpreter or console to manipulate data without a visual interface, like in a Shell (perfect for development and debugging)
    - A website (the front-end) that shows the final product to everybody: static and dynamic
    - A database or files that store data (data = objects)
    - An API that provides a communication interface between the front-end and your data (retrieve, create, delete, update them)

##### Project Structure:
```
├── AUTHORS
├── README.md
├── TODO.md
├── change_perm
├── check_style
├── console.py
├── models
│   ├── __init__.py
│   ├── amenity.py
│   ├── base_model.py
│   ├── city.py
│   ├── engine
│   │   ├── __init__.py
│   │   └── file_storage.py
│   ├── place.py
│   ├── review.py
│   ├── state.py
│    └── user.py
├── push
├── run_tests
├── storage.json
├── tests
│   ├── __init__.py
│   ├── test_amenity.py
│   ├── test_base_model.py
│   ├── test_city.py
│   ├── test_file_storage.py
│   ├── test_place.py
│   ├── test_review.py
│   ├── test_state.py
|   └── test_user.py
```
