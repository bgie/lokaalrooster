# lokaalrooster
Eenvoudige webpagina om lessenroosters per lokaal te tonen op groot scherm met een klok

## Setup

This project uses `uv` to manage the virtual environment.

1.  **Install uv**:
    If you don't have `uv` installed, follow the instructions on the [official `uv` website](https://astral.sh/docs/uv#installation).

2.  **Create the virtual environment and install dependencies**:
    Run the setup script:
    ```bash
    sh setup.sh
    ```
    This will create a `.venv` directory with all the necessary packages.

3.  **Activate the virtual environment**:
    ```bash
    source .venv/bin/activate
    ```

## Data Files

The application requires three data files in the `data` directory:

- `config.json`: This file contains the main configuration for the application. You can start by copying `data/config.example.json` to `data/config.json`.
- `rooms.json`: This file defines the different rooms. An example is provided. Each room should have a `name` and a `color`.
- `schedule.json`: This file contains the actual schedule. You will need to provide this file yourself with your schedule data.
