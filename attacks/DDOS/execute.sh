#!/bin/bash

# Start 100 Python programs in a loop
for i in {1..100}; do
  python3 dos.py &
done
