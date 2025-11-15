# Weather Watcher TUI Processor.load_data() Test Plan

## Feature Under Test
Processor.load_data() loads a JSON-like dictionary into the Processor object by applying a preferences dictionary to filter it into a flat list of key-value pairs. Filtering logic is handled by the Processor.filter_data_recursive method, which recursively traverses the input dictionary according to the structure of the preferences dictionary and produces a list of key-value items (as strings). The list is then stored as Processor.filtered_data. This method does not return a value; just modifies the state of the Processor object.

## Objectives
When the feature is working correctly:
- It must accept a dictionary of arbitrary length and depth without raising an exception.
- It must clear previously loaded data before loading new data.
- It must produce a flat list and save it to the Processor object.
- If no preferences are found, it should save a blank list.
- If the input contains no items from preferences, it should save a blank list.
- It must not raise an exception in any case, and must clear any partial data and save a blank list in case of errors during filtering.

## Scope
### In Scope
- Return type of Processor.filter_data_recursive().
- Filtered data coherence between the input data and preferences dictionary.
- Ensuring empty input data or preferences result in an empty list being saved.
- Verifying flatness of the saved list.
- Verifying proper behavior during errors.

### Out of Scope
- Correct display of data in the TUI.
- Loading of preferences from environment (handled by sub classes).
- Validating data type of input data.
- Ensuring correctness of input data.
- Validating correctness of preference structure.


## Assumptions & Dependencies
### Assumptions
- Preferences will be present in the correct data type and structure.
- Input data will be provided in the correct data type.
- If preferences and input don't match, the method should skip them without error.
- Any errors raised during Processor.filter_data_recursive() will be caught in Processor.load_data().

### Dependencies
- Dependence on presence of initialized Processor.prefs dictionary.
- Dependence on structure of Processor.prefs dictionary conforming to expected layout.
- Dependence on recursive behavior of Processor.filter_data_recursive().

## Risks
- If no preferences are provided, valid input data may be unintentionally ignored.
- If an exception occurs at any point during filtering, all filtered results will be discarded, and no partial data will be preserved.
- If the structure of prefs doesn't match that of input data, presence of matching data may be ignored unintentionally.

## Test Level and Style
### Test Level
- Unit level - tests cover Processor.load_data() in isolation.
- Black box - only testing inputs and observable interactions.
- Integration and system tests will be handled elsewhere.

### Techniques
- Testing will consist of equivalence partitioning using test matrices.
- Testing will use custom prefs dictionaries.
- Testing will check success, error, and mismatch paths to ensure appropriately filtered data on success and empty filtered data on error or mismatch.
- Testing will check safe handling of errors that occur during filtering.
- Testing will include nested and flat input to verify correct filtering and recursive traversal.

## Tooling and Isolation
### Tooling
- Testing is performed using Pytest.
- Python tooling for test execution and structure.
- Prefs and input data will be faked using test parameters.

### Isolation
- Tests do not load prefs from the environment.
- Tests do not use I/O.
- Tests run entirely in memory.
- Tests do not use WeatherProcessor.

## Test Design and Coverage
- Tests will cover all functional paths, including success, error, edge cases, and mismatch between prefs and input.
- Tests will validate expected filtered data against input and simulated prefs.
- Tests will validate effectiveness of error handling during filtering.
- Tests will verify empty filtered data on error or mismatch.
- Tests will verify that previously loaded data is cleared upon a call to Processor.load_data(), regardless of success.

## Test Data and Environment
### Test Data
- Prefs:
    ```Python
    Processor.prefs = {
        "test":{
            "name": [
                True,
                "Town"
            ],
            "country": [
                False,
                "Nation"
            ],
            "region": {
                "district": [
                    True,
                    "District"
                ],
                "subdistrict": [
                    True,
                    "Burrough"
                ]
            }
        }
    }
    ```
    ```Python
    Processor.prefs = {}
    ```
- Data:
    ```Python
    # Success case
    data = {
        "test": {
            "name": "New York",
            "country": "USA"
        }
    }
    ```
    ```Python
    # Success case nested
    data = {
        "test": {
            "name": "New York",
            "country": "USA",
            "region":{
                "district":"Smithtown",
                "subdistrict":"Bronx"
            }
        }
    }
    ```
    ```Python
    # Mismatch case 1
    data = {
        "not_test": {
            "name": "New York",
            "country": "USA"
        }
    }
    ```
    ```Python
    # Mismatch case 2
    data = {
        "test": {
            "Town": "New York",
            "Nation": "USA"
        }
    }
    ```
    ```Python
    # Empty case
    data = {}
    ```

### Environment
- All tests run on local machine using Python 3.x.
- Tests do not load real environment variables.
- No external configuration is required beyond satisfying stated dependencies.

## Entry and Exit Criteria
### Entry Criteria
- The Processor class must be implemented with its dependencies satisfied.
- The Processor class must be accessible by the test file.
- Pytest must be installed in the Python 3.x environment.
- There must not be any unresolved syntax or runtime errors present in the feature code.
- Prefs must be initialized before calling Processor.load_data().

### Exit Criteria
- Test cases fully align with test plan.
- All identified test scenarios have been executed.
- All test cases execute and pass.
- Behavior matches all objectives laid out in test plan.
