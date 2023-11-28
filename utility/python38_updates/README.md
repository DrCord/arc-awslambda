# Python 3.8 lambda upgrade

Steps to upgrade all lambdas from python3.6 to python3.8

This assumes that a python3.8 compatible layer has already been created and is available in the dependecies.json file for the `global_dependencies` layer. This layer contains a psycopg2 version compiled for the python minor version.

NOTE: Lambdas without unit tests will need to be tested manually before upgrading.

1. Make a directory to contain the test-reports

        mkdir test-reports

2. Output list of all unit test lambdas

        list --tests_only >> lambdas_tests.txt

3. Output list of all regular (non-unit test) lambdas

        list --exclude_tests >> lambdas.txt

4. Run all lambda unit tests

        while IFS= read -r line; do test $line --output-xml; if [ "$(grep -c '<failure' "test-reports/test_{$line}.xml")" -gt 0 ]; then echo $line >> test_failures.txt; echo "$line FAILED unit tests"; fi; done < lambdas.txt

5. Address any unit test failures in *test_failures.txt*

6. Create list of lambdas with unit tests

        while IFS= read -r line; do if [ "$(grep -c '<failure' "test-reports/test_${line}.xml")" -eq 0 ]; then echo $line >> lambdas_with_tests.txt; fi; done < lambdas.txt

7. Create list of lambdas without unit tests  as *lambdas_without_tests.txt* using the output of the last command. The console should output any errors regarding no test file directly.

8. Upgrade all unit test lambdas

        while IFS= read -r line; do runtime $line; echo "$line runtime set"; update $line; echo "$line updated"; release $line staging; echo "$line release to staging"; release $line prod; echo "$line release to prod"; done < lambdas_tests.txt

9. Remove all test output files from the *test-reports* directory and the *test_failures.txt* file

        rm -rf ./test-reports/*
        rm test_failures.txt

10. Re-Run all lambda unit tests

        while IFS= read -r line; do test $line --output-xml; if [ "$(grep -c '<failure' "test-reports/test_${line}.xml")" -gt 0 ]; then echo $line >> test_failures.txt; echo "$line FAILED unit tests"; fi; done < lambdas_with_tests.txt

11. Address any failures in *test_failures.txt*
12. Remove any lambdas you choose not to proceed with upgrading from *lambdas_with_tests.txt*
13. Update runtime and code for all lambdas with unit tests

        while IFS= read -r line; do update $line; echo "$line updated"; runtime $line; echo "$line runtime set"; done < lambdas_with_tests.txt

14. Remove all test output files from the *test-reports* directory and the *test_failures.txt* file

        rm -rf ./test-reports/*
        rm test_failures.txt

15. Re-Run all lambda unit tests

        while IFS= read -r line; do test $line --output-xml; if [ "$(grep -c '<failure' "test-reports/test_${line}.xml")" -gt 0 ]; then echo $line >> test_failures.txt; echo "$line FAILED unit tests"; fi; done < lambdas_with_tests.txt

16. Address any failures in *test_failures.txt*
17. Remove any lambdas you choose not to proceed with releasing from *lambdas_with_tests.txt*

    NOTE: lambdas removed from the upgrade process at this point have their LATEST version (and hence *dev* alias) upgraded and will need to be addressed.

18. Release all lambdas with passing unit tests to *staging* and *prod*

        while IFS= read -r line; do if [ "$(grep -c '<failure' "test-reports/test_${line}.xml")" -eq 0 ]; then release $line staging; echo "$line released to staging"; release $line prod; echo "$line released to prod"; fi; done < lambdas_with_tests.txt

19. Manually test lambdas that do that have unit tests, address failures

20. Release all lambdas without unit tests to *staging* and *prod*

        while IFS= read -r line; do release $line staging; echo "$line released to staging"; release $line prod; echo "$line released to prod"; done < lambdas_without_tests.txt
