#!/bin/bash

cd `dirname $0`/../units

./elements cp 5 | ./group -t comb -n 4 | ./show
