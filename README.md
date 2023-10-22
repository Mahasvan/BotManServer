# BotManServer

## Server component for [BotManClient](https://github.com/Mahas1/BotManClient)

### Installation
- Clone the repository
  - Install requirements 
    - ```shell
      pip3 install -r requirements.txt
      ```
- Fill in `config.json` with appropriate data
- Run the app
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
  "logfile": "log.txt"
}
```

### Config entries
- `currency-api-key`
  - Free API Key from [CurrencyConverterAPI](https://www.currencyconverterapi.com)
- `spotify-client-id`
- `spotify-client-secret`
  - Spotify Client ID and Secret from [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
  - Create a new app, go to its settings, and copy the Client ID and Client Secret