import csv
from flask import Flask, render_template, request

DATA_FILE = 'data.csv'
FIELDNAMES = ['id', 'player', 'pass_yds', 'att', 'cmp', 'cmp_percent', 'td', 'intx']

app = Flask(__name__)

stats = []

def load_data():
    """Function which loads csv file for use in program"""
    with open(DATA_FILE, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            stats.append(row)

def append_stats(new_row):
    with open(DATA_FILE, 'a', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, FIELDNAMES)
        writer.writerow(new_row)

@app.route('/stats')
def qb_stats_index():
    return render_template('index.html', stats=stats)

@app.route('/stats/<stat_id>')
def qb_stat_show(stat_id):
    """Show stats on webpage"""
    for stat in stats:
        if stat['id'] == stat_id:
            return render_template('show.html', stat=stat)
    return 'Not Found', 404

@app.route('/stats', methods=['POST'])
def qb_stats_create():
    new_stat = request.get_json()
    new_stat['id'] = str(len(stats) + 1)
    stats.append(new_stat)
    append_stats(new_stat)
    return { 'message': 'Stats created successfully' }, 201

@app.route('/stats/<stat_id>', methods=['PATCH'])
def qb_stats_update(stat_id):
    updated_qb_stat = request.get_json()
    for stat in stats:
        if stat['id'] == stat_id:
            stat.update(updated_qb_stat)
            return { 'message': 'QB Stats updated successfully' }, 201

    return 'Not Found', 404

@app.route('/stats/<stat_id>', methods=['DELETE'])
def qb_stats_delete(stat_id):
    i = None
    for j in range(len(stats)):
        if stats[j]['id'] == stat_id:
            i = j
            break
    if i is not None:
        stats.pop(i)
        
    return { 'message': 'QB Stats deleted successfully' }, 201

load_data()
app.run()
