from enum import Enum


class KafkaTopics(str, Enum):
    TEST = "topic_test"
    SEND_WA = "topic_ygS6sDBkwbM5QVqeduFt9nZmXJpTLHrG2hxEKCW7"
    SEND_MAIL = "topic_GRfmBK8erqbZ7PDVgkzv5NxaXWuAUc62JHd9tnC3"

    @classmethod
    def get_all(cls):
        return [member.value for member in cls]
