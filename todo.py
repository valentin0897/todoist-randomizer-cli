from todoist_api_python.api import TodoistAPI
from random import randrange
import datetime as dt


class TaskRandomizer:
    def __init__(self, api: TodoistAPI):
        self.api = api

    def get_all_projects(self):
        return self.api.get_projects()

    def get_all_sections(self):
        return self.api.get_sections()

    def get_random_task_by_project_name(self, project_name: str, is_nested: bool = False):
        projects = self.get_all_projects()
        try:
            project = list(filter(lambda _project: _project.name == project_name, projects))[0]
        except KeyError:
            return f"Project with name {project_name} not found"

        tasks = self.api.get_tasks(project_id=project.id)
        if not is_nested:
            TaskRandomizer._parse_not_nested_tasks(tasks)
        rand_task = TaskRandomizer._get_random_task(tasks)

        return self._get_str_from_task(rand_task)

    def get_random_task_by_section(self, section_name: str, is_nested: bool = False):
        sections = self.get_all_sections()
        try:
            section = list(filter(lambda _section: _section.name == section_name, sections))[0]
        except KeyError:
            return f"Sections with name {section_name} not found"

        tasks = self.api.get_tasks(section_id=section.id)
        if not is_nested:
            tasks = TaskRandomizer._parse_not_nested_tasks(tasks)
        rand_task = TaskRandomizer._get_random_task(tasks)

        return self._get_str_from_task(rand_task)

    def get_random_task(self, is_nested: bool = False):
        tasks = self.api.get_tasks()
        if not is_nested:
            tasks = TaskRandomizer._parse_not_nested_tasks(tasks)
        rand_task = TaskRandomizer._get_random_task(tasks)

        return self._get_str_from_task(rand_task)

    def get_filtered_tasks(self, _filter: str):
        tasks = self.api.get_tasks(filter=_filter)
        return ''.join([f"{task.content}\n" for task in tasks]).strip()

    def get_top_priority_tasks(self):
        tasks = self.api.get_tasks()
        top_priority = self._get_top_priority(tasks)
        return self.get_filtered_tasks(f"p{str(top_priority)}")

    def get_random_top_priority_task(self):
        tasks = self.api.get_tasks()
        top_priority = self._get_top_priority(tasks)
        return self.get_random_filtered_tasks(f"(overdue | today) & p{str(top_priority)}")
            

    def get_random_filtered_tasks(self, _filter: str, is_nested: bool = False):
        tasks = self.api.get_tasks(filter=_filter)
        if not is_nested:
            tasks = TaskRandomizer._parse_not_nested_tasks(tasks)
        rand_task = TaskRandomizer._get_random_task(tasks)

        if tasks:
            return self._get_str_from_task(rand_task)
        else:
            return "There is no tasks with this filter"

    def get_cherry_prioriy_task(self):
        tasks = self.api.get_tasks()
        top_priority = self._get_top_priority(tasks)
        prioritized_tasks = self.api.get_tasks(filter=f"p{str(top_priority)}")
        min_date_task = prioritized_tasks[0]
        for task in prioritized_tasks:
            task_date = dt.datetime.strptime(task.due.date, "%Y-%m-%d")
            min_date = dt.datetime.strptime(min_date_task.due.date, "%Y-%m-%d")
            if min_date > task_date:
                min_date_task = task
        return self._get_str_from_task(min_date_task)

    def get_cherry_earliest_task(self):
        tasks = self.api.get_tasks()
        min_date_task = tasks[0]
        print(min_date_task)
        for task in tasks:
            if task.to_dict().get("due", False):
                task_date = dt.datetime.strptime(task.due.date, "%Y-%m-%d")
                min_date = dt.datetime.strptime(min_date_task.due.date, "%Y-%m-%d")
                if min_date > task_date:
                    min_date_task = task
        return self._get_str_from_task(min_date_task)

    def _get_str_from_task(self, task):
        project = self.api.get_project(task.project_id)
        if task.section_id != 0:
            section = self.api.get_section(task.section_id)
            section_name = section.name
        else:
            section_name = "INBOX"

        return f"  Project: {project.name}\n  Section: {section_name}\n  Task: {task.content}"

    @staticmethod
    def _get_random_task(tasks):
        if tasks:
            return tasks[randrange(len(tasks))]

    @staticmethod
    def _parse_not_nested_tasks(tasks):
        return list(filter(lambda task: task.parent_id is None, tasks))

    @staticmethod
    def _get_top_priority(tasks):
        return min(tasks, key = lambda task: task.priority).priority


class PomodoroTimer:
    def __init__(self, work, rest) -> None:
        self.work = work
        self.rest = rest
    
    def start(self):
        now = dt.datetime.now()
        target = dt.datetime.combine(dt.date.today(), dt.time())

    

    