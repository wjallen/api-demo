import json
from flask import Flask, request
from jobs import rd, q, add_job, get_job_by_id

app = Flask(__name__)


@app.route('/', methods=['GET'])
def info():
    """
    Informational
    """

    return """
  Try the following routes:

  /                GET    informational
  /data            GET    read data in database
  /data            POST   upload data to database
    
  /jobs            GET    info on how to submit job
  /jobs            POST   submit job
  /jobs/<jobid>    GET    info on job

"""


@app.route('/data', methods=['POST', 'GET'])
def download_data(): 
    """
    API route for adding raw meteorite landing data to the dabase.
    """
    if request.method == 'POST':

        rd.flushdb()

        with open('ML_Data_Sample.json', 'r') as f:
            ml_data = json.load(f)

        for item in ml_data['meteorite_landings']:
            rd.set(item['id'], json.dumps(item))

        return 'Data has been loaded to Redis from file\n'

    elif request.method == 'GET':

        list_of_data = []

        for item in rd.keys():
            list_of_data.append(json.loads(rd.get(item)))

        return (f'{json.dumps(list_of_data, indent=2)}\n')

    else:

        return 'Only supports POST and GET methods\n'



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
  curl localhost:5041/jobs -X POST -d '{"start":1, "end":2}' -H "Content-Type: application/json"

"""

@app.route('/jobs/<job_uuid>', methods=['GET'])
def get_job_result(job_uuid):
    """
    API route for checking on the status of a submitted job
    """
    return json.dumps(get_job_by_id(job_uuid), indent=2) + '\n'


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

