# Your Django App Name

A brief description of your Django application.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)


## Features

- List key features or functionalities of your Django app.

## Prerequisites

List the prerequisites that users need to have before using your app. This could include:

- Python 3.10
- Django 4.2
- database system PostgreSQL(for production), SQLite(for dev)

## Installation

Provide step-by-step instructions on how to install your app:

1. Clone the repository:
   ```bash
   git clone git@github.com:mostafanawam/e_commerce.git
   cd e_commerce/

2. Create a virtual environment and activate it:
   ```bash
   python3 -m venv venv
   source venv/bin/activate

3. Install dependencies:
   ```bash
   make install

4. Migrate the database:
    ```bash
    make setup

5. load static data:
    ```bash
    make static  

6. Start the development server:
    ```bash
    make backend-server-start

