# 🚀 SchemaLence

<div align="center">

### Cyberpunk PostgreSQL Database Explorer & Schema Intelligence Platform

**SchemaLence** is a powerful PostgreSQL database schema viewer and data exploration tool featuring a modern cyberpunk-inspired desktop interface. Designed for developers, database administrators, data engineers, and analysts, it provides deep database introspection, schema visualization, and data exploration capabilities.

<p align="center">
  <img src="logo.png" alt="SchemaLence Logo" width="200">
</p>

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-9.6+-336791)
![Desktop App](https://img.shields.io/badge/Desktop-Tkinter-green)
![License](https://img.shields.io/badge/License-Educational-lightgrey)
![Version](https://img.shields.io/badge/Version-1.0.0-orange)

</div>

---

## 📖 Overview

SchemaLence simplifies PostgreSQL database exploration by providing a visually appealing and highly informative interface for understanding database structures, relationships, constraints, indexes, triggers, and data.

Whether you're onboarding to a new project, documenting an existing database, troubleshooting schema issues, or analyzing production systems, SchemaLence provides a fast and intuitive way to understand your PostgreSQL environment.

---

## ✨ Features

### 🔌 Flexible Database Connection

Connect to PostgreSQL databases using multiple methods:

#### Connection String

```text
postgresql://user:password@host:port/database
```

#### Manual Connection Form

* Host
* Port
* Database Name
* Username
* Password
* SSL Mode Support

---

### 🗂️ Schema Browser

Navigate database structures effortlessly through an interactive sidebar.

Features include:

* Sidebar navigation for all tables
* Quick table selection
* Visual highlighting
* Instant schema loading
* Complete database documentation view
* "View All Schemas" mode

---

### 🔍 Comprehensive Schema Analysis

SchemaLence automatically extracts detailed metadata for every table.

#### Table Information

* Table descriptions
* Metadata
* Row counts

#### Column Analysis

* Column names
* Data types
* Nullable status
* Default values

#### Relationship Mapping

* Foreign key relationships
* Referenced tables
* Dependency tracking

#### Constraints

* Primary keys
* Unique constraints
* Check constraints
* ENUM allowed values

#### Database Objects

* Indexes
* Triggers

#### Data Insights

* Row counts
* Example records
* Sample data previews

---

### 📊 Data Grid Explorer

Inspect live table data directly within the application.

Features:

* Display up to 500 rows
* Sortable columns
* Horizontal scrolling
* Vertical scrolling
* Fast navigation between records

---

### 📤 Export & Productivity Tools

| Feature                | Description                            |
| ---------------------- | -------------------------------------- |
| 📥 Export CSV          | Export table data to CSV files         |
| 📋 Copy Schema         | Copy schema documentation to clipboard |
| 📋 Copy Visible Data   | Copy currently visible records         |
| ⚡ One-Click Disconnect | Instantly disconnect from database     |

---

---

# 📋 Prerequisites

Before installing SchemaLence, ensure you have:

| Requirement     | Version  |
| --------------- | -------- |
| Python          | 3.11+    |
| PostgreSQL      | 9.6+     |
| Database Access | Required |

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone <repository-url>
cd SchemaLens
```

---

## 2. Create a Virtual Environment

### Linux / macOS

```bash
python -m venv venv
source venv/bin/activate
```

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install ttkbootstrap psycopg2-binary pandas
```

---

## 4. Run the Application

```bash
python app.py
```

---

# 🏗️ Building the Executable

Create a standalone executable using PyInstaller.

## Install PyInstaller

```bash
pip install pyinstaller
```

## Build Executable

```bash
pyinstaller SchemaLence.spec
```

After completion, the executable will be available inside:

```text
dist/
```

---

# 🚀 Usage

## Connecting to a Database

### Option A — Connection String

Paste your PostgreSQL connection string:

```text
postgresql://user:password@host:port/database
```

Click:

```text
CONNECT VIA STRING
```

---

### Option B — Manual Form

Enter:

| Field    | Example     |
| -------- | ----------- |
| Host     | localhost   |
| Port     | 5432        |
| Database | my_database |
| Username | postgres    |
| Password | ********    |

Click:

```text
TEST & CONNECT
```

---

## Exploring Schemas

### Single Table View

1. Select a table from the sidebar.
2. Review schema details.
3. Switch between:

* SCHEMA VIEW
* DATA GRID

4. Use export and copy actions as needed.

---

### View All Schemas

Click:

```text
⚡ VIEW ALL SCHEMAS
```

This mode provides:

* Complete database documentation
* Full schema inspection
* Cross-table analysis
* Clipboard export support

---

## Exporting Data

### Export CSV

Click:

```text
📥 EXPORT CSV
```

Downloads table data to a CSV file.

---

### Copy Visible Data

Click:

```text
📋 COPY ALL VISIBLE
```

Copies currently visible records.

---

### Copy Schema Documentation

Click:

```text
📋 COPY SCHEMA TO CLIPBOARD
```

Copies schema metadata and documentation.

---

# 📦 Dependencies

| Package         | Purpose                              |
| --------------- | ------------------------------------ |
| ttkbootstrap    | Modern themed Tkinter widgets        |
| psycopg2-binary | PostgreSQL database adapter          |
| pandas          | Data manipulation and analysis       |
| tkinter         | GUI framework (included with Python) |

---

# 🗄️ Database Compatibility

SchemaLence supports:

* PostgreSQL 9.6+
* Managed PostgreSQL services
* Self-hosted PostgreSQL instances

Required access:

```sql
information_schema
pg_catalog
```

---

# 🔒 Security Notes

SchemaLence follows security-conscious design principles.

### Credential Handling

* Credentials remain in memory only
* No credential persistence
* No password logging

### SSL Support

* SSL mode enabled by default
* Secure form-based connections

### Privacy

* No telemetry
* No credential storage
* No external data transmission

---

# 🤝 Contributing

Contributions are welcome and appreciated.

### How to Contribute

1. Fork the repository

```bash
git clone your-fork-url
```

2. Create a feature branch

```bash
git checkout -b feature/amazing-feature
```

3. Commit changes

```bash
git commit -m "Add amazing feature"
```

4. Push your branch

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

---

# 📄 License

This project is provided **as-is** for educational and professional use.

Please review the repository for any future licensing updates.

---

# 👨‍💻 Author

### SchemaLence

**Database Architect Tool**

Designed to help developers and database professionals explore, understand, and document PostgreSQL databases efficiently.

---

# 🛣️ Roadmap

Future enhancements may include:

* MySQL support
* SQL Server support
* Database diagram generation
* Relationship visualization
* Query editor
* Saved connections
* Dark/Light theme switching
* Advanced filtering
* Schema diff comparison
* AI-assisted schema analysis

---

# 📌 Version

Current Version:

```text
v1.0.0
```

---

<div align="center">

### ⚡ Explore PostgreSQL Schemas Faster

Built for Developers • DBAs • Data Engineers • Analysts
##
SCREENSHOTS 
<img width="1919" height="1006" alt="SchemaLence" src="https://github.com/user-attachments/assets/925b88ce-67c5-444c-ab7a-dcf9db1b8e76" />
|->
<img width="1916" height="1003" alt="1" src="https://github.com/user-attachments/assets/ff310fc2-b7c2-4851-8908-a95729e10a97" />
|->
<img width="1904" height="1004" alt="2" src="https://github.com/user-attachments/assets/f9260895-d6a0-43b4-b148-7f917b097eb3" />
|->
<img width="1919" height="1005" alt="3" src="https://github.com/user-attachments/assets/e202e772-3c55-4a98-a1cd-b63465d333d9" />
|->
<img width="1919" height="1003" alt="4" src="https://github.com/user-attachments/assets/6ed864df-606d-41bc-ab71-0c60b7839c6e" />

</div>

