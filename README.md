manot
=============

[![pypi](https://img.shields.io/pypi/v/manot.svg)](https://pypi.org/project/manot)
[![versions](https://img.shields.io/pypi/pyversions/manot.svg)]()
[![license](https://img.shields.io/pypi/l/manot)](https://github.com/manotai/manot-client/blob/main/LICENSE)

The manot SDK is a wrapper on top of our API to make it easier to work with our model performance monitoring system.
Using our SDK you can quickly set up your project by defining a few key parameters, including the paths to your data,
classes and model. Once the project is set up you will be able to use the insight method to extract outliers that manot
has detected on the new unstructured data that the performance of the model is evaluated on.

Installation
------------

Install manot with `pip`:

    pip install manot

Example
-------

This is an example how to start:

```python
from manot import manotAI

manot = manotAI("manot_service_url", "token")
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

```python
# Upload data for Setup or Insights process
manot.upload_data(dir_path="/path/to/data", process="process_name")
```
For Setup process
- dir_path is directory path, which must contain images, detections, and ground_truths folders and classes.txt file.
- process must be "setup".

For Insight process
- dir_path is directory path, which must contain data. Data formats must be ".jpeg", ".jpg", ".png", ".avi", ".gif", ".m4v", ".mkv" or ".mp4".
- process must be "insight".


Resources
---------

- [API Documentation](https://api.dev.manot.ai/api-documentation/v1)
- [Jupyter Example](https://github.com/manotai/manot-client/blob/main/manot-client-notebook.ipynb)

[//]: # (- [pypi]&#40;https://pypi.python.org/pypi/manot&#41; )
