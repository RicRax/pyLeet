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
        slug = question["titleSlug"]
        print(question["title"], f" (Titleslug:{slug})")


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
@click.argument("slug")
@click.argument("question_id")
def submitFile(filepath, slug, question_id):
    with open(filepath, "r") as file:
        file_content = file.read()

    response = requests.post(
        f"https://leetcode.com/problems/{slug}/submit/",
        json={
            "lang": "python3",
            "question_id": f"{question_id}",
            "typed_code": file_content,
        },
        cookies=graphql.cookies,
        headers=graphql.getHeadersSubmit(slug),
    )
    python_object = json.loads(response.text)
    submissionId = python_object["submission_id"]
    status = "PENDING"
    print("Processing request...")

    while status == "PENDING":
        response = requests.get(
            f"https://leetcode.com/submissions/detail/{submissionId}/check/",
            cookies=graphql.cookies,
            headers=graphql.getHeadersSubmit(slug),
        )
        print(response.text)
        status = json.loads(response.text)["state"]
        if status != "PENDING":
            print(json.loads(response.text)["status_msg"])
        else:
            time.sleep(5)


@click.group()
def cli():
    """A Click Program to fetch LeetCode problems"""
    pass


cli.add_command(getQuestion)
cli.add_command(getQuestionList)
cli.add_command(submitFile)


if __name__ == "__main__":
    cli()
