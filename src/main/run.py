import signal
import subprocess
import sys
import threading
import time
import webbrowser
from concurrent.futures import ThreadPoolExecutor


def start_api():
    """Start the FastAPI backend server."""
    try:
        print("Starting API server on http://localhost:8000")
        subprocess.run(["python", "-m", "src.main.app"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting API server: {e}")
        return False
    except KeyboardInterrupt:
        print("API server stopped")
    return True


def start_interface():
    """Start the Streamlit interface."""
    try:
        print("Starting Streamlit interface on http://localhost:8501")
        subprocess.run(["streamlit", "run", "src/main/interface.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error starting Streamlit interface: {e}")
        return False
    except KeyboardInterrupt:
        print("Streamlit interface stopped")
    return True


def open_browser():
    """Open the web browser after a delay."""
    try:
        print("Waiting for services to start...")
        time.sleep(5)  # Wait longer to ensure services are ready
        print("Opening browser...")
        webbrowser.open("http://localhost:8501")  # Streamlit default port
    except Exception as e:
        print(f"Error opening browser: {e}")


def signal_handler(sig, frame):
    """Handle shutdown signals gracefully."""
    print("\nShutting down Crypto Analytics platform...")
    sys.exit(0)


def main():
    """Main function to run the Crypto Analytics platform."""
    # Register signal handlers for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    print("Starting Crypto Analytics platform...")
    print("Press Ctrl+C to stop all services")

    with ThreadPoolExecutor(max_workers=2) as executor:
        # Start FastAPI in a thread
        api_future = executor.submit(start_api)

        # Open browser in a separate thread
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()

        # Start Streamlit in the main thread pool
        interface_future = executor.submit(start_interface)

        # Wait for both services to complete (which normally shouldn't happen unless they crash)
        for future in [api_future, interface_future]:
            try:
                future.result()
            except Exception as e:
                print(f"Service error: {e}")

        print("All services stopped")


if __name__ == "__main__":
    main()
