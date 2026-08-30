import json
from typing import TypedDict
from pathlib import Path
from zen_api import call_zen, ZenFreeModel, ZenResponse, ZenChatSession

DATA_PATH = Path("./raw_data/messages.ndjson")
PENNYWISE_DATA_PATH = Path("./raw_data/pennywise_regex.json")

class Message(TypedDict):
    _id: str
    thread_id: str
    address: str
    date: str
    date_sent: str
    protocol: str
    read: str
    status: str
    type: str
    reply_path_present: str
    subject: str
    body: str
    service_center: str
    locked: str
    sub_id: str
    error_code: str
    creator: str
    seen: str
    contains_otp: str
    restricted: str

def load_msg(path: str) -> list[Message]:
    msgs: list[Message] = []

    with open(path, "r") as f:
        for line in f:
            if line.strip():
                msg = json.loads(line)
                msgs.append(msg)

    return msgs

def load_pennywise_data(path: str):
    data = {}
    with open(path, "r") as f:
        data = json.load(f)

    return data


data = load_msg(DATA_PATH)
print("total data -> ",len(data))

data1 = load_pennywise_data(PENNYWISE_DATA_PATH)
print("data1",data1["regexes"][0])

# # single call
# r = call_zen("hello, where are you from", model=ZenFreeModel.MUSE_SPARK_1_2_CONTRIBUTOR_FREE)
# print("single call: ", r.text)

# # chat like call
# s = ZenChatSession(system_prompt="You are a pirate. Speak like a pirate.")
# r1 = s.ask("Hello! Who are you?") 
# print("chat r1: ", r1.text)
# r2 = s.ask("What style?")     
# print("chat r2: ", r2.text)
# s.reset()
