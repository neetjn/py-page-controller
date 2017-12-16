from pyscc import Component, Controller, component_element, component_elements
from selenium import webdriver
from unittest import TestCase
from time import time


class HomePage(Component):

    @component_element
    def logo(self):
        return 'header-partial h1.logo'

    @component_element
    def task(self):
        return 'todo-task#task-{id}'

    @component_elements
    def tasks(self):
        return 'todo-task'

    @component_elements
    def task_assignees(self):
        return 'todo-task #assignee'

    @component_element
    def delete_tasks_button(self):
        return '#deleteTasks'

    @component_element
    def create_task_assignee(self):
        return '#taskAssignee'

    @component_element
    def create_task_title(self):
        return '#taskTitle'

    @component_element
    def create_task_content(self):
        return '#taskContent'


class AppController(Controller):

    def __init__(self, browser, base_url, **env):
        super(AppController, self).__init__(browser, base_url, {
            'home': HomePage}, **env)

    def go_home(self):
        self.components.home.logo.click()

    def delete_tasks(self, tasks):
        assert isinstance(tasks, (tuple, list)), 'Expected a tuple or list of tasks'
        home = self.components.home
        if isinstance(tasks, (tuple, list)):
            home.tasks.wait_for(
                timeout=5, error='No available tasks to delete')
            for task in tasks:
                if 'disabled' not in home.task.fmt(id=task).get_attribute('class'):
                    home.task.fmt(id=task).click()
        elif isinstance(tasks, int):
            task_el = home.task.fmt(id=tasks)
            if 'disabled' not in task_el.wait_for(timeout=5, error=True).get_attribute('class'):
                task_el.click()
        else:
            raise RuntimeError('Expected a task or list of tasks')
        home.delete_tasks_button.click()

    def create_tasks(self, assignee, title, content):
        home = self.components.home
        home.create_task_assignee.wait_visible(5)
        home.create_task_assignee.get().send_keys(assignee)
        home.create_task_title.get().send_keys(title)
        home.create_task_content.get().send_keys(content)


class BaseTest(TestCase):

    def setUp(self):
        self.app_url = 'http://localhost:3000'
        self.created = time()
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        self.app = AppController(
            webdriver.Chrome(chrome_options=chrome_options), self.app_url, created=self.created)

    def tearDown(self):
        self.app.exit()
