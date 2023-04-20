import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from promptbook.models import Profile, Category, Prompt, Label, PromptLabel

class Command(BaseCommand):
    help = "Populate database with sample data."

    def handle(self, *args, **options):

        PromptLabel.objects.all().delete()
        Label.objects.all().delete()
        Prompt.objects.all().delete()
        Category.objects.all().delete()
        User.objects.all().delete()
        # Create a superuser
        User.objects.create_superuser(username='admin', password='admin', email='admin@example.com')

        # Create sample users
        user_list = []
        for i in range(5):
            user = User.objects.create_user(f'user{i + 1}', f'user{i + 1}@example.com', f'password{i + 1}')
            user_list.append(user)

        # Create sample categories
        category_list = []
        for i in range(3):
            category = Category(name=f'Category {i + 1}', help_text=f'Category {i + 1} help text')
            category.save()
            category_list.append(category)

        # Create sample prompts
        prompt_list = []
        for i, user in enumerate(user_list):
            for j, category in enumerate(category_list):
                prompt = Prompt(
                    text=f'Sample prompt {i + 1}-{j + 1}',
                    category=category,
                    owner=user,
                    is_public=bool(random.getrandbits(1)),
                )
                prompt.save()
                prompt_list.append(prompt)

        # Create sample labels
        label_list = []
        for i in range(4):
            label = Label(name=f'Label {i + 1}')
            label.save()
            label_list.append(label)

        # Create sample prompt labels
        for prompt in prompt_list:
            selected_labels = random.sample(label_list, random.randint(1, len(label_list)))
            for label in selected_labels:
                prompt_label = PromptLabel(label=label, prompt=prompt)
                prompt_label.save()

        self.stdout.write(self.style.SUCCESS("Database successfully populated with sample data!"))
