import requests
import json

jobs = []

url = "https://production.api.recruiting-solutions.org/search"

payload = {
    "count": True,
    "facets": [],
    "filter": "addresses/any(address: address/countryCode eq 'DEU') and language eq 'de_DE' and custUnsolicitedApplication ne true and datePosted lt 2026-09-29T17:23:23.964Z",
    "search": "*",
    "skip": 0
}

headers = { 
    "customerid": "vector-prod"
}

def extract_data(job):
    return {
            "job_id": job["jobId"],
            "title": job["title"],
            "link": job["link"],
            "date_posted": job["datePosted"],
            "last_modified": job["lastModifiedDateTime"],
            "company": job["legalEntity"],
            "working_model": job["workingModel"],
            "country": job["country"],
            "city": job["addresses"][0]["city"],
            "entry_level": job["entryLevels"][0]["code"],
            "job_code": job["jobCode"],
            "programmingLanguages": job["programmingLanguages"]
        }

response = requests.post(url, headers=headers, json=payload)

data = response.json()

def give_jobs():
    with open("jobs.json", "w", encoding="utf-8") as f:
        for job in data["value"]:
            jobs.append(extract_data(job))
            f.write(json.dumps(jobs, indent=4, ensure_ascii=False))
            f.write("\n")

    return jobs



        