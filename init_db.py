import sqlite3
import os
import re

def init_sqlite_db():
    schema_path = os.path.join(os.path.dirname(__file__), 'sql', 'schema.sql')
    db_path = os.path.join(os.path.dirname(__file__), 'database.sqlite')

    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = f.read()

    # Simple conversion from MySQL syntax to SQLite syntax for basic structures
    schema = schema.replace('AUTO_INCREMENT', 'AUTOINCREMENT')
    schema = schema.replace('TINYINT(1)', 'INTEGER')
    schema = schema.replace(' INT ', ' INTEGER ')
    schema = schema.replace(' INT,', ' INTEGER,')
    schema = schema.replace('DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP', 'DATETIME DEFAULT CURRENT_TIMESTAMP')

    schema = schema.replace('ENUM("ok","atencao","grave")', 'TEXT')
    schema = schema.replace('ENUM("barra","linha")', 'TEXT')
    schema = schema.replace('ENUM("imagem","texto")', 'TEXT')

    schema = schema.replace('INTEGER AUTOINCREMENT PRIMARY KEY', 'INTEGER PRIMARY KEY AUTOINCREMENT')

    # Remove INDEX from CREATE TABLE
    schema = re.sub(r',\s*INDEX idx_status_data \(data\)', '', schema)

    # Separate statements
    statements = [s.strip() for s in schema.split(';') if s.strip()]

    # We add the index manually
    statements.append("CREATE INDEX idx_status_data ON status_qualidade_dia (data)")

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for statement in statements:
        try:
            cursor.execute(statement)
        except Exception as e:
            print(f"Error executing statement:\n{statement}\nException: {e}")

    conn.commit()
    conn.close()
    print("Database initialized successfully at", db_path)

if __name__ == '__main__':
    db_path = os.path.join(os.path.dirname(__file__), 'database.sqlite')
    if os.path.exists(db_path):
        os.remove(db_path)
    init_sqlite_db()
