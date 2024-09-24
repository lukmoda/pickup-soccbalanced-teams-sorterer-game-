from flask import Flask, render_template, request, jsonify
from service import TeamGeneratorService

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/generate_teams', methods=['POST'])
def generate_teams():
    data = request.json
    players = data.get('players', [])
    team_count = int(data.get('teamCount', 1))

    teams = TeamGeneratorService.load_players_from_list(players, team_count)
    return jsonify(teams)


@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    file = request.files['csvFile']
    team_count = int(request.form.get('teamCount', 1))

    file_content = file.read()
    teams = TeamGeneratorService.process_uploaded_csv(file_content, team_count)
    return jsonify(teams)


if __name__ == '__main__':
    app.run(debug=True)
