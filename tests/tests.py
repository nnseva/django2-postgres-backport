"""
Test backport
"""
import io
import json
import sys

from django.conf import settings
from django.core.management import call_command
from django.test import Client, TransactionTestCase


class Test(TransactionTestCase):
    """
    Test backport
    """

    def test_001_proper_sql_generated(self):
        """Test migrations generate proper SQL"""
        out = io.StringIO()
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = out
        sys.stderr = out
        try:
            call_command('sqlmigrate', 'tests', '0002')
        finally:
            sys.stdout = stdout
            sys.stderr = stderr
        self.assertIn('CREATE INDEX CONCURRENTLY "my_index" ON "tests_mymodel" ("field1", "field2");', out.getvalue().strip())

        out = io.StringIO()
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = out
        sys.stderr = out
        try:
            call_command('sqlmigrate', 'tests', '0003')
        finally:
            sys.stdout = stdout
            sys.stderr = stderr
        self.assertIn('DROP INDEX CONCURRENTLY IF EXISTS "my_index";', out.getvalue().strip())

        out = io.StringIO()
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = out
        sys.stderr = out
        try:
            call_command('sqlmigrate', 'tests', '0003', backwards=True)
        finally:
            sys.stdout = stdout
            sys.stderr = stderr
        self.assertIn('CREATE INDEX CONCURRENTLY "my_index" ON "tests_mymodel" ("field1", "field2");', out.getvalue().strip())

        out = io.StringIO()
        stdout = sys.stdout
        stderr = sys.stderr
        sys.stdout = out
        sys.stderr = out
        try:
            call_command('sqlmigrate', 'tests', '0002', backwards=True)
        finally:
            sys.stdout = stdout
            sys.stderr = stderr
        self.assertIn('DROP INDEX CONCURRENTLY IF EXISTS "my_index";', out.getvalue().strip())

    def test_002_proper_migration(self):
        """Test migrations available in both directions"""
        call_command('migrate', 'tests', 'zero')
        call_command('migrate', 'tests',)
