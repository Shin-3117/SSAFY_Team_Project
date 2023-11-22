from django.test import TestCase

# Create your tests here.
from datetime import date, timedelta
print(str(date.today() - timedelta(days=1)).replace("-", ""))