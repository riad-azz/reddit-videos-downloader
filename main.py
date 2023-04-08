from app import create_app

if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "-p", "--port", default=5000, type=int, help="port to listen on"
    )
    parser.add_argument(
        "-d", "--debug", default=False, type=bool, help="Set debug mode (True/False)"
    )
    args = parser.parse_args()
    debug = args.debug
    port = args.port

    app = create_app(debug=debug)
    app.run(host="0.0.0.0", port=port)
