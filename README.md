# Pickup Soccer Game Balanced Teams Sorter

Python project that generates balanced teams for pickup soccer games.

The python script expects a csv as input (example in the repo), with Player name, Rating and a boolean column indicating if said player is participating in the pickup game for which you want to sort the teams.

Currently it is suited to work for a scenario with 4 teams of 5 people, but you can change the code to adapt to your needs with little changes needed.

## Features

- Generate balanced teams based on player ratings.
- Supports manual input and CSV file upload.
- Flask web interface for easy interaction.
- Command-line interface (CLI) for quick usage.

## Requirements

- Python 3.x
- Flask
- Pandas

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/pickup-soccer-game-balanced-teams-sorter.git
    cd pickup-soccer-game-balanced-teams-sorter
    ```

2. Install the required packages:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

### Command-Line Interface (CLI)

To generate teams using the CLI, run the following command example:
```sh
python cli.py PlayersRatings.csv --teams 4
````
* `path/to/file.csv`: Path to the CSV file containing player data.
* `--teams 4`: Number of teams to generate (default is 4).

### Web Interface

* Start the Flask web server:  
    ```sh
    python app.py
    ```
* Open your web browser and go to http://127.0.0.1:5000.  
* Use the web interface to either manually input player data or upload a CSV file.

### CSV File Format

The CSV file should have the following columns:

| **Coluna**   | **Descrição**                                           | **Exemplo**          |
|--------------|---------------------------------------------------------|----------------------|
| `player`     | Nome do jogador.                                         | `"John Doe"`         |
| `rating`     | Avaliação do jogador, pode ser um valor decimal (0 a 5). | `3.5`                |
| `is_going`   | Booleano indicando se o jogador está participando.       | `1` para sim, `0` para não |

Example file: [PlayersRatings.csv](https://github.com/artcurty/pickup-soccer-game-balanced-teams-sorter/blob/main/pickup_soccer_team_sorter.py)

### Project Structure

* `app.py`: Flask web server.
* `cli.py`: Command-line interface for generating teams.
* `service.py`: Contains the TeamGeneratorService class with the core logic.
* `templates/index.html`: HTML template for the web interface.
* `static/js/scripts.js`: JavaScript for handling form submissions and displaying results.
* `static/css/styles.css`: CSS for styling the web interface.
