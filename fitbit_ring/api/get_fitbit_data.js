const access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyM1BTUkwiLCJzdWIiOiJDQzZYUk0iLCJpc3MiOiJGaXRiaXQiLCJ0eXAiOiJhY2Nlc3NfdG9rZW4iLCJzY29wZXMiOiJ3aHIgd251dCB3cHJvIHdzbGUgd3dlaSB3c29jIHdzZXQgd2FjdCB3bG9jIiwiZXhwIjoxNzYzNTY1Njc3LCJpYXQiOjE3MzIwMjk2Nzd9.cvepX3vu6damhlWV9WdSU0FMaMJ7oInLYuGNEDSb8qw"

fetch('https://api.fitbit.com/1/user/-/profile.json',{
    method: "GET",
    headers:{"Authorization": "Bearer " + access_token}
})
.then(response => response.json())
.then(json => console.log(json));