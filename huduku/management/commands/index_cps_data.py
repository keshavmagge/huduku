import logging

from django.core.management.base import BaseCommand
from huduku import index

log = logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Indexes cps product records in solr"

    def handle(self, **options):
        index.build_index()
