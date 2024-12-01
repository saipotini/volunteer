# Volunteer Tracker

## Overview
Volunteer Tracker is a web application that allows volunteers to log and track their volunteer hours across different organizations.

## Features
- User Registration and Authentication
- Log Volunteer Hours
- View Volunteer Hours History
- Track Total Volunteer Hours

## Prerequisites
- Python 3.8+
- pip (Python Package Manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone https://github.com/yourusername/volunteer-tracker.git
cd volunteer-tracker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python app.py
```

5. Run the application:
```bash
python app.py
```

6. Open a web browser and navigate to `http://localhost:5000`

## Technologies Used
- Flask
- SQLAlchemy
- Flask-Login
- SQLite

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License.
