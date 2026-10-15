
import argparse
import base64
import random
import time

import grpc

import lab6_pb2
import lab6_pb2_grpc


parser = argparse.ArgumentParser()
parser.add_argument('host')
parser.add_argument('cmd', choices=['add', 'rawImage', 'dotProduct', 'jsonImage'])
parser.add_argument('reps', type=int)
parser.add_argument('-p', '--port', type=int, default=50051)
parser.add_argument('-d', '--debug', action='store_true')
args = parser.parse_args()

with grpc.insecure_channel(f'{args.host}:{args.port}') as channel:
    stub = lab6_pb2_grpc.Lab6Stub(channel)

    def run_once():
        if args.cmd == 'add':
            result = stub.Add(lab6_pb2.AddMsg(a=5, b=10))
        elif args.cmd == 'rawImage':
            with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
                img = f.read()
            result = stub.RawImage(lab6_pb2.RawImageMsg(img=img))
        elif args.cmd == 'dotProduct':
            a = [random.random() for _ in range(100)]
            b = [random.random() for _ in range(100)]
            result = stub.DotProduct(
                lab6_pb2.DotProductMsg(a=a, b=b)
            )
        else:
            with open('Flatirons_Winter_Sunrise_edit_2.jpg', 'rb') as f:
                img = f.read()
            img = base64.b64encode(img).decode('utf-8')
            result = stub.JsonImage(lab6_pb2.JsonImageMsg(img=img))

        if args.debug:
            print(result)

    print(f"Running {args.reps} reps against {args.host}:{args.port}")

    start = time.perf_counter()

    for _ in range(args.reps):
        run_once()

    delta = (time.perf_counter() - start) * 1000 / args.reps
    print("Took", delta, "ms per operation")

