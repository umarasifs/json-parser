#!/bin/bash

source ".venv/Scripts/activate"

pip install .

pass_count=0
fail_count=0

for i in {1..33}; do
    parse "test/fail$i.json"
    actual_value=$?

    if [ $actual_value -ne 0 ];then
        echo "Test $i failed successfully"
        ((pass_count++))
    else
        echo "Test $i failed unsuccessfully"
        ((fail_count++))
    fi
done

for i in {1..6}; do
    parse "test/pass$i.json"
    actual_value=$?
    if [ $actual_value -eq 0 ];then
        echo "Test $i passed successfully"
        ((pass_count++))
    else
        echo "Test $i passed unsuccessfully"
        ((fail_count++))
    fi
done

echo "Total successes: $pass_count"
echo "Total unsuccesses: $fail_count"