# Anomaly Detection Program

The `anomaly_detection.py` program implements three different detection methods for identifying anomalies within data sets. If no method is specified, it will print basic statistics.

## Examples
`python3 anomaly_detection.py -csva a.csv a1.csv -cvsn b.csv` # basic stats

`python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m1` # advanced statistic

`python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m2`  # 3-sigma

`python3 anomaly_detection.py -csva a.csv -cvsn b.csv -m3` # T-test

## Arguments
The following arguments can be used with the program:

- `-cvsn 1.csv 2.csv ... n.csv`: List with Modbus TCP IPFIX csvs that represent normal communication.
- `-csva 1.csv 2.csv ... n.csv`: List with Modbus TCP IPFIX cvss that will be investigated (compared to normal).
- `-m1`: Advanced statistic.
- `-m2`: 3-sigma.
- `-m3`: T-test.