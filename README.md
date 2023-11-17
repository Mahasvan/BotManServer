# BotManServer

## Server component for [BotManClient](https://github.com/Mahas1/BotManClient)

### Installation

- Clone the repository
- Install requirements
    - ```shell
      pip3 install -r requirements.txt
      ```
- Fill in `config.json` with appropriate data
- Install [Tesseract OCR](https://tesseract-ocr.github.io/tessdoc/#binaries)
    - Instructions are in the **Binaries** section

### Running the App

- ```shell
  python3 app.py
  ```

### Config Structure

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

### Config entries

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