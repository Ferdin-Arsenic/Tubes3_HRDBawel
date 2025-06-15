# **ATS (Applicant Tracking System) Based on Digital CVs**

This application is a desktop-based Applicant Tracking System (ATS) designed to assist in the recruitment process. The system allows users to search for candidates based on keywords within a collection of digital CVs, automatically extract key information, and display concise candidate profiles.

This application was developed as part of the Major Project for IF2211 Algorithm Strategies.

---

## **Brief Explanation of Algorithms**

The exact match search feature in this application is implemented using three different string matching algorithms: **Knuth-Morris-Pratt (KMP)**, **Boyer-Moore (BM)**, and **Aho-Corasick**.

### **i. Knuth-Morris-Pratt (KMP) Algorithm**

The KMP algorithm is a string matching algorithm that works by avoiding comparisons of characters that have already been compared. The key to KMP's efficiency is preprocessing the pattern (keyword) to create an auxiliary table called the *Longest Proper Prefix which is also Suffix* (LPS) table.

This LPS table stores the length of the longest proper prefix that is also a suffix for each sub-pattern. When a mismatch occurs while comparing the text with the pattern, the algorithm does not shift the pattern one character at a time. Instead, it uses the value from the LPS table to make an intelligent jump to the next most likely matching position. This significantly reduces the number of comparisons and makes KMP very efficient.

### **ii. Boyer-Moore (BM) Algorithm**

The Boyer-Moore algorithm is another string matching algorithm that is often faster in practice than KMP, especially for large alphabets. The uniqueness of this algorithm is that it starts the comparison process from the **last** character of the pattern, not the first.

When a mismatch occurs, BM uses two heuristics to shift the pattern as far as possible:

1.  **Bad-Character Heuristic**: If the mismatched character in the text (`T[i]`) exists within the pattern, the pattern is shifted to align `T[i]` with its last occurrence in the pattern. If it does not exist, the pattern is shifted completely past that character.
2.  **Good-Suffix Heuristic**: If a part of the pattern's suffix has already matched the text, the pattern is shifted to align with the next occurrence of that matched suffix within the pattern.

With these two heuristics, BM can often skip large portions of the text in a single shift, making it extremely fast.

### **iii. Aho-Corasick Algorithm**

The Aho-Corasick algorithm is a highly efficient multi-pattern matching algorithm. Unlike KMP or BM, which search for one pattern at a time, Aho-Corasick is designed to find all occurrences of a **set of keywords (a dictionary)** simultaneously in a **single pass** through the text.

It works by building a finite state machine data structure, shaped like a *Trie* (prefix tree), from all the keywords. Additionally, the algorithm adds *failure links* to each node. If a mismatch occurs at a certain character, the algorithm follows a failure link to another state that represents the next longest possible matching prefix, without needing to backtrack in the text. This allows for very fast searching for many keywords at once.

---

## **Program Requirements and Installation**

The following software and libraries are required to run the application.

### **Software Requirements**

* **Python**: Version 3.10 or newer.
* **MySQL Server**: The application requires a connection to a MySQL database. You can use a standalone MySQL installation or a package like **XAMPP** or **WAMP**.

### **Python Library Installation**

1.  **Create a Virtual Environment (Recommended)**
    Open a terminal or command prompt in the project's root directory and run the following command to create a virtual environment:
    ```bash
    python -m venv .venv
    ```

2.  **Activate the Virtual Environment**
    * **On Windows (Command Prompt):**
        ```cmd
        .\.venv\Scripts\activate
        ```
    * **On macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

3.  **Install Required Libraries**
    With the virtual environment activated, install all necessary libraries with the following command:
    ```bash
    pip install PyQt6 PyMuPDF mysql-connector-python
    ```

### **Database Configuration**

1.  Create a new database on your MySQL server (e.g., named `db_ats_stima`).
2.  Import the `database.sql` file (or any other provided seeding file) into your newly created database to populate the tables and initial data.
3.  **IMPORTANT**: Adjust the database connection details (host, user, password, and database name) in the `src/database/cv_database.py` file to match your local configuration.

---

## **How to Run the Program**

After all requirements and configurations are set up, you can run the application by executing the main script.

Make sure you are in the project's root directory with your virtual environment activated, then run the following command in the terminal:

```bash
python src/main.py
```

The application window will open, and it will be ready to use.

---

## **Authors**

This project was developed by Group **HRD Bawel**:

| Name                         | NIM      |
| ---------------------------- | -------- |
| Syahrizal Bani Khairan       | 13523063 |
| Muhammad Iqbal Haidar        | 13523111 |
| Ferdin Arsenarendra Purtadi  | 13523117 |