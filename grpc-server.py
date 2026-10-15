
import argparse
import base64
import io
from concurrent import futures

import grpc
from PIL import Image

import lab6_pb2
import lab6_pb2_grpc


class Lab6Server(lab6_pb2_grpc.Lab6Servicer):

    def Add(self, request, context):
        return lab6_pb2.AddReply(sum=request.a + request.b)

    def RawImage(self, request, context):
        try:
            img = Image.open(io.BytesIO(request.img))
            return lab6_pb2.ImageReply(
                width=img.size[0],
                height=img.size[1]
            )
        except Exception:
            return lab6_pb2.ImageReply(width=0, height=0)

    def DotProduct(self, request, context):
        if len(request.a) != len(request.b):
            context.abort(grpc.StatusCode.INVALID_ARGUMENT,
                          "Vectors must have the same length")

        result = sum(a * b for a, b in zip(request.a, request.b))
        return lab6_pb2.DotProductReply(dotproduct=result)

    def JsonImage(self, request, context):
        try:
            img_data = base64.b64decode(request.img)
            img = Image.open(io.BytesIO(img_data))
            return lab6_pb2.ImageReply(
                width=img.size[0],
                height=img.size[1]
            )
        except Exception:
            return lab6_pb2.ImageReply(width=0, height=0)


parser = argparse.ArgumentParser()
parser.add_argument('-p', '--port', type=int, default=50051)
args = parser.parse_args()

server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
lab6_pb2_grpc.add_Lab6Servicer_to_server(Lab6Server(), server)
server.add_insecure_port(f'[::]:{args.port}')
server.start()

print(f"Running gRPC server on port {args.port}")
server.wait_for_termination()

