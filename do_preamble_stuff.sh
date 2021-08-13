#!/bin/bash

for file in $(find ./ -name '*.py'); do 
    cat preamble $file | sponge $file
done