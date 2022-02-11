[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_dapla-start-api&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=statisticsnorway_dapla-start-api)

# dapla-start-api

API used by https://start.dapla.ssb.no

## Development

Use `make` for common tasks:

```
local-install                  Installation steps for local development
test                           Run tests
bump-version-patch             Bump patch version, e.g. 0.0.1 -> 0.0.2.
bump-version-minor             Bump minor version, e.g. 0.0.1 -> 0.1.0.
local-build                    Build the app for local development
local-run                      Run the app locally
docker-build                   Build docker image
docker-run                     Run app locally with docker
docker-shell                   Enter shell of locally running docker app
docker-cleanup                 Cleanup locally running docker app
```

Swagger UI for the API can be browsed locally at: http://localhost:8000/docs 

## Logging
This library uses the standard Python logging library with two pre-defined log configurations.
The default configuration will use a colourful, human-readable output which is well suited for running locally.

However, by setting the environment variable `LOG_FORMAT_ECS`, one can switch to the Elastic Common Schema (ECS) format
which is more suitable for log visualization tools like Kibana.
