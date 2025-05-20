# 🧪 Auto Test Case Generator

This project automates the generation and execution of API test cases using OpenAPI (Swagger) YAML files.  
It supports random payload generation, dynamic test case execution, and a flexible test framework.

---

## 🚀 Features

- ✅ Parses OpenAPI YAML files
- ✅ Generates Gherkin-based test scenarios automatically
- ✅ Sends API requests using `requests`
- ✅ Supports all HTTP methods: `GET`, `POST`, `PUT`, `PATCH`, `DELETE`
- ✅ Random JSON payload generation for `POST` and `PUT` requests using [Faker](https://faker.readthedocs.io/)
- ✅ Payloads saved to `.json` files for debugging and reuse

---

## 📁 Project Structure

```
auto\_testcase\_generator/
│
├── input.yaml                     # Your OpenAPI spec
├── generated\_file\_contents.py     # Helper for payloads, file writers, etc.
├── framework\_generator.py         # Core logic to parse spec and generate steps
├── features/
│   ├── sample.feature             # Gherkin-style feature file
│   └── steps/
│       └── sample\_step\_definitions.py  # Step implementations (uses requests)
├── post\_payload.json              # Randomly generated POST request body
├── put\_payload.json               # Randomly generated PUT request body
└── README.md                      # This file

````

---

## ⚙️ Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/auto_testcase_generator.git
cd auto_testcase_generator
````

### 2. Create a Virtual Environment (optional)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If there's no `requirements.txt`, install these manually:

```bash
pip install requests pyyaml faker behave
```

---

## 🧪 Running Tests

### 1. Generate Payload (Optional Manual Step)

```bash
python -c "from generated_file_contents import generate_post_payload; generate_post_payload('post')"
```

### 2. Run Tests Using `behave`

```bash
behave features/
```

---

## 🛠 Configuration

* Input your OpenAPI YAML spec as `input.yaml` (or pass a different one into your parser).
* Adjust the Faker-based random payloads in `generate_post_payload()`.

---

## 📌 Notes

* Payloads for `POST` and `PUT` are automatically created and stored as `post_payload.json` and `put_payload.json`.
* You can override `context.body` in custom steps if needed.
* Logs and response codes are printed to help debugging.

---


## 👨‍💻 Author

Created by [Nitin Kumar](https://linkedin.com/in/nitin30kumar/) — Contributions welcome!
