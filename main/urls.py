from django.urls import include, path
from rest_framework import routers
from . import views
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'projects', views.ProjectView)
router.register(r'issues', views.ProjectIssuesView)
router.register(r'comments', views.ProjectIssueCommentsView)
router.register(r'issue_labels', views.IssueLabelView)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-auth/', obtain_auth_token, name='api_token_auth'),  
]