from django.core.management.base import BaseCommand
from news.models import Post, Category

class Command(BaseCommand):
    help = 'Удаляет все новости из указанной категории с подтверждением'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        category_name = options['category']
        answer = input(f'Вы правда хотите удалить все статьи в категории "{category_name}"? (yes/no): ')

        if answer.lower() != 'yes':
            self.stdout.write(self.style.ERROR('Отменено'))
            return

        try:
            category = Category.objects.get(name=category_name)
            Post.objects.filter(categories=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Succesfully deleted all news from category "{category.name}"'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Could not find category  "{category_name}"'))