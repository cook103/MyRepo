#!/usr/bin/env python3
import argparse
import routes
import extensions

try:
    import utils
except Exception as e:
    print(f"Failed to import utils, error {e}.")
    sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Stock Analyzer Web App")

    parser.add_argument(
        "-p", "--port",
        type=str,
        help="TCP port to host server on"
    )

    args = parser.parse_args()

    if args.port:
        port = args.port
    else:
        # use defualt port 8080
        port = "8080"

    # kick off thread to grab new data everyday
    utils.start_cache_reset_thread()

    with extensions.app.app_context():
        extensions.db.create_all()

    # kick off thread for processing database entries
    extensions.process_runs_into_database()

    extensions.app.run(debug=True, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
