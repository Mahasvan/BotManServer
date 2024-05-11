import requests

HOST = "localhost"
PORT = 8000

if __name__ == "__main__":
    try:
        response = requests.get(f"http://{HOST}:{PORT}/ping/")
        if response.status_code == 200:
            print("Server is running!")
            exit()
        else:
            print("Server is not running!")
            exit(1)
    except requests.exceptions.ConnectionError:
        print("Server is not running!")
        exit(1)
