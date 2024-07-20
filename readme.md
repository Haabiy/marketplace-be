## Overview

This project is the backend application for marketplace-fe, https://github.com/Haabiy/marketplace-fe, a marketplace UI. It is built using Django, ensuring compatibility with marketplace-fe's API (use the same version release tags, e.g: v0.0.1 for both marketplace-fe(frontend) and marketplace-be(backend).
## Endpoints

- **Login:** `POST /api/login/`
- **Add Source:** `POST /api/add-source/`
- **Read Sources:** `GET /api/read-source/`
- **Update Source:** `PUT/PATCH/POST /api/update-source/<uuid:id>/`
- **Delete Source:** `DELETE/POST /api/delete-source/<uuid:id>/`
- **Activate Source:** `POST /api/activate-source/<uuid:source_id>/`
- **Deactivate Source:** `POST /api/deactivate-source/<uuid:source_id>/`
- **Reactivate Source:** `POST /api/reactivate-source/<uuid:source_id>/`
- **Data Library:** `GET /api/data-library/`

## URL Patterns

```python
urlpatterns = [
    path('api/', include('myapp.urls')),
    path('admin/', admin.site.urls),
]
```

```python
urlpatterns = [
    path('', debug.default_urlconf), 
    
    # Login/Logout
    path('login/', authlogin.login_view, name='login'),
    path('logout/', authlogin.logout_view, name='logout'),

    #CRUD
    path('add-source/', crud.add_new_source, name="add_source"),
    path('read-source/', crud.data_sources, name="data_source"),
    path('update-source/<uuid:id>/', crud.update_source, name='update_source'),
    path('delete-source/<uuid:id>/', crud.delete_source, name='delete_source'),

    #STATUS
    path('activate-source/<uuid:source_id>/', sstatus.activate_source, name='activate_source'),
    path('deactivate-source/<uuid:source_id>/', sstatus.deactivate_source, name='deactivate_source'),
    path('reactivate-source/<uuid:source_id>/', sstatus.reactivate_source, name='reactivate_source'),
    path('data-library/', sstatus.data_library, name='data-library'),

]
```

## Notification settings
sending updates whenever we make changes

```python
async def handle_data_update(self, event):
    await self.fetch_data_sources()
```
```python
if self.channel_layer:
    await self.channel_layer.group_send(
        'DataLibrary',
        {
            'type': 'handle_data_update',
            'message': ({ "type": "update data sources"})
        }
    )
    await self.channel_layer.group_send(
        'DataSource',
        {
            'type': 'handle_data_update',
            'message': ({ "type": "update data sources"})
        }
    )
await self.send(text_data=json.dumps(response))
```
