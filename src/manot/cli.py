import uuid
import base64
from src.actioncable import Message, Subscription, Connection


class Manot:

    def __init__(self):
        self.__token = self.__generate_uuid()
        self.__connection = Connection(url="ws://127.0.0.1:3000/cable")
        self.__connection.connect()
        self.__subscription = Subscription(self.__connection, identifier={'channel': 'ImageChannel', 'token': self.__token})
        self.__subscription.on_receive(self.__on_receive)
        self.__subscription.create()

    def __on_receive(self, message):
        print('New message arrived!')
        if type(message) is dict and 'images' in message and message['images'] and type(message['images']) is list:
            self.__image_to_np_array(message['image'])
            self.__listener("asass")
        else:
            print("No required param in message.")

    def __send_message(self, message:str):
        message = Message(
            action='get_similar_images',
            data={'message': message}
        )
        self.__subscription.send(message)

    def __image_to_np_array(self, base64_image:bytes):

        with open("imageToSave.png", "wb") as fh:
            fh.write(base64.b64decode((base64_image)))
            fh.close()


    def listen(self, inference_fn, options=None):
        if options is None:
            options = {}
        elif options is not dict:
            raise('Wrong Argument pased')
        self.__listener = inference_fn
        self.__options = options

        # TODO do request to server
        #TODO socket
        self.__send_message("Started to listen...")



    def on(self, img):
        print(img)
        # self.listener(options,img)

    def __generate_uuid(self) -> str:
        return str(uuid.uuid4())



def my_inference(image):
    print("Image name already has reached into inference: ", image)


def main():

    manot = Manot()
    manot.listen(my_inference)

if __name__ == '__main__':
    main()
