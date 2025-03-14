# Project Title: SWF Configuration Manager

## Overview
SWF Configuration Manager is a simple web application built using Flask that allows users to manage configuration settings through a web interface. The application provides endpoints to read, create, update, and delete configuration keys stored in a JSON file.

## Project Structure
```
swf
├── static
│   ├── css
│   │   └── styles.css
│   ├── js
│   │   └── scripts.js
├── templates
│   └── index.html
├── app.py
├── config.json
└── README.md
```

## Files Description
- **static/css/styles.css**: Contains the CSS styles for the web frontend, defining the visual appearance of the HTML elements.
- **static/js/scripts.js**: Contains JavaScript code for client-side interactions, handling AJAX requests to the Flask backend and updating the UI dynamically.
- **templates/index.html**: The main HTML template for the web frontend, serving as the entry point for the user interface and including links to the CSS and JavaScript files.
- **app.py**: The Flask application code that defines API endpoints for managing the configuration and serves the HTML template for the frontend.
- **config.json**: Stores the configuration data in JSON format, used by the Flask application to read and write configuration settings.

## Setup Instructions
1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd swf
   ```

2. **Install dependencies**:
   Make sure you have Python and pip installed. Then, install Flask:
   ```
   pip install Flask
   ```

3. **Run the application**:
   ```
   python app.py
   ```
   The application will start on `http://127.0.0.1:5000`.

4. **Access the web interface**:
   Open your web browser and navigate to `http://127.0.0.1:5000/config` to view and manage the configuration settings.

## Usage
- **GET /config**: Retrieve the current configuration.
- **POST /config**: Create or update configuration keys by sending a JSON object in the request body.
- **DELETE /config/<key>**: Delete a specific configuration key by providing the key in the URL.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for details.