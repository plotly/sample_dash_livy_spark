from constants import JobStates, SparkStates
import json
import requests


def prettify_json(json_dict):
    return json.dumps(json_dict, indent=4, sort_keys=True)


def parse_json(json_text):
    return json.loads(json_text)


job_states = JobStates()
spark_states = SparkStates()


class LivyRequests:
    livy_host = "http://localhost:8998"
    data = {"kind": "pyspark", "executorMemory": "512m"}
    headers = {"Content-Type": "application/json"}

    def list_sessions(self):
        resp = requests.get(self.livy_host + "/sessions", headers=self.headers)
        payload = resp.json()
        return payload["sessions"]

    def kill_sessions(self):
        sessions = self.list_sessions()
        payloads = []
        for session in sessions:
            session_url = self.livy_host + "/sessions/{}".format(session["id"])
            resp = requests.delete(session_url, headers=self.headers)
            payload = resp.json()
            payloads.append(payload)

        if len(payloads) == 0:
            return None
        else:
            return payloads

    def run_session(self):
        resp = requests.post(
            self.livy_host + "/sessions",
            data=json.dumps(self.data),
            headers=self.headers,
        )
        payload = resp.json()
        return {
            "id": payload["id"],
            "state": payload["state"],
            "session-url": self.livy_host + resp.headers["location"],
        }

    def session_info(self, session_url):
        resp = requests.get(session_url, headers=self.headers)
        payload = resp.json()
        return {
            "id": payload["id"],
            "state": payload["state"],
            "session-url": session_url,
        }

    def run_job(self, session_url, job):
        resp = requests.post(
            session_url + "/statements", data=json.dumps(job), headers=self.headers
        )
        payload = resp.json()

        return {
            "id": payload["id"],
            "state": payload["state"],
            "output": payload["output"],
            "statement-url": self.livy_host + resp.headers["location"],
        }

    def job_info(self, statement_url):

        try:
            resp = requests.get(statement_url, headers=self.headers)
            payload = resp.json()

            return {
                "id": payload["id"],
                "state": payload["state"],
                "output": payload["output"],
                "statement-url": statement_url,
            }

        except Exception as e:
            return {"state": job_states.ERROR, "error": str(e)}
