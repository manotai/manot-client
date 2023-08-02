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

Install manot using `pip`:

    pip install manot

Example
-------

This is an example how to start:

```python
from manot import manotAI

manot = manotAI("manot_service_url", "token")
```

Uploading data for creating a project
-------

```python
# Upload data to manot manager S3 bucket for creating a project. The data should be in YOLO format
manot.upload_data(dir_path="/path/to/data", process="project")
```

Running project 
-------

```python
# Create a project for "local","gcs" and "s3" providers
project = manot.create_project(
    data_provider="s3", # it must be "s3", "gcs" or "local"
    arguments={
            "name": "project_example",
            "images_path": "/path/to/images",
            "ground_truths_path": "/path/to/ground_truths",
            "detections_path": "/path/to/detections",
            "detections_metadata_format": "xyx2y2",  # it must be one of "xyx2y2", "xywh", or "cxcywh"
            "classes_txt_path": "/path/to/classes.txt",
            "task": 'task_type', #can be classification or detection, in case of classification you don't have to provide ground_truths_path or detections_metadata_format
            "weight_name": "yolov5s" # by default, it is None
            
        }
)
#for classification predictions should be in yolo format (txt file containing probability, classname) 

# Creating project using deeplake as data provider
project = manot.create_project(
    data_provider="deeplake",
    arguments={
            "name": "project_example",
            "detections_metadata_format": "xyx2y2",  # it must be one of "xyx2y2", "xywh", or "cxcywh"
            "deeplake_token": "your deeplake token",
            "data_set": "user/dataset/",
            "detections_boxes_key": "deeplake key where detection boxes are stored",
            "detections_labels_key": "deeplake key where where detection labels are stored",
            "detections_score_key": "deeplake key where detections score is stored",
            "ground_truths_boxes_key": "deeplake key where ground truth boxes are stored",
            "ground_truths_labels_key": "deeplake key where ground truth labels are stored",
            "classes": "classes for deeplake",
            "task": 'task_type', #can be classification or detection, in case of classification you don't have to provide detections_metadata_format
            "weight_name": "yolov5s" # by default, it is None   
        }
)
print(project)
# {"id": project_id, "name": "project_example", "status": "started"}

```
Get project by id 
-------

```python

project_info = manot.get_project(project["id"])
# when creating a project is successfully finished, then project_info is {"id": project_id, "name": "project_example", "status": "started"}
```
Upload data to get insights from 
-------

```python
# Upload data to manot manager S3 bucket to get insights
manot.upload_data(dir_path="/path/to/data", process="evaluation")
```
Running evaluation on data in s3, gcs or local machine
-------

```python
evaluation = manot.evaluate(
    name="insight_example",
    project_id=project["id"],
    data_path="/path/to/data",
    data_provider="s3",  # it must be "s3", "gcs" or "local"
    percentage="percentage" # percentage of images to be considered insight should be larger than 0 and less or equal than 100
)
print(evaluation)
# {"id": evaluation_id, "name": "evaluation_example", "status": "started"}

evaluation_info = manot.get_evaluation(evaluation["id"])
# when evaluation is successfully finished, then evaluation_info is {"id": evaluation_id, "name": "evaluation_example", "status": "finished"}
```

Running evaluation on hugging face model and dataset 
-------

```python
evaluation = manot.huggingface_evaluation(
    name='manot-huggingface',
    data_path="huggingface_dataset",
    model_path="huggingface_model",
    task="detection",
    percentage=0.5
)
evaluation_info = manot.get_evaluation(evaluation["id"])
```

```
scores = manot.get_score(evaluation['id'])
#returns list of all processed images graded by their score from 0 to 10 (higher is more impactful image)
# if the image cannot be assigned a score it will not be showing in the list 
```

```python
#in case of deeplake please also provide deeplake token 
manot.visualize_data_set(evaluation_info['data_set']['id'], deeplake_token,group_similar=True)
# if group similar is set to True(default) will only return unique images 
```

In case of detection task use this to calculate mAP on your data
```python
manot.calculate_map(
    ground_truths_path="/path/to/ground_truths",
    detections_path="/path/to/detections",
    classes_txt_path="/path/to/classes.txt",
    data_provider="local",  # it must be "s3", "gcs" or "local"
    data_set_id="data_set_id",  # if data_set_id is provided will calculate mAP only on selected data, otherwise will calculate mAP on all the data
)
```
In case of classification use this to calculate accuracy on your data

```python
manot.calculate_accuracy(
    images_path="/path/to/images",
    predictions_path="/path/to/predictions",
    classes_txt_path="/path/to/classes.txt",
    data_provider="local",  # it must be "s3", "gcs" or "local"
    data_set_id="data_set_id",  # if data_set_id is provided will calculate mAP only on selected data, otherwise will calculate mAP on all the data
)
```

Resources
---------

- [API Documentation](https://api.dev.manot.ai/api-documentation/v1)
- [Jupyter Example](https://github.com/manotai/manot-client/blob/main/manot-client-notebook.ipynb)

[//]: # (- [pypi]&#40;https://pypi.python.org/pypi/manot&#41; )
