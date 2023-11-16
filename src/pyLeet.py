#!/usr/bin/env python3
from click.types import IntParamType
import requests
import time
import json
import click
import subprocess
from pathlib import Path

from conf import graphql


def getQueryQuestionContent(titleSlug):
    questionQuery = """query questionContent($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        content
        titleSlug
      }
    }"""
    variables = {"titleSlug": titleSlug}
    return {"query": questionQuery, "variables": variables}


def getFirst10Problems(limit):
    variables = {"categorySlug": "", "skip": 0, "limit": limit, "filters": {}}
    return {"query": graphql.problemSetQuery, "variables": variables}


@click.command()
@click.argument("limit", type=int, required=1)
def getQuestionList(limit):
    response = requests.post(
        graphql.leetCodeUrl,
        json=getFirst10Problems(limit),
        cookies=graphql.cookies,
        headers=graphql.headers,
    )
    python_object = json.loads(response.text)
    for question in python_object["data"]["problemsetQuestionList"]["questions"]:
        click.echo(question["title"])


@click.command()
@click.argument("titleslug", type=str, required=1)
def getQuestion(titleslug):
    response = requests.post(
        graphql.leetCodeUrl,
        json=getQueryQuestionContent(titleslug),
        cookies=graphql.cookies,
        headers=graphql.headers,
    )
    python_object = json.loads(response.text)
    subprocess.run(
        ["w3m", "-dump", "-T", "text/html"],
        input=python_object["data"]["question"]["content"].encode(),
        check=True,
    )


@click.command()
@click.argument(
    "filepath",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, path_type=Path),
)
def runFile(filepath):
    with open(filepath, "r") as file:
        file_content = file.read()

    response = requests.post(
        "https://leetcode.com/problems/two-sum/submit/",
        json={"lang": "python3", "question_id": "1", "typed_code": file_content},
        cookies=graphql.cookies,
        headers=graphql.headersSubmit,
    )
    python_object = json.loads(response.text)
    submissionId = python_object["submission_id"]
    status = "PENDING"

    while status == "PENDING":
        response = requests.get(
            f"https://leetcode.com/submissions/detail/{submissionId}/check/",
            cookies=graphql.cookies,
            headers=graphql.headersSubmit,
        )
        status = json.loads(response.text)["state"]
        if status != "PENDING":
            subprocess.run(
                ["w3m", "-dump", "-T", "text/html"],
                input=response.text.encode(),
                check=True,
            )
        else:
            time.sleep(5)


@click.group()
def cli():
    """A Click Program to fetch LeetCode problems"""
    pass


cli.add_command(getQuestion)
cli.add_command(getQuestionList)
cli.add_command(runFile)


if __name__ == "__main__":
    cli()
