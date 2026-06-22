# NHS Postcode & ODS Code Router

A lightweight, enterprise-ready Python command-line utility that maps UK postcodes to their national NHS administrative boundaries and routes them to local primary care infrastructure (GP Practices and Primary Care Networks) using real-time ODS codes.

## Features
* **Live API Integration:** Connects seamlessly with the open-source Postcodes.io API to fetch live regional health authority data.
* **Hierarchical ODS Routing:** Simulates a central Organisation Data Service (ODS) lookup matrix to resolve local GP surgeries and PCN allocations.
* **Robust Input Sanitisation:** Utilises regular expressions (Regex) to validate and standardise diverse UK postcode formats seamlessly.
* **Continuous Interface:** A user-friendly, continuous command-line loop allowing multiple lookups without restarting the script.
* **Modern Tooling:** Built using `uv` for lightning-fast dependency management and fully linted/formatted with the modern `Ruff` toolchain.

## How the Routing Architecture Works
UK health geography is managed through distinct administrative tiers. This utility bridges national geographic boundaries with local healthcare providers:

1. **Format Validation:** Filters and normalises input using a strict UK postcode regex.
2. **National Boundary Resolution:** Calls the external registry to extract the structural Integrated Care Board (ICB) details and its corresponding national ODS code.
3. **Primary Care Routing:** Extracts the geographical outcode sector to map the patient directly to their allocated local GP practice and Primary Care Network (PCN) via a structured ODS lookup table.

## Getting Started

### Prerequisites
* Python 3.8 or higher installed on your system.
* [uv](https://github.com/astral-sh/uv) installed.

### Installation
1. Clone this repository to your local machine:

```bash
git clone https://github.com/JHerron1990/nhs-number-validator.git
```

2. Navigate into the project folder:

```bash
cd nhs-number-validator
```

## Running the Application
Instead of manually managing virtual environments, use uv to safely execute the script with a single command:

```bash
uv run nhs_postcode_router.py
```

## Development & Linting
This project uses Ruff for linting and formatting. You can run these commands instantly using uv without needing to install anything globally:

* Check code for quality/errors:

```bash
uv x ruff check
```

* Auto-format code cleanly:

```bash
uv x ruff format
```

## License
This project is licensed under the MIT Licence.