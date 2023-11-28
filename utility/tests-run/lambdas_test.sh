#!/bin/bash

# remove any existing test reports files
rm -rf ./test-reports/*
# generate input by replacing tabs with newlines in functions_dump.txt file
# and then sorting the file alphabetically
tr -d '\r' <functions_dump.txt >functions_dump_clean.txt;
tr '\t' '\n' <functions_dump_clean.txt >functions_list.txt;
sort -o functions_list.txt{,};
functions_to_test=(`cat functions_list.txt`);
noofelements=${#functions_to_test[*]};
echo "Number of lambdas to test: $noofelements";

# test lambdas
counter=0;
while [ $counter -lt $noofelements ];
do
  lambda_name="${functions_to_test[$counter]}"
  python ../../utility/lambda test $lambda_name --output-xml;
  counter=$(( $counter + 1 ));
done;

# output untested lambdas
counter=0;
while [ $counter -lt $noofelements ];
do
  lambda_name="${functions_to_test[$counter]}"
  if [ ! -f "test-reports/test_$lambda_name.xml" ]; then
    echo $lambda_name >> lambdas_untested.txt;
  fi
  counter=$(( $counter + 1 ));
done;


# parse test output for failures
for file in test-reports/*
  do
    if [ "$(grep -c '<failure' "${file}")" -gt 0 ]; then 
      echo $file > lambda_failures.txt;
      echo "$file failed testing";
    fi;
  done;
