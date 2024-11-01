# Bakdroid

**Bakdroid** is a command-line tool for unpacking backup files with support for decryption and decompression.

## Features

- **Unpack Backup Files**: Extract data from various backup file formats.
- **Decryption Support**: Securely decrypt encrypted backup files using a password.
- **Compression Handling**: Automatically decompress data if the backup is compressed.
- **Verbose Logging**: Enable detailed logging for troubleshooting and monitoring.
- **Versioning**: Easily check the installed version of Bakdroid.

## Installation

### Prerequisites

- **Python 3.13** or higher
- **pip** (Python package installer)

### Install via Pip

Bakdroid will also be available on PyPI. You can install it using pip:

```bash
pip install bakdroid
```

### Install from Source

If you prefer to build and install Bakdroid from source, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/zahidaz/bakdroid.git
   cd bakdroid
   ```

2. **Install Dependencies with Poetry**

   Ensure you have [Poetry](https://python-poetry.org/) installed. If not, install it using:

   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

   Then, install the project dependencies:

   ```bash
   poetry install
   ```

3. **Build the Package**

   ```bash
   poetry build
   ```

4. **Install the Package**

   After building, install the package using pip:

   ```bash
   pip install dist/bakdroid-0.1.0-py3-none-any.whl
   ```

## Usage

Bakdroid provides a simple command-line interface to unpack backup files.

### Unpack Command

```bash
bakdroid unpack [OPTIONS] INPUT_FILE OUTPUT_FILE
```

#### Arguments

- `INPUT_FILE`: Path to the input backup file (e.g., `backup.en.ab`).
- `OUTPUT_FILE`: Path to the output tar file.

#### Options

- `--password, -p`: Password to decrypt the backup file.
- `--verbose, -v`: Enable verbose output.
- `--version, -V`: Show the version of Bakdroid.

#### Examples

- **Basic Unpack**

  ```bash
  bakdroid unpack backup.ab backup.tar
  ```

- **Unpack with Decryption**

  ```bash
  bakdroid unpack -p yourpassword backup.en.ab backup.tar
  ```

- **Unpack with Verbose Logging**

  ```bash
  bakdroid unpack -v backup.ab backup.tar
  ```

- **Combine Options**

  ```bash
  bakdroid unpack -p yourpassword -v backup.en.ab backup.tar
  ```

- **Check Version**

  ```bash
  bakdroid --version
  ```

## License

This project is licensed under the [MIT License](LICENSE).
