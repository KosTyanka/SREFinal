# Load Simulation Results
## Test Scenarios
### Baseline Scenario Results
#### Container Stats
```
CONTAINER ID   NAME                   CPU %     MEM USAGE / LIMIT   MEM %     NET I/O           BLOCK I/O     PIDS
9cb6d43c4a40   load_tests-backend-1   0.16%     53.37MiB / 512MiB   10.42%    21.1MB / 30.5MB   0B / 4.1kB    1
1a3ec884700b   load_tests-db-1        0.00%     30.55MiB / 1GiB     2.98%     1.61kB / 0B       0B / 49.9MB   7
```
#### Load Test Results
```
```
### Medium Scenario Results
#### Container Stats
```
CONTAINER ID   NAME                    CPU %     MEM USAGE / LIMIT    MEM %     NET I/O           BLOCK I/O         PIDS
f1b074452e07   load_tests-backend-2    0.18%     51.64MiB / 1GiB      5.04%     20.9MB / 30.4MB   0B / 4.1kB        1
924d25d817a6   load_tests-db-1         0.01%     17.98MiB / 1GiB      1.76%     1.61kB / 0B       0B / 344kB        7
97ab0c42935b   srefinal-prometheus-1   0.00%     26.59MiB / 15.2GiB   0.17%     20.1kB / 23.1kB   2.13MB / 65.5kB   18
c21677c5fdb5   srefinal-grafana-1      0.33%     92.66MiB / 15.2GiB   0.60%     133kB / 404kB     1.87MB / 291kB    17
```
#### Load Test Results
```
```
### High Scenario Results
#### Container Stats
```
CONTAINER ID   NAME                    CPU %     MEM USAGE / LIMIT    MEM %     NET I/O           BLOCK I/O        PIDS
c01e6d0dd2be   load_tests-backend-2    0.18%     52.44MiB / 2GiB      2.56%     21.2MB / 30.6MB   0B / 4.1kB       1
dd8f44b12f89   load_tests-db-1         0.01%     18.06MiB / 1GiB      1.76%     1.61kB / 0B       0B / 344kB       7
97ab0c42935b   srefinal-prometheus-1   0.00%     37.19MiB / 15.2GiB   0.24%     64.6kB / 71.2kB   2.13MB / 270kB   18
c21677c5fdb5   srefinal-grafana-1      0.71%     85.8MiB / 15.2GiB    0.55%     274kB / 639kB     1.93MB / 426kB   17
```
#### Load Test Results
```
```
### Spike Scenario Results
#### Container Stats
```
CONTAINER ID   NAME                    CPU %     MEM USAGE / LIMIT    MEM %     NET I/O           BLOCK I/O        PIDS
8633c6fc323c   load_tests-backend-1    0.16%     51.63MiB / 4GiB      1.26%     20.8MB / 30.3MB   0B / 4.1kB       1
4934683eacbb   load_tests-db-1         0.01%     18.27MiB / 1GiB      1.78%     1.67kB / 0B       57.3kB / 344kB   7
97ab0c42935b   srefinal-prometheus-1   0.00%     32.28MiB / 15.2GiB   0.21%     93.7kB / 102kB    2.13MB / 451kB   18
c21677c5fdb5   srefinal-grafana-1      0.19%     83.48MiB / 15.2GiB   0.54%     365kB / 775kB     2.24MB / 709kB   17
```
#### Load Test Results
```
```
