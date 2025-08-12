# Sorting code

This code helps a user sort packages with a function called "sort" which returns a string with 1 of 3 different values "STANDARD", "SPECIAL", "REJECTED".

The function receives 4 arguments width, height, length and mass.

## Installation

```bash
docker-compose build
docker-compose up -d
```

## Usage

Start a console with access to the docker image with this command:
```bash
docker-compose exec app bash
```

Run the tests with the following command
```bash
pytest
```

Start up the app:
```
python src/main.py
```


