from src.channel import Channel
from pprint import pprint

if __name__ == '__main__':
    moscowpython = Channel('UC-OVMPlMA3-YCIeg4z5z23A')
    print(moscowpython.title)
    print(moscowpython.description)
    print(moscowpython.channel_id)
    print(moscowpython.url)
    print(moscowpython.subscribers)
    print(moscowpython.video_count)
    print(moscowpython.views)
