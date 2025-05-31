# Load Test Results Summary
## Test Scenarios and Results
### Environment
- Date: Sat May 31 12:04:13 +05 2025
- Backend URL: http://localhost:8000
- Docker Resources: Default configuration
### Baseline Load Test Results
```
Health Endpoint:
Requests per second:    1827.76 [#/sec] (mean)
Time per request:       54.712 [ms] (mean)
Time per request:       0.547 [ms] (mean, across all concurrent requests)
Transfer rate:          292.73 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   0.9      1       5
Processing:     6   52   7.5     53      72
Waiting:        2   40   8.4     41      57
Total:          7   53   6.9     55      72

Percentage of the requests served within a certain time (ms)
  50%     55
  66%     56
  75%     56

Concerts Endpoint:
Requests per second:    1760.03 [#/sec] (mean)
Time per request:       56.817 [ms] (mean)
Time per request:       0.568 [ms] (mean, across all concurrent requests)
Transfer rate:          807.83 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    1   1.0      1       6
Processing:     9   54   8.4     54      73
Waiting:        2   41   9.1     43      69
Total:         10   55   7.7     55      74

Percentage of the requests served within a certain time (ms)
  50%     55
  66%     56
  75%     57
```
### Medium Load Test Results
```
Health Endpoint:
Requests per second:    1800.95 [#/sec] (mean)
Time per request:       277.631 [ms] (mean)
Time per request:       0.555 [ms] (mean, across all concurrent requests)
Transfer rate:          288.43 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    6   5.1      4      25
Processing:    27  263  44.8    261     361
Waiting:        2  195  48.9    201     335
Total:         27  269  41.4    264     361

Percentage of the requests served within a certain time (ms)
  50%    264
  66%    274
  75%    276

Concerts Endpoint:
Requests per second:    1684.24 [#/sec] (mean)
Time per request:       296.869 [ms] (mean)
Time per request:       0.594 [ms] (mean, across all concurrent requests)
Transfer rate:          773.04 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    5   5.2      4      26
Processing:    40  283  45.0    280     359
Waiting:        2  224  46.5    224     335
Total:         40  288  41.9    287     365

Percentage of the requests served within a certain time (ms)
  50%    287
  66%    296
  75%    307
```
### High Load Test Results
```
Health Endpoint:
Requests per second:    1898.02 [#/sec] (mean)
Time per request:       526.866 [ms] (mean)
Time per request:       0.527 [ms] (mean, across all concurrent requests)
Transfer rate:          303.98 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   14  11.2     12      57
Processing:    59  501  65.9    506     692
Waiting:        2  357  88.7    356     526
Total:         59  515  58.8    517     695

Percentage of the requests served within a certain time (ms)
  50%    517
  66%    522
  75%    529

Concerts Endpoint:
Requests per second:    1772.38 [#/sec] (mean)
Time per request:       564.212 [ms] (mean)
Time per request:       0.564 [ms] (mean, across all concurrent requests)
Transfer rate:          813.50 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   12  10.2      9      54
Processing:    56  537  75.8    535     669
Waiting:        2  419  78.1    426     617
Total:         56  548  68.9    546     673

Percentage of the requests served within a certain time (ms)
  50%    546
  66%    553
  75%    565
```
### Spike Load Test Results
```
Health Endpoint:
Requests per second:    1834.78 [#/sec] (mean)
Time per request:       1090.052 [ms] (mean)
Time per request:       0.545 [ms] (mean, across all concurrent requests)
Transfer rate:          293.85 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   40  31.5     39     101
Processing:   144  901 263.6    980    1230
Waiting:        2  704 234.8    753    1043
Total:        144  941 245.4   1001    1233

Percentage of the requests served within a certain time (ms)
  50%   1001
  66%   1091
  75%   1097

Concerts Endpoint:
Requests per second:    1799.34 [#/sec] (mean)
Time per request:       1111.516 [ms] (mean)
Time per request:       0.556 [ms] (mean, across all concurrent requests)
Transfer rate:          825.87 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0   39  26.6     31      98
Processing:   138  930 191.0   1018    1099
Waiting:        2  708 218.7    775    1083
Total:        138  968 170.1   1072    1099

Percentage of the requests served within a certain time (ms)
  50%   1072
  66%   1082
  75%   1089
```
