# BotManServer

## Server component for [BotManClient](https://github.com/Mahas1/BotManClient)

## Installation

- Clone the repository
- Install requirements
    - ```shell
      pip3 install -r requirements.txt
      ```
- Fill in `config.json` with appropriate data

## Running the App

### Running Locally
- Make sure the config entries are filled correctly.
- Make sure Docker Desktop is installed and running
- Install [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/#binaries)
    - Instructions are in the **Binaries** section
- ```shell
  python3 app.py
  ```

### Running with Docker
- Make sure the config entries are filled correctly.
- Build the Docker image
    - ```shell
      docker build -t botman-server .
      ```
- Run the Docker container
- ```shell
  docker run -p 8000:{PORT} botman-server # PORT is the port specified in the config file
  ```


## Config Structure

```json
{
  "host": "0.0.0.0",
  "port": 8000,
  "currency-api-key": "Your API Key",
  "spotify-client-id": "Spotify Client ID",
  "spotify-client-secret": "Spotify Client Secret",
  "tesseract_exec_path": "tesseract",
  "tesseract_tessdata_path": "/usr/local/Cellar/tesseract-lang/4.1.0/share/tessdata",
  "logfile": "log.db"
}
```

## Config entries

- `currency-api-key`
    - Free API Key from [CurrencyConverterAPI](https://www.currencyconverterapi.com).
- `spotify-client-id` & `spotify-client-secret`
    - Spotify Client ID and Secret from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard).
    - Create a new app, go to its settings, and copy the Client ID and Client Secret.
- `tesseract_exec_path`
    - Path to the `tesseract` executable. If installed properly, should be `tesseract.exe` for Windows and `tesseract`
      for Linux and macOS.
    - If installed in a custom path, or you knew what you were doing, change the path to the installation's path
      accordingly.
- `tesseract_tessdata_path`
    - Path to the `tessdata` folder. This is for additional languages support. Not mandatory.

## Additional Documentation
### Running behind a proxy (Nginx)
- Sometimes, you may need to run the app behind a proxy, like I had to with Kubernetes and the Nginx Ingress Controller.
- if the app is served with an additional path prefix, say `/api/v1`, FastAPI freaks out.
- So to fix this, we need to set the prefix manually.
- Set the `FASTAPI_ROOT_PATH` environment variable to your path prefix 
- Check [this page](https://fastapi.tiangolo.com/advanced/behind-a-proxy/) for more information.

### Kubernetes Instructions
- Build the container using
  - ```shell
    sudo docker build -t mahasvan/botmanserver:latest .
    ```
- Install the Nginx Ingress Controller - [Install Guide](https://docs.nginx.com/nginx-ingress-controller/installation/installing-nic/installation-with-helm/)
- Add the BotMan Server Docker image to the cluster registry
  - If using K3S, refer to [this answer](https://stackoverflow.com/a/72928176) on StackOverflow
- Go through the YAML files in the `k8s` directory, and change the details needed.
- Apply the Kubernetes manifests
  - ```shell
    kubectl apply -f k8s/
    ```
- You should now have the deployment in effect.