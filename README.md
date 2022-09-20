# zazzone
A social media website developed using django framework.
![Screenshot from 2022-08-10 07-05-26](https://user-images.githubusercontent.com/72627757/183827608-bb165373-e2ad-45b7-b303-84732273fba7.png)
![Screenshot from 2022-08-10 07-10-56](https://user-images.githubusercontent.com/72627757/183828303-07c1a25e-b3e4-467d-a35f-1ec873c76f18.png)
![Screenshot from 2022-08-10 07-11-40](https://user-images.githubusercontent.com/72627757/183828570-ce607038-c3a2-4d3f-9eea-79f87d02b8b9.png)
![Screenshot from 2022-08-10 07-14-54](https://user-images.githubusercontent.com/72627757/183828686-2835f2ce-77e2-483b-8c7a-8a2d892acb60.png)


MODULES (libraries)
1.   To install Django (pip install django)
2.   To install pillow for image resize (pip install pillow)
3.   To install django-countries (pip install django-countries) i.e it provides a country field for django models:
    NB: add 'django_countries' in the INSTALLED_APP app.


4.   To install django-phonenumber-field (pip install django-phonenumber-field) i.e An international phone number field for django models, a django library which interface with python phonenumber (the below phonenumbers) to validate, pretty print and convert phone numbers:
    NB: add 'phonenumber_field' in the INSTALLED_APP


5.   To install phonenumbers (pip install phonenumbers) i.e A python version of google's common library for parsing, formatting, storing and validating international phone numbers.


6.  pip install geocoder
        Geocoder is a simple Python geocoding library. It makes it very easy to work with geocoding providers such as Google or Bing. It is also very useful to locate an IP address. 

7.  pip install folium
        Folium is a library that makes it easy to visualize data that has been manipulated in Python on an interactive leaflet map.


NOTE:
Change the path of default images, before/when deploying for production to meet your VM route


In the view:
from django.core.mail import send_mail
from django.conf import settings


def message(request):
    subject_email = form.cleaned_data.get('subject')
    email_message_body = form.cleaned_data.get('message_body')
    recepient = [message_now.email]
    send_mail(subject_email, email_message_body, settings.EMAIL_HOST_USER, recepient, auth_user='Usman Musa Website')


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '<user>@gmail.com' # OR os.environ.get('EMAIL_USER')
EMAIL_HOST_PASSWORD = '******************' # OR os.environ.get('EMAIL_PASSWORD')


For yahoo
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.yahoo.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = '<user>@yahoo.com'
EMAIL_HOST_PASSWORD = '****************'


For localhost
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
from django.core.mail import EmailMessage
email = EmailMessage('PasswordResetEmail', 'Hello kindly follow this link for password backup', 'Skysurf', to=['user@gmail.com'])
email.send()
