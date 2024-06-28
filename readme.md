## Overview

A simple Django API for managing data sources with endpoints for adding, updating, deleting, and reading data sources. Newly added data sources are marked as active by default.

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
    # Auth
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
```

## Key Functions

- **login_view:** Handles user login.
- **add_new_source:** Adds a new data source.
- **data_sources:** Retrieves all data sources.
- **update_source:** Updates an existing data source.
- **delete_source:** Deletes a data source.

---
