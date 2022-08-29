# SEAT-recommender
The Two-tower unsupervised Machine Learning Recommender API repository for the SIA-app-challenge.
Built with Flask, TensorFlow Recommenders and deployed on Heroku.

## About the Machine Learning


## Documentation
To make a request via curl, you may use the --request or -X flag followed by the HTTP POST method followed by the full URL. The API takes in a JSON object containing three keys parameters ( "userid", "input_indoorOutdoorScore", "input_leisureThrillScore", "input_cheapExpensiveScore") in its body. This information will be parse to the tensorflow model via flask and returned with a array of attractions id. 

**An example of curl POST request**
$ curl --location --request POST 'https://seat-recommender-api.herokuapp.com/api/recommender' \
--header 'Content-Type: application/json' \
--data-raw '{
    "userid": "2",
    "input_indoorOutdoorScore": 5,
    "input_leisureThrillScore": 3,
    "input_cheapExpensiveScore": 5
}'

You may also choose to send a POST request via an external application such as React to the same URL Route with the body containing the following.
 
**An example of JSON Object Input**

{
    "userid": "2",
    "input_indoorOutdoorScore": 5,
    "input_leisureThrillScore": 3,
    "input_cheapExpensiveScore": 5
}

**Expected Result**

{
    "attractions": [
        "9",
        "12",
        "31",
        "11",
        "2"
    ]
}


## Screenshots
Postman Example
