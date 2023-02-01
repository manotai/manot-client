from tqdm.notebook import tqdm
import concurrent.futures
from .logger import log
import requests
import os.path
import glob
import uuid


class UploadManager:

    def __init__(self, directory: str, url: str, token: str):
        self.directory = directory
        self.url = url
        self.token = token
        self.save_path = str(uuid.uuid4())


    def upload_insight_data(self):

        if not self._is_exist(self.directory):
            log.error(f"No such directory: {self.directory}")
            return False

        correct_files = []
        for file_path in glob.glob(self.directory + "/*"):
            if file_path.endswith((".jpeg", ".jpg", ".png", ".avi", ".gif", ".m4v", ".mkv", ".mp4")):
                correct_files.append({"type": "images", "path": file_path})

        if not correct_files:
            log.error("There are no files to upload.")
            return False

        if self.upload_data(correct_files):
            return {"data_path": os.path.join(self.save_path, "images")}


    def upload_setup_data(self):

        images_path = os.path.join(self.directory, "images")
        detections_path = os.path.join(self.directory, "detections")
        ground_truths_path = os.path.join(self.directory, "ground_truths")
        classes_txt_path = os.path.join(self.directory, "classes.txt")
        if not self._is_exist(self.directory):
            log.error(f"No such directory: {self.directory}")
            return False
        if not self._is_exist(images_path):
            log.error(f"No such directory: {images_path}")
            return False
        if not self._is_exist(detections_path):
            log.error(f"No such directory: {detections_path}")
            return False
        if not self._is_exist(ground_truths_path):
            log.error(f"No such directory: {ground_truths_path}")
            return False
        if not os.path.isfile(classes_txt_path):
            log.error(f"No such directory: {classes_txt_path}")
            return False

        images = glob.glob(images_path + "/*")
        correct_files = []
        for image in images:
            detection = os.path.join(detections_path, f"{image.rsplit('/', 1)[1].rsplit('.', 1)[0]}.txt")
            if image.endswith((".jpeg", ".jpg", ".png", ".gif")) and os.path.isfile(detection):
                ground_truth = os.path.join(ground_truths_path, f"{image.rsplit('/', 1)[1].rsplit('.', 1)[0]}.txt")
                if os.path.isfile(ground_truth):
                    correct_files.extend([
                        {"type": "images", "path": image},
                        {"type": "detections", "path": detection},
                        {"type": "ground_truths", "path": ground_truth}
                    ])
                    continue
                ground_truth = os.path.join(ground_truths_path, f"{image.rsplit('/', 1)[1].rsplit('.', 1)[0]}.xml")
                if os.path.isfile(ground_truth):
                    correct_files.extend([
                        {"type": "images", "path": image},
                        {"type": "detections", "path": detection},
                        {"type": "ground_truths", "path": ground_truth}
                    ])

        if not correct_files:
            log.error("There are no files to upload.")
            return False

        correct_files.append({"type": "", "path": classes_txt_path})

        if self.upload_data(correct_files):
            return {
                "images_path": os.path.join(self.save_path, "images"),
                "ground_truths_path": os.path.join(self.save_path, "ground_truths"),
                "detections_path": os.path.join(self.save_path, "detections"),
                "classes_txt_path": os.path.join(self.save_path, "classes.txt")
            }



    def upload_data(self, data: list[dict]) -> bool:

        paths_count = len(data)
        progress_bar = tqdm(desc="Uploading...", total=paths_count)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            upload_result = [executor.submit(self.__upload_file, file) for file in data]
            for _ in concurrent.futures.as_completed(upload_result):
                progress_bar.update(1)
        progress_bar.close()

        return True


    def __upload_file(self, file) -> None:

        url = f"{self.url}/api/v1/data/upload"
        files = {"file": open(file["path"], 'rb')}
        headers = {"token": self.token}
        data = {"data_path": os.path.join(self.save_path, file["type"])}
        response = requests.post(url, files=files, data=data, headers=headers)

        if response.status_code == 200:
            log.info(f'{file["path"]} is successfully uploaded.')
        else:
            log.error("Something went wrong.")


    def _is_exist(self, path: str) -> bool:
        if os.path.isdir(path):
            return True
        return False
