#!/bin/bash

pwd
find . -name $1
find . -name $1 -exec tail -n 20 {} \;
