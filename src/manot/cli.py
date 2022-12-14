from typing import Literal, Union, Optional, List
import requests
import json
from logger import log


class Manot:

    def __init__(self, url: str) -> None:
        self.__url = url


    def setup(
            self,
            name: str,
            images_path: str,
            ground_truths_path: str,
            detections_path: str,
            detections_metadata_format: Literal['cxcywh', 'xywh', 'xyx2y2'],
            classes_txt_path: str,
            data_provider: Literal['s3', 'local']
    ) -> Union[bool, dict]:

        url = f"{self.__url}/api/v1/collector/setup"
        data = {
            "name": name,
            "images_path": images_path,
            "ground_truths_path": ground_truths_path,
            "detections_path": detections_path,
            "detections_metadata_format": detections_metadata_format,
            "classes_txt_path": classes_txt_path,
            "data_provider": data_provider
        }

        try:
            response = requests.post(url=url, data=json.dumps(data))
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code == 202:
            log.info("Setup is successfully created.")
            return response.json()

        log.error(response.json()['message'])
        return False


    def get_setup(self, setup_id: int) -> Union[bool, None, dict]:

        url = f"{self.__url}/api/v1/setup/{setup_id}"

        try:
            response = requests.get(url=url)
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code != 200:
            log.warning("Setup not found.")
            return None

        log.info("Setup is successfully found.")
        return response.json()

    def insight(
            self,
            name: str,
            weight_name: str,
            setup_id: int,
            files: Optional[bytes],
            data_path: Union[str, List[str]],
            data_provider: Literal['s3', 'local', 'deeplake']
    ) -> Union[bool, dict]:

        url = f"{self.__url}/api/v1/real_time/"
        data = {
            "name": name,
            "weight_name": weight_name,
            "setup_id": setup_id,
            "files": files,
            "data_path": data_path,
            "data_provider": data_provider
        }

        try:
            response = requests.post(url=url, data=json.dumps(data))
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code == 202:
            log.info("Insights process is successfully started.")
            return response.json()

        log.error(response.json()['message'])
        return False

    def get_insight(self, insight_id: int) -> Union[bool, None, dict]:

        url = f"{self.__url}/api/v1/real_time/{insight_id}"

        try:
            response = requests.get(url=url).json()
        except Exception:
            log.error("There is problem with request.")
            return False

        if not response:
            log.warning("Insight not found.")
            return None

        log.info("Insight is successfully found.")
        return response
