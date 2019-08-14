# Omen/CurrencyConverter  
Converts euro to various the various currencies found at https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml

Parsing implemented using https://github.com/dabeaz/ply
Web server implemented using Django and django-rest-framework
https://www.djangoproject.com/
https://www.django-rest-framework.org/


### ENVIRONMENT
      pip install django
      pip install django-rest-framework
      pip install ply

### GETTING IT RUNNING
      git clone 
      python manage.py runserver

### UPDATING DB
      python manage.py fetch_exrates

### TESTING
      python manage.py test
