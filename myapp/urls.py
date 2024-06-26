from django.contrib import admin
from django.urls import path
from django.views import debug
from myapp import authlogin, crud, sstatus

from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('', debug.default_urlconf), # returns the default page for / end-point
    path('api/login/', authlogin.login_view, name='login'),

    #CRUD
    path('api/add-source/', crud.add_new_source, name="add_source"),
    path('api/read-source/', crud.data_sources, name="data_source"),
    path('api/update-source/<uuid:id>/', crud.update_source, name='update_source'),
    path('api/delete-source/<uuid:id>/', crud.delete_source, name='delete_source'),

    #STATUS
    path('api/activate-source/<uuid:source_id>/', sstatus.activate_source, name='activate_source'),
    path('api/deactivate-source/<uuid:source_id>/', sstatus.deactivate_source, name='deactivate_source'),
    path('api/reactivate-source/<uuid:source_id>/', sstatus.reactivate_source, name='reactivate_source'),
    path('api/data-library/', sstatus.data_library, name='data-library'),

]