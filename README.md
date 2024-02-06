# Lookup Table Export for Startel® Soft Switch

This is not an official Startel® tool and the provided license should not be
construed to override any rights or licenses of Startel® Corporation or its
subsidiaries.

## Setup

This guide assumes you have Windows because the Soft Switch is generally acccessed from Windows only.

Make sure to install Python 3.8.5 or later.

Clone the repository or download it as a zip file from GitHub.

Open your preferred command line tool and change to the directory where the repository/source is stored.

Create a virtual environment:

```
virtualenv venv
```

Activate it:

```
.\venv\Scripts\activate
```

Install the required dependencies:

```
pip install -r requirements.txt
```

Then run the script:

```
python export.py --user softswitchuser --password softswitchpassword --switch-url https://x.x.x.x --out out.csv
```