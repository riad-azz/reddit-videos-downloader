# Other modules
import os
from dotenv import load_dotenv
from argparse import ArgumentParser

# App modules
from app import create_app

# Load environment variables from .env file
load_dotenv()


if __name__ == "__main__":
    PORT = os.getenv("PORT", 5000)

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=PORT, type=int, help="port to listen on"
    )
    parser.add_argument(
        "-d", "--debug", default=False, type=bool, help="Set debug mode (True/False)"
    )
    args = parser.parse_args()
    debug = args.debug
    port = args.port

    app = create_app(debug=debug)
    app.run(host="0.0.0.0", port=port)
