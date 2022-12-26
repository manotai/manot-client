manot
=============

[//]: # ([![pypi]&#40;https://img.shields.io/pypi/v/manot.svg&#41;]&#40;https://pypi.python.org/pypi/pydantic&#41;)
[//]: # ([![versions]&#40;https://img.shields.io/pypi/pyversions/manot.svg&#41;]&#40;https://github.com/pydantic/pydantic&#41;)
[//]: # ([![license]&#40;https://img.shields.io/github/license/manot-client/manot-client.svg&#41;]&#40;https://github.com/manotai/manot-client/blob/main/LICENSE&#41;)

Flask-Migrate is an extension that handles SQLAlchemy database migrations for Flask applications using Alembic. The database operations are provided as command-line arguments under the `flask db` command.

Installation
------------

Install manot with `pip`:

    pip install manot

Example
-------

This is an example how to start:

```python
from manot import Manot

manot = Manot('manot_service_url')
```

```python
setup = manot.setup(
    name="setup_example",
    images_path="/path/to/images",
    ground_truths_path="/path/to/labels",
    detections_path="/path/to/detections",
    detections_metadata_format="xyx2y2",  # it must be one of "xyx2y2", "xywh", or "cxcywh"
    classes_txt_path="/path/to/classes.txt",
    data_provider="local"  # it must be "s3" or "local"
)
print(setup)
# {"id": setup_id, "name": "setup_example", "status": "started"}

setup_info = manot.get_setup(setup["id"])
# when setup is successfully finished, then setup_info is {"id": setup_id, "name": "setup_example", "status": "started"}

```

```python
insight = manot.insight(
    name="insight_example",
    setup_id=setup["id"],
    data_path="/path/to/data",
    data_provider="local"  # it must be "s3" or "local"
)
print(insight)
# {"id": insight_id, "name": "insight_example", "status": "started"}

insight_info = manot.get_insight(insight["id"])
# when setup is successfully finished, then insight_info is {"id": insight_id, "name": "setup_example", "status": "started"}
```

```python
manot.visualize_data_set(insight_info['data_set']['id'])
```


Resources
---------

- [API Documentation](https://api.manot.ai/api-documentation/v1)
- [Jupyter Example](manot-client-notebook.ipynb)

[//]: # (- [pypi]&#40;https://pypi.python.org/pypi/manot&#41; )
