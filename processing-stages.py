# Multi-step contract signing engine for long workflows
import hashlib
import json
import time
import uuid
from datetime import datetime

class StepContract:
    def __init__(self, origin, target, goal):
        self.origin = origin
        self.target = target
        self.goal = goal
        self.uid = str(uuid.uuid4())
        self.timeline = []

    def snapshot(self):
        return json.dumps({
            "uid": self.uid,
            "origin": self.origin,
            "target": self.target,
            "goal": self.goal
        }, sort_keys=True)

    def hash_state(self):
        return hashlib.sha256(self.snapshot().encode()).hexdigest()

    def sign(self, key):
        base = self.hash_state()
        return hashlib.sha256(f"{base}:{key}".encode()).hexdigest()

    def verify(self, sig, key):
        return self.sign(key) == sig

    def record(self, event):
        self.timeline.append({
            "event": event,
            "time": datetime.utcnow().isoformat()
        })

def execute_flow():
    contract = StepContract("AgentA", "AgentB", "Research Agreement")
    contract.record("init")

    h = contract.hash_state()
    sig = contract.sign("agent_secret")

    contract.record("signed")

    print("Contract UID:", contract.uid)
    print("Hash:", h)
    print("Signature:", sig)
    print("Verified:", contract.verify(sig, "agent_secret"))

    contract.record("verified")
    return contract
