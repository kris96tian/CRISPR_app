# CRISPR gRNA Tool

## Visit at: [https://crisprapp.pythonanywhere.com/](https://crisprapp.pythonanywhere.com/)

## Overview

The CRISPR gRNA Tool is a web application developed using Python and Flask to assist researchers in identifying potential guide RNA (gRNA) target sites within a given DNA sequence. It focuses on the CRISPR-Cas9 system and detects 20-nucleotide sequences followed by the canonical NGG Protospacer Adjacent Motif (PAM) on the forward strand.

This tool provides a user-friendly interface to analyze DNA sequences and quickly locate potential gRNA binding sites, along with essential information for downstream analysis.

## Key Features

* **PAM Site Detection:** Identifies all occurrences of 20-nucleotide sequences followed by the 'NGG' PAM motif.
* **DNA Sequence Validation:** Ensures the input sequence contains only valid DNA bases (A, T, C, G).
* **Flexible Input:** Accepts DNA sequences with mixed casing and common whitespace characters (spaces, newlines).
* **GC Content Calculation:** Computes and displays the percentage of Guanine (G) and Cytosine (C) in each identified 20-mer guide sequence.
* **Example Sequences:** Includes pre-defined example sequences for easy testing and demonstration.
* **Analysis History:** Persists a history of analyzed sequences and their results using a MySQL database hosted on PythonAnywhere.
* **Session Management:** Allows users to start new analysis sessions with options to clear history.
* **Export Functionality:** Enables users to download individual analysis sessions (input sequence and results) as JSON files.

## Installation

To run this application locally, you will need Python 3.11 installed on your system.

1.  **Clone the repository (if you have it on GitHub):**
    ```bash
    git clone [repository URL]
    cd [repository name]
    
    ## Create a virtual environment (recommended):**
    python -m venv venv
    
    source venv/bin/activate  # On macOS and Linux
    # venv\Scripts\activate   # On Windows
    ## Install the required dependencies:**
    pip install Flask Flask-SQLAlchemy mysqlclient

    ##Usage:
    python app.py
    ```
2.  **Open your web browser:** Navigate to `http://127.0.0.1:5000/` (or the address provided in your terminal).
3.  **Enter your DNA sequence:** Paste your DNA sequence into the text area on the homepage.
4.  **Click "Find gRNA Targets":** The results will be displayed below the input area.
5.  **Explore Examples:** Use the "Use" buttons next to the example sequences to quickly populate the input.
6.  **View History:** Access the analysis history by clicking the "History" link in the navigation bar.
7.  **Export Analysis:** From the history page, you can export individual analysis results as JSON files.
8.  **New Session:** Use the "New Session" button on the homepage to start a fresh analysis. You'll be prompted if you want to clear the history.

## Database

The application now uses a **MySQL** database hosted on **PythonAnywhere** to store the history of analyses. The application connects to the database named `crisprapp$default` using the username `crisprapp`.

**Note for PythonAnywhere Deployment:** When deploying on PythonAnywhere, ensure that the `SQLALCHEMY_DATABASE_URI` in your `app.py` file is correctly configured with your MySQL connection details (username, password, host, and database name) as provided by PythonAnywhere. You also need to install the `mysqlclient` library in your PythonAnywhere virtual environment.
