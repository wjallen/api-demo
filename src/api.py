#!/usr/bin/env python3
import json
from flask import Flask, request, send_file
from jobs import add_job, get_job_by_id, jdb, results

app = Flask(__name__)

@app.route('/help', methods=['GET'])
def help():
        return """
  To submit a job, do the following:
  curl localhost:5000/jobs -X POST -d '{"start":1, "end":2}' -H "Content-Type: application/json"

"""

@app.route('/hello', methods=['GET'])
def hello():
    return {'result': 'hello'}

@app.route('/jobs', methods=['POST', 'GET'])
def jobs_api():
    """
    API route for creating a new job to do some analysis. This route accepts a JSON payload
    describing the job to be created.
    """
    if request.method == 'POST':
        try:
            job = request.get_json(force=True)
        except Exception as e:
            return json.dumps({'status': "Error", 'message': 'Invalid JSON: {}.'.format(e)})
    
        return json.dumps(add_job(job['start'], job['end']), indent=2) + '\n'

    elif request.method == 'GET':
        return json.dumps([item.decode() for item in jdb.keys()], indent=2)

@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid):
    """
    API route for checking on the status of a submitted job
    """
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'


@app.route('/results-img/<job_uuid>', methods=['GET'])
def get_result_image(job_uuid):
    path=f'/app/{job_uuid}.png'
    with open(path, 'wb') as f:
        f.write( results.hget(job_uuid, 'image') )
    return send_file(path, mimetype='image/png', as_attachment=True)

@app.route('/results-dat/<job_uuid>', methods=['GET'])
def get_result_data(job_uuid):
    return results.hget(job_uuid, 'data')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

