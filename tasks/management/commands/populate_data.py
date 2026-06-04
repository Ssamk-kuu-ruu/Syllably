from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from tasks.models import Priority, Category, Task, SubTask, Note


class Command(BaseCommand):
    help = 'Populate Priority, Category, Task, SubTask, Note with fake data'

    def add_arguments(self, parser):
        parser.add_argument('--tasks', type=int, default=20, help='Number of tasks to create')
        parser.add_argument('--subtasks', type=int, default=2, help='Average number of subtasks per task')
        parser.add_argument('--notes', type=int, default=2, help='Average number of notes per task')

    def handle(self, *args, **options):
        fake = Faker()
        tasks_count = options['tasks']
        subtasks_count = options['subtasks']
        notes_count = options['notes']

        priorities = ['High', 'Medium', 'Low', 'Critical']
        categories = ['Work', 'School', 'Personal', 'Finance', 'Projects']

        for name in priorities:
            Priority.objects.get_or_create(name=name)

        for name in categories:
            Category.objects.get_or_create(name=name)

        priorities_objs = list(Priority.objects.all())
        categories_objs = list(Category.objects.all())

        statuses = ['Pending', 'In Progress', 'Completed']

        created_tasks = []

        for _ in range(tasks_count):
            title = fake.sentence(nb_words=5)
            description = fake.paragraph(nb_sentences=3)
            deadline_dt = timezone.make_aware(fake.date_time_this_month(before_now=False, after_now=True))
            status = fake.random_element(elements=statuses)
            category = fake.random_element(elements=categories_objs)
            priority = fake.random_element(elements=priorities_objs)

            task = Task.objects.create(
                title=title,
                description=description,
                deadline=deadline_dt,
                status=status,
                category=category,
                priority=priority,
            )
            created_tasks.append(task)

            for i in range(fake.random_int(min=1, max=subtasks_count)):
                SubTask.objects.create(
                    parent_task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=statuses),
                )

            for i in range(fake.random_int(min=1, max=notes_count)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

        self.stdout.write(self.style.SUCCESS(f'Created {len(created_tasks)} task records.'))
        self.stdout.write(self.style.SUCCESS('Priorities and categories are populated.'))
        self.stdout.write(self.style.SUCCESS('Subtasks and notes added.'))
