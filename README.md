# MySQL Generator Value

## Overview
MySQL Generator Value is a Python-based tool designed for generating MySQL data and managing MySQL databases. It offers a command-line interface for real-time interactions, allowing users to generate abstract data types like addresses, names, dates, and paragraphs. The tool intelligently handles complex database constraints and provides functionalities for database blueprint generation, custom modification, serialization, and more.

## Installation
To install MySQL Generator Value, follow these steps:

1. Clone the repository or download the source code.
2. Navigate to the project directory.
3. Run the following command:

python setup.py install


This will install the package along with its dependencies.

## Usage
MySQL Generator Value can be used for various database operations. Here are some common commands:

- **Connect to a Database:**

  ```bash
mysqlgen --user [username] --hostname [hostname] --password [password] --database [database]


- **Initialize Blueprint Generation:**

  ```bash
mysqlgen init

- **Inject Data:**

  ```bash
mysqlgen inject [nb_data]

- **Update Abstract Type:**

  ```bash
mysqlgen update


## Customizing Data Generation
1. Generate blueprints for your database.
2. Modify the JSON blueprints to conform to the data you want to generate.
3. The tool will read and serialize these blueprints for data generation.

## Author
Guillaume SCHNEIDER

## Contact
For any queries, feel free to reach out to Guillaume at guillaumeschneider@siggraph.org.
