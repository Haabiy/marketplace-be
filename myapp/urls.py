from django.contrib import admin
from django.urls import path
from django.views import debug
from myapp import authlogin, crud, status

#from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('', debug.default_urlconf), 
    
    # Login/Logout
    path('login/', authlogin.login_view, name='login'),
    path('logout/', authlogin.logout_view, name='logout'),

    #JWT
    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #CRUD
    path('add-source/', crud.add_new_source, name="add_source"),
    path('read-source/', crud.data_sources, name="data_source"),
    path('update-source/<uuid:id>/', crud.update_source, name='update_source'),
    path('delete-source/<uuid:id>/', crud.delete_source, name='delete_source'),

    #STATUS
    path('activate-source/<uuid:source_id>/', status.activate_source, name='activate_source'),
    path('deactivate-source/<uuid:source_id>/', status.deactivate_source, name='deactivate_source'),
    path('reactivate-source/<uuid:source_id>/', status.reactivate_source, name='reactivate_source'),
    path('data-library/', status.data_library, name='data-library'),

]