#!/bin/sh
# First testing procedure

rm params/*

gfortran all_combinations/libraries.f90 all_combinations/main.f90 -o all_combinations.e

# ./all_combinations.e

echo "done"

