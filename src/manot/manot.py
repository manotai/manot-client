from typing import Literal, Union, Optional, List
from .upload_manager import UploadManager
from IPython import get_ipython
from .logger import log
import requests
import ipyplot
import json
import time
from pathlib import Path

try:
    if get_ipython():
        from tqdm.notebook import tqdm  # Using IPython terminal
    else:
        raise NameError()
except NameError:
    from tqdm import tqdm


class manotAI:

    def __init__(self, url: str) -> None:
        self.__url = url.rstrip('/')
        self.credentials_path = Path.home() / ".manot" / "credentials.json"
        if self.credentials_path.exists():
            with open(self.credentials_path, "r") as f:
                credentials_data = json.load(f)
            token = credentials_data["token"]
            url = f"{self.__url}/api/v1/user/"
            response = requests.get(url=url, headers={"token": token})
            if response.status_code == 200:
                self.__token = token
            else:
                log.info("Token expired please get a new token with get_token()")
        else:
            log.info("Missing credentials.json, get one with get_token()")

    def get_token(self, email: str, password: str) -> None:
        url = f"{self.__url}/api/v1/user/sign-in"
        response = requests.post(url=url, data=json.dumps({"email": email, "password": password}))
        if response.status_code == 200:
            self.__token = response.headers["access-token"]
            self.credentials_path.parent.mkdir(exist_ok=True)
            with open(self.credentials_path, "w") as f:
                credentials_data = {
                    "token": self.__token
                }
                json.dump(credentials_data, f)
                log.info("Credentials successfully updated!")
        else:
            log.info("Wrong credentials, please revise and try again!")
            

    def create_project(
            self,
            data_provider: Literal['s3', 'local', 'deeplake'],
            arguments: dict
    ) -> Union[bool, dict]:
        """
        :param data_provider: Provider name, it must be 's3', 'local' or 'deeplake'.
        :param arguments: Request data to create project.

            If data_provider is 'deeplake', arguments must contain such values::
                name: str,
                detections_metadata_format: Literal['cxcywh', 'xywh', 'xyx2y2'],
                deeplake_token: str,
                data_set: str,
                detections_boxes_key: str,`
                detections_labels_key: str,
                detections_score_key: str,
                ground_truths_boxes_key: str,
                ground_truths_labels_key: str,
                task: Literal['detection', 'classification']
                classes: Optional[list[str]],
                weight_name: Optional[Literal["yolov5s"]],
                description: Optional[str]
            Otherwise:
                name: str,
                images_path: str,
                ground_truths_path: str,
                detections_path: str,
                detections_metadata_format: Literal['cxcywh', 'xywh', 'xyx2y2'],
                classes_txt_path: str,
                weight_name: Optional[Literal["yolov5s"]],
                description: Optional[str]
        """

        url = f"{self.__url}/api/v1/project/"
        if data_provider == "deeplake":
            url = f"{url}deeplake"

        arguments.update({"data_provider": data_provider})

        try:
            response = requests.post(url=url, data=json.dumps(arguments), headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code == 201:
            log.info("Project process is being prepared to be started.")
            progress_result = self.__check_progress(self.get_project, response.json()["id"])
            if progress_result:
                if progress_result['status'] == "finished":
                    log.info("Project process has successfully finished.")
                elif progress_result['status'] == "failure":
                    log.error(f'There is problem to create project with id {response.json()["id"]}.')
                return progress_result
            else:
                log.error(f'There is problem to create project with id {response.json()["id"]}.')
                return False

        log.error(response.text)
        return False

    def get_project(self, project_id: int) -> Union[bool, None, dict]:

        url = f"{self.__url}/api/v1/project/{project_id}"

        try:
            response = requests.get(url=url, headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code != 200:
            log.warning("Project not found.")
            return None

        return response.json()

    def evaluate(
            self,
            name: str,
            project_id: int,
            data_path: Union[str, List[str]],
            data_provider: Literal['s3', 'local', 'deeplake'],
            weight_name: Optional[str] = None,
            deeplake_token: Optional[str] = None,
            percentage: Optional[float] = None,
            description: Optional[str] = None
    ) -> Union[bool, dict]:

        url = f"{self.__url}/api/v1/evaluation/"
        data = {
            "name": name,
            "project_id": project_id,
            "data_path": data_path,
            "data_provider": data_provider,
            "deeplake_token": deeplake_token,
            "percentage": percentage,
            "description": description
        }
        if weight_name:
            data["weight_name"] = weight_name

        try:
            response = requests.post(url=url, data=json.dumps(data), headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code == 201:
            log.info("Evaluation process is being prepared to be started.")
            progress_result = self.__check_progress(self.get_evaluation, response.json()["id"])
            if progress_result:
                if progress_result['status'] == "finished":
                    log.info("Evaluation process has successfully finished.")
                elif progress_result['status'] == "failure":
                    log.error(f'There is problem evaluation process with id {response.json()["id"]}.')
                return progress_result
            else:
                log.error(f'There is problem evaluation process with id {response.json()["id"]}.')
                return False

        log.error(response.text)
        return False

    def huggingface_evaluation(
            self,
            name: str,
            data_path: str,
            task: Optional[Literal['classification', 'segmentation', 'detection']] = 'detection',
            percentage: Optional[float] = None,
            model_path: Optional[str] = None,
            description: Optional[str] = None
    ) -> Union[bool, dict]:

        url = f"{self.__url}/api/v1/evaluation/huggingface"
        data = {
            "name": name,
            "data_path": data_path,
            "model_path": model_path,
            "task": task,
            "percentage": percentage,
            "description": description
        }
        try:
            response = requests.post(url=url, data=json.dumps(data), headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code == 201:
            log.info("Evaluation process is being prepared to be started.")
            progress_result = self.__check_progress(self.get_evaluation, response.json()["id"])
            if progress_result:
                if progress_result['status'] == "finished":
                    log.info("Evaluation process has successfully finished.")
                elif progress_result['status'] == "failure":
                    log.error(f'There is problem evaluation process with id {response.json()["id"]}.')
                return progress_result
            else:
                log.error(f'There is problem evaluation process with id {response.json()["id"]}.')
                return False

        log.error(response.text)
        return False

    def get_evaluation(self, evaluation_id: int) -> Union[bool, None, dict]:

        url = f"{self.__url}/api/v1/evaluation/{evaluation_id}"

        try:
            response = requests.get(url=url, headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code != 200:
            log.warning("Evaluation not found.")
            return None

        return response.json()

    def visualize_data_set(
            self,
            data_set_id: int,
            deeplake_token: str = None,
            group_similar=True,
            with_inference: Optional[bool] = False,
            huggingface_model: Optional[str] = None
    ):
        url = f"{self.__url}/api/v1/data_set/{data_set_id}?deeplake_token={deeplake_token}&group_similar={group_similar}"

        try:
            response = requests.get(url=url, headers={"token": self.__token}).json()
        except Exception:
            log.error("There is problem with request.")
            return False

        if not response:
            log.warning("Data Set not found.")
            return None

        images = response['data_set_images']
        images_urls = []
        for file in images:
            images_urls.append(self.__process(file['id'], deeplake_token, with_inference, huggingface_model))
        return ipyplot.plot_images(images_urls, img_width=200, show_url=False, max_images=len(images_urls))

    def upload_data(self, dir_path: str, process: Literal["project", "evaluation"]):

        upload_manager = UploadManager(directory=dir_path, url=self.__url, token=self.__token)
        if process == "project":
            return upload_manager.upload_project_data()
        elif process == "evaluation":
            return upload_manager.upload_evaluation_data()
        else:
            log.error("Process must be 'project' or 'evaluation'.")
            return False

    def calculate_map(
            self,
            ground_truths_path: str,
            detections_path: str,
            classes_txt_path: str,
            data_provider: Literal['s3', 'local'],
            data_set_id: Optional[int] = None
    ):
        url = f"{self.__url}/api/v1/metrics/map/"
        data = {
            "ground_truths_path": ground_truths_path,
            "detections_path": detections_path,
            "classes_txt_path": classes_txt_path,
            "data_provider": data_provider,
            "data_set_id": data_set_id
        }

        try:
            response = requests.post(url=url, data=json.dumps(data), headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code == 200:
            log.info("mAP has successfully calculated.")
            return response.json()

        log.error(response.text)
        return False

    def calculate_accuracy(
            self,
            images_path: str,
            predictions_path: str,
            classes_txt_path: str,
            data_provider: Literal['s3', 'local'],
            data_set_id: Optional[int] = None
    ):
        url = f"{self.__url}/api/v1/metrics/accuracy/"
        data = {
            "images_path": images_path,
            "predictions_path": predictions_path,
            "classes_txt_path": classes_txt_path,
            "data_provider": data_provider,
            "data_set_id": data_set_id
        }

        try:
            response = requests.post(url=url, data=json.dumps(data), headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code == 200:
            log.info("Accuracy has successfully calculated.")
            return response.json()

        log.error(response.text)
        return False

    def get_score(self, evaluation_id):
        url = f"{self.__url}/api/v1/evaluation/{evaluation_id}/scores"
        try:
            response = requests.get(url=url, headers={"token": self.__token})
        except Exception:
            log.error("There is problem with request.")
            return False

        if response.status_code != 200:
            log.warning(response.json()['message'])
            return None
        return response.json()

    def __process(self, image_id: int, deeplake_token: str = None, with_inference=False,huggingface_model=None):

        url = f"{self.__url}/api/v1/image/{image_id}?deeplake_token={deeplake_token}&with_inference={with_inference}&huggingface_model={huggingface_model}&time={time.time()}"
        return url

    def __check_progress(self, process_method, id):
        progress = 0
        status = 'started'
        progress_bar = tqdm(desc="Progress", total=100)
        while status == 'started':
            result = process_method(id)
            if result:
                status = result['status']
                if result["status"] != "failure":
                    progress_bar.update(int(result['progress'] - progress))
                    progress = result['progress']
                if result["status"] in ["finished", "failure"]:
                    progress_bar.close()
                    return result
            else:
                progress_bar.close()
                return False
            time.sleep(2)
