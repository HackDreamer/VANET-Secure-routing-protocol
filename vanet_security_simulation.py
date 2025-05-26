import random
import hashlib
import matplotlib.pyplot as plt
import time
import pandas as pd
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class Metrics:
    total_messages = 0
    tampered_detected = 0

    @staticmethod
    def log_message(received, valid):
        Metrics.total_messages += 1
        if not valid:
            Metrics.tampered_detected += 1

    @staticmethod
    def report():
        print(f"Total Messages: {Metrics.total_messages}")
        print(f"Tampered Detected: {Metrics.tampered_detected}")
        if Metrics.total_messages:
            print(f"Detection Rate: {100 * Metrics.tampered_detected / Metrics.total_messages:.2f}%\n")


class Vehicle:
    def __init__(self, vehicle_id, speed, position):
        self.id = vehicle_id
        self.speed = speed
        self.position = position
        self.salt = "vanet" + str(random.random())
        self.private_key = RSA.generate(2048)
        self.public_key = self.private_key.publickey()

    def move(self, dt):
        self.position = (
            self.position[0] + self.speed * dt * random.uniform(-0.1, 1.1),
            self.position[1] + self.speed * dt * random.uniform(-0.1, 1.1),
        )

    def check_collision(self, other, threshold=1):
        distance = ((self.position[0] - other.position[0]) ** 2 +
                    (self.position[1] - other.position[1]) ** 2) ** 0.5
        return distance < threshold

    def hash_message(self, message):
        message_bytes = str(message).encode()
        hashes = {}
        for algo in ['sha256', 'md5', 'sha1', 'blake2b', 'sha3_256']:
            start = time.time()
            func = getattr(hashlib, algo)
            hashes[algo] = func(message_bytes + self.salt.encode()).hexdigest()
            hashes[f"{algo}_time"] = time.time() - start
        return hashes

    def sign_message(self, message):
        h = SHA256.new(str(message).encode())
        return pkcs1_15.new(self.private_key).sign(h)

    def verify_signature(self, message, signature, public_key):
        h = SHA256.new(str(message).encode())
        try:
            pkcs1_15.new(public_key).verify(h, signature)
            return True
        except (ValueError, TypeError):
            return False

    def generate_message(self):
        message = {
            "vehicle_id": self.id,
            "speed": self.speed,
            "position": self.position,
        }
        hashes = self.hash_message(message)
        signature = self.sign_message(message)
        return message, hashes, signature, self.public_key

    def check_integrity(self, message, hashes):
        calc_hashes = self.hash_message(message)
        for algo in ['sha256', 'md5', 'sha1', 'blake2b', 'sha3_256']:
            if hashes.get(algo) != calc_hashes.get(algo):
                return False
        return True

    def receive_message(self, message, hashes, signature, sender_public_key):
        print(f"Vehicle {self.id} received message from {message['vehicle_id']}")
        valid_integrity = self.check_integrity(message, hashes)
        valid_signature = self.verify_signature(message, signature, sender_public_key)
        if valid_integrity and valid_signature:
            print("Message is authentic and unaltered.\n")
            Metrics.log_message(True, True)
        else:
            print("Message FAILED integrity or signature verification!\n")
            Metrics.log_message(True, False)


def simulate(vehicles, dt, num_steps):
    hash_times = {algo: [] for algo in ['sha256', 'md5', 'sha1', 'blake2b', 'sha3_256']}
    for _ in range(num_steps):
        for vehicle in vehicles:
            vehicle.move(dt)
            collisions = [other for other in vehicles if vehicle != other and vehicle.check_collision(other)]
            if collisions:
                print(f"Collision detected between {vehicle.id} and {[v.id for v in collisions]}")
            message, hashes, signature, pubkey = vehicle.generate_message()
            for other in vehicles:
                if other != vehicle:
                    other.receive_message(message.copy(), hashes.copy(), signature, pubkey)
            for algo in hash_times:
                hash_times[algo].append(hashes[f"{algo}_time"])
    return hash_times


def plot_hash_times(hash_times):
    hash_data = [{"hash_type": algo, "time": t} for algo, times in hash_times.items() for t in times]
    df = pd.DataFrame(hash_data)
    df.boxplot(column="time", by="hash_type", showmeans=True)
    plt.title("Hash Function Times")
    plt.suptitle("")
    plt.xlabel("Hash Type")
    plt.ylabel("Time (s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


def main():
    vehicle1 = Vehicle("V1", 65, (0, 0))
    vehicle2 = Vehicle("V2", 50, (10, 20))
    vehicle3 = Vehicle("V3", 35, (30, 50))
    vehicle4 = Vehicle("V4", 20, (10, 50))

    print("Testing valid and tampered messages...\n")
    message, hashes, signature, pubkey = vehicle1.generate_message()
    vehicle2.receive_message(message.copy(), hashes.copy(), signature, pubkey)

    tampered = message.copy()
    tampered["speed"] = 100
    vehicle2.receive_message(tampered.copy(), hashes.copy(), signature, pubkey)

    print("Running simulation...\n")
    hash_times = simulate([vehicle1, vehicle2, vehicle3, vehicle4], dt=0.1, num_steps=100)

    Metrics.report()
    plot_hash_times(hash_times)


main()





