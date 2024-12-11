# Skin Lesion Detection Web Application

The application integrated a generated densenet model and pytorch to perform classification on uploaded images to identify what lesions are apparant in the imagee.
It provides basic classification and confidence level for that classification.

# Setup

Create a virtual environment
```bash
python3 -m venv ham10000-web
```

Install requirements
```bash
pip3 install -r requirements.txt
```

Run the application
```bash
./serve
```

> Note that the application locally will run without an ASGI server, so for actual deployment edit the 'serve' file and uncomment the hypercorn command and comment the quart command.

# Screenshots

Here are some sample classifications

# Disclaimer

This application is not designed for commercial purposes, and no gurantees can be made on the validity of the classifications generated. Always refer to trained professionals before medicating yourself.
