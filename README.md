# MyDBAids (MDBA)

## Overview
MyDBAids is a Python-based tool designed for generating data and managing databases. It offers a command-line interface for real-time interactions, allowing users to generate abstract data types like addresses, names, dates, and paragraphs. The tool intelligently handles complex database constraints and provides functionalities for database blueprint generation, custom modification, serialization, and more.

## Running the Tool
To use MyDBAids, you simply need to run it from the source code:

1. Clone the repository or download the source code.
2. Install the dependencies by running:
```bash
pip install -r requirements.txt
```
4. Navigate to the project directory.
5. Run the tool using Python. For example:
```bash
python main.py
```

## Usage
MyDBAids can be used for various database operations. Here are some common commands:

### Connect to a Database:

   ```bash
   mdba --user [username] --hostname [hostname] --password [password] --database [database]
   ```

### Initialize Blueprint Generation:

   ```bash
   mdba init
   ```

### Inject Data:

  ```bash
  mdba inject [nb_data]
  ```

### Update Abstract Type:

   ```bash
    mdba update
   ```

## Customizing Data Generation

1. Generate blueprints for your database.
2. Modify the JSON blueprints to conform to the data you want to generate.
3. The tool will read and serialize these blueprints for data generation.

## Documentation
For more detailed information, usage guides, and advanced topics, please visit our [MyDBAids Wiki](https://github.com/guillaume-schneider/mysql-generator-value/wiki/MySQL-Generator-Value-Wiki).

## Author
Guillaume SCHNEIDER

## Contact
For any queries, feel free to reach out to Guillaume at guillaumeschneider@siggraph.org.
