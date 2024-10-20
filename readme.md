# 🚀 Marketplace Backend (Django)

## 📊 Overview

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![Amazon EMR](https://img.shields.io/badge/Amazon%20EMR-FF9900?style=for-the-badge&logo=amazon-aws&logoColor=white)

This project serves as the backend application for [marketplace-fe](https://github.com/Haabiy/marketplace-fe), a dynamic marketplace UI. Built with Django, it ensures seamless compatibility with the marketplace-fe API. 

> 🔗 **Important:** Always use matching version release tags (e.g., v0.0.1) for both marketplace-fe (frontend) and marketplace-be (backend).

![ASGI Layout](./Assets/Consumer-Vs-Signal.png)


## 🔌 WebSocket Consumers

### 📚 DataLibraryConsumer

Manages real-time display of data library metrics.

- **Group Name**: `DataLibrary`
- **Key Functions**:
  - `connect()`: Joins the WebSocket group
  - `disconnect()`: Leaves the WebSocket group
  - `fetch_data()`: Retrieves and sends latest data metrics
  - `get_data()`: Fetches data from the database (synchronous)

### 🔄 ActivationSourcesConsumer

Handles source activation, deactivation, and reactivation.

- **Group Name**: `ToggleVisibility`
- **Key Functions**:
  - `connect()`: Joins the WebSocket group
  - `disconnect()`: Leaves the WebSocket group
  - `receive()`: Processes activation-related actions
  - `activate_source()`, `deactivate_source()`, `reactivate_source()`

### 🌐 DataSourcesConsumer

Provides real-time updates of data sources.

- **Group Name**: `DataSource`
- **Key Functions**:
  - `connect()`: Joins the WebSocket group
  - `disconnect()`: Leaves the WebSocket group
  - `fetch_data_sources()`: Retrieves and sends latest data sources
  - `get_data_sources()`: Fetches data sources from the database (synchronous)

### 📝 SourceConsumer

Manages CRUD operations for sources.

- **Group Name**: `CRUDSource`
- **Key Functions**:
  - `connect()`: Joins the WebSocket group
  - `disconnect()`: Leaves the WebSocket group
  - `receive()`: Processes CRUD-related actions
  - `update_source()`: Updates an existing source
  - `add_source()`: Adds a new source

## 📡 Signals

Signals notify WebSocket groups about data changes.

- **Available Signals**: `crud`, `lib`, `source`, `toggle`, `source_lib`

- **Signal Receivers**:
  - `CRUDSourceSignal`: Handles CRUD operations
  - `DataLibrarySignal`: Updates the data library
  - `DataSourceSignal`: Updates data sources
  - `DataSource_DataLibSignal`: Updates both data sources and library
  - `ToggleVisibilitySignal`: Toggles source visibility

## 🛠 Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

## 🚀 Usage

1. Connect to WebSocket endpoints for real-time updates
2. Utilize WebSocket consumers to manage data operations
3. Signals will automatically update connected clients upon data changes

## 💡 Django Tips

### Notification Settings

Send updates on data changes:

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

### Model Fields

The `default` attribute in Django models:

```python
granularity = models.CharField(max_length=255, default='National')
```

> ℹ️ **Note**: The `default` value is only applied when the field is not present in the provided data. It won't override explicitly set empty values.

---

🔍 For more information on the data pipeline Amazon EMR runner part, please refer to [https://github.com/Haabiy/EMRRunner](https://github.com/Haabiy/EMRRunner)