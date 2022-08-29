#!/usr/bin/env python3
import click
from todoist_api_python.api import TodoistAPI

from todo import *
from api_token import api_token

api = TodoistAPI(api_token)

randomizer = TaskRandomizer(api)


@click.group()
def cli():
    pass


@click.command("list")
@click.option("--projects", "-p", is_flag=True, help="Show all projects")
@click.option("--sections", "-s", is_flag=True, help="Show all sections")
def todo_list(projects, sections):
    if projects:
        _projects = randomizer.get_all_projects()
        for project in _projects:
            click.echo(project.name)
    elif sections:
        _sections = randomizer.get_all_sections()
        for section in _sections:
            click.echo(section.name)


@click.command("random")
@click.option("--project", "-p", help="Random project task")
@click.option("--section", "-s", help="Random section task")
@click.option("--today", "-T", is_flag=True, help="Random today task")
@click.option("--overdue", "-o", is_flag=True, help="Random overdue+today task")
@click.option("--only-overdue", "-O", is_flag=True, help="Random overdue task")
@click.option("--priority", "-P", is_flag=True, help="Random Top priority task")
def random_task(project: str, section: str, today: bool, overdue: bool, only_overdue: bool, priority: bool):
    if project:
        click.echo(randomizer.get_random_task_by_project_name(project))
    elif section:
        click.echo(randomizer.get_random_task_by_section(section))
    elif today:
        click.echo(randomizer.get_random_filtered_tasks("today"))
    elif overdue:
        click.echo(randomizer.get_random_filtered_tasks("(overdue | today)"))
    elif only_overdue:
        click.echo(randomizer.get_random_filtered_tasks("overdue"))
    elif priority:
        click.echo(randomizer.get_random_top_priority_task())
    else:
        click.echo(randomizer.get_random_task())


@click.command("tasks")
@click.option("--today", "-T", is_flag=True, help="Get only today tasks")
@click.option("--overdue", "-o", is_flag=True, help="Get today and overdue tasks")
@click.option("--only-overdue", "-O", is_flag=True, help="Get only overdue tasks")
@click.option("--priority", "-p", is_flag=True, help="Get Top priority tasks")
def tasks(today: bool, overdue: bool, only_overdue: bool, priority: bool):
    if today:
        click.echo(randomizer.get_filtered_tasks("today"))
    elif overdue:
        click.echo(randomizer.get_filtered_tasks("(overdue | today)"))
    elif only_overdue:
        click.echo(randomizer.get_filtered_tasks("overdue"))
    elif priority:
        click.echo(randomizer.get_top_priority_tasks())
    else:
        click.echo(randomizer.get_filtered_tasks(""))

@click.command("cherry")
@click.option("--priority", "-p", is_flag=True, help="Get top priority and max outdated")
@click.option("--earliest", "-e", is_flag=True, help="Get the earliest date")
def cherry(priority: bool, earliest: bool):
    if priority:
        click.echo(randomizer.get_cherry_prioriy_task())
    elif earliest:
        click.echo(randomizer.get_cherry_earliest_task())

cli.add_command(random_task)
cli.add_command(todo_list)
cli.add_command(tasks)
cli.add_command(cherry)

if __name__ == '__main__':
    cli()
