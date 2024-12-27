import json
import os
import statistics
from pathlib import Path

import flask
from flask import render_template, request

app = flask.Flask(__name__)
app.debug = True


def extract_score(row):
    return row["security_advisory"]["cvss"]["score"]


def load_reports():
    for filename in os.listdir("reports"):
        report = {"filename": Path(filename).stem}

        with open(f"reports/{filename}", "r", encoding="utf-8") as file_handle:
            raw_data = json.load(file_handle)

        report["findings"] = sorted(
            [row for row in raw_data if row["state"] == "open"], key=extract_score, reverse=True
        )

        scores = [extract_score(r) for r in report["findings"]]
        if scores:
            report.update(
                {
                    "total_score": sum(scores),
                    "max_score": max(scores),
                    "median_score": statistics.median(scores),
                }
            )
        else:
            report.update(
                {
                    "total_score": 0,
                    "max_score": 0,
                    "median_score": 0,
                }
            )

        yield report


@app.route("/", methods=["GET"])
def home():
    reports = sorted(load_reports(), key=lambda x: -x["total_score"])
    return render_template("index.html", reports=reports)
