from django.urls import include, path, re_path
from django.conf import settings
from django.views.static import serve
from rest_framework import routers

from . import views
from . import personViewSet

# rest api routes
router = routers.DefaultRouter()

router.register(r'person', personViewSet.PersonViewSet, base_name=r'person')

urlpatterns = [
# Static files
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}), # Requests for static files e.g. css, js, svg, etc

# API
    re_path(r'^api/v1/', include(router.urls)), # Function-specific api's e.g. http://localhost:8000/api/v1/person/
    re_path(r'^api/v1/options/(?P<category>\w+)/(?P<item>\w+)/$', views.get_options), # Serves lists of options defined in the 'plus__definition' table

# Home page
    # Catches everything apart from the login, static files and the api calls
    # For example, a request for 'https://app.org/persons' would be caught by views.home
    # The index.html template would be served with a link to the javascript bundle
    # App.jsx would then use React Router to map the '/person' suffix and mount the personQuery component
    re_path(r'^((?!api/v1/).)*$', views.home),
]

