#!/usr/bin/env python3
import requests
import json
import click
import subprocess

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
    # click.echo_via_pager(python_object["data"]["question"]["content"])
    subprocess.run(
        ["w3m", "-dump", "-T", "text/html"],
        input=python_object["data"]["question"]["content"].encode(),
        check=True,
    )


@click.group()
def cli():
    """A Click Program to fetch LeetCode problems"""
    pass


cli.add_command(getQuestion)
cli.add_command(getQuestionList)


if __name__ == "__main__":
    cli()
