# LLM automatic lawnmower schedule

This project demonstrates how to simply control an automower schedule with an LLM.
I've made it for my own use case but you can easily adapt it to your needs.
The reason is to see how well the ChatGPT can control a low risk parameter
of an actual device to observer & learn. It's simple, glues 2 libraries together:

- [Langchain](https://www.langchain.com/)
- [aioautomower](https://github.com/Thomas55555/aioautomower/)

The app works in the following way:

1. Get the weather forecast from ChatGPT for specified location
2. Feed the forecast to a prompt and ask ChatGPT to generate a schedule
3. Send the schedule to Husqvarna Automower Connect API
4. Profit! ;)

Preferable you want to run it once or twice a day to get the most accurate forecast.
In my case, haaving the simplest Automower Aspire R4 I'm not getting into
weekday scheduling and instead just setting schedule the same way for every
day - especially that 7-day forecast is not very accurate.

## Getting started

To install dependencies run:

```sh
PIPENV_VENV_IN_PROJECT=1 pipenv install --dev
pipenv shell
```

## Usage

Place API keys into .env file looking like the one below:

```none
LAT="52.237049"
LON="21.017532"
OPENAI_API_KEY="sk-"
AUTOMOWER_API_KEY="..."
AUTOMOWER_API_SECRET="..."
```

Open the project in vscode and execute it.
If you want to run it periodically then add it to cron.

## Building binary

```sh
pyinstaller --noconfirm llm_ls.spec
```

### OpenAI

1. To obtain OpenAI API key go to <https://platform.openai.com/api-keys> and create one.
  A key starts with `sk-...`.
2. Place it into .env

### Husqvarna Automower Connect API

To obtain Husqvarana API key:

1. Go to <https://developer.husqvarnagroup.cloud/> aand sign in
2. Go to [My Applications](https://developer.husqvarnagroup.cloud/applications) and create a new one. Set the name to anything you want and leave the rest empty.
3. You will receive application key and secret. Copy them to .env and press the "Connect new API" button below
4. Select "Automower Connect API" and press "Connect"
5. Afterwards you will receive a `curl` command to test your credentials - you can use it to test if your credentials are correct.
