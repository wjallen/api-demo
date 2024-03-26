import json
from flask import Flask, request
from jobs import add_job, get_job_by_id

app = Flask(__name__)

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
        return """
  To submit a job, do the following:
  curl localhost:5000/jobs -X POST -d '{"start":1, "end":2}' -H "Content-Type: application/json"

"""

@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid):
    """
    API route for checking on the status of a submitted job
    """
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

