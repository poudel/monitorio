# Notes

Solution to https://gist.github.com/Chompas/0208b85feab1f51292865f8088df2e4a

Developed using Python 3.8 on Linux.

I'm afraid I may have overengineered this app. Because of that, I
didn't have enough time to write tests.

## Testability

Having said that, the code, is organized/splitted in a way to make it
easily testable. 

Some methods in the `App` class can be tricky to test (e.g `report`)
but it is possible to test log outputs using `assertLogs` or similar
assertion functions.

The `Storage` class and/or it's methods can be mocked to facilitate
testing. Same goes for the `Config` class.

# Running

Go to the project root and run the following commands. Change the
values of the env vars if you need to.

Create a virtualenv and install `twisted` or do `pip install -r
requirements.txt`.

## The HTTP service

It's the same service as mentioned in the coding challenge. I did
change it a little bit to test timeout.

```
python src/server.py
```

## Service monitor

```shell
PYTHONPATH=. MON_SQLITE_DB_PATH=db.sqlite3 python src/cli.py monitor
```

By default the service is checked every 6 seconds but it's possible to
change the frequency using `MON_FREQUENCY_SECONDS`.

## Reporter

Simple reporter that displays the recorded last 10 minutes (or less if
there isn't enough data).

```shell
PYTHONPATH=. MON_SQLITE_DB_PATH=db.sqlite3 python src/cli.py report
```

To change the number of minutes reported, pass
`MON_REPORT_WAY_BACK_MINUTES` (I know, naming is difficult).


## `Config` class

The `Config` class has defaults for most of the parameters specified
there. Env variables should be prefixed by `MON_` to be picked by the
`from_environment` classmethod; namespacing just in case.
