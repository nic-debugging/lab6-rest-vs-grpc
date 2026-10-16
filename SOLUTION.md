# Lab 6: REST vs gRPC

## Performance measurements

All timings are in milliseconds per operation. Local tests ran on the laptop, same-zone tests used VMs in `us-west1-a`, and different-region tests used a client in `us-west1-a` and a server in `europe-west3-a`.

| Test | Local | Same-Zone | Different Region |
|---|---:|---:|---:|
| REST add | 2.679 | 3.994 | 324.657 |
| gRPC add | 1.095 | 1.510 | 145.978 |
| REST rawimg | 5.384 | 28.440 | 1355.576 |
| gRPC rawimg | 16.391 | 27.916 | 262.693 |
| REST dotproduct | 3.107 | 6.191 | 328.545 |
| gRPC dotproduct | 1.165 | 1.358 | 164.058 |
| REST jsonimg | 25.659 | 26.060 | 1482.773 |
| gRPC jsonimg | 31.666 | 44.181 | 276.601 |
| PING | 0.036 | 0.504 | 141.665 |

## Observations

In the local tests, gRPC was faster for the lightweight add and dot-product operations, while REST was faster for the image operations. In the same-zone tests, gRPC was faster for add and dot-product, raw-image timings were similar, and REST was faster for JSON-image processing. In the different-region tests, gRPC was faster for all four operations. The average ping increased from 0.504 ms in the same-zone tests to 141.665 ms across regions, showing the substantial impact of network latency on remote requests.

REST establishes a new TCP connection for each query, whereas gRPC reuses a TCP connection for multiple queries. Reusing a connection reduces connection overhead, which helps explain gRPC's better performance across regions. The results also show that transferring image data can make operations much slower when network latency is high. These timings are measurements from individual runs and may vary with network conditions and system load.

