<h1 align="center"><a href="https://refyne-car-rental-api.herokuapp.com/" target="_blank">Refyne Car Rental API</a></h1>
<p align="center">
  <b> Refyne Car Rental </b> is an API to manage Car Rental Services.
</p>
<br>
<p align="center">
<img src="https://github.com/divy-14/Refyne_CarRental/blob/main/DataBaseLayout.png" alt="demo Xmeme" width="800px" height="500px">
</p>
<p align="center"> Fig: Database Design</p>
<br>

<h3>What is Refyne 🚗 Rental API ?</h3>
<ul>
  <li> This is an API which one can use to manage their vehicle rental services. </li>
  <li> Add the list of available vehicles into the CAR Database. </li>
  <li> Add the list of users to the USER Database. </li>
  <li> Allow the users to calculate the price of their ride and also allow them to book any available vehicles. </li>
  <li> The API keeps track of all the booked vehicles as well as provides user with the information about available vehicles for a given duration </li>
  <li> The user can track their history of bookings as well as we can track the history of a particular vehicle providing the system with Robustness.
</ul>

<h3>Tech Stack:</h3>
<ul>
<li> <b>Backend:</b>
<ul> 
<li> Django & Django Rest Framework</li>
</ul>
</li>
<li> <b>Database:</b>
<ul> 
<li> SQLite </li>
</ul> 
</li>
</ul>

<h3>Using the API (curl commands):</h3>

<ul>
<li> API to Add a user and Add a car in the system. 
<br>
<br>
<ul>
  <li><b>GET request -> CARS 👇</b> <p> curl -i --location --request GET  http://localhost:8000/cars/ </p></li>

  <li><b>POST request -> CARS 👇</b> <p>curl --location --request POST http://localhost:8000/cars/ --header Content-Type:application/json --data-raw "{\"carLicenseNumber\":\"jefefuef21\",  \"Manufacturer\":\"HYUndai\",  \"Model\":\"MP\" , \"base_price\":\"189000\", \"pph\":\"1000\", \"security_deposit\":\"2000\"}"</p> </li>
  
  <li><b>GET request -> USERS 👇</b> <p>curl -i --location --request GET  http://localhost:8000/user </p></li>
  
  <li><b>POST request -> USERS 👇</b> <p>curl --location --request POST http://localhost:8000/user/ --header Content-Type:application/json --data-raw "{\"userName\":\"Jhonny\",  \"userMobile\":\"9876767890\"}"</p> </li>
</ul>
</li>

<li> Given a time range, figure out which cars are available for that duration
<br>
<br>
<ul>
  <li><b>GET request -> CARS 👇</b> <p> curl -i --location --request GET http://localhost:8000/search-cars/ --header Content-Type:application/json --data-raw "{\"fromDate\":\"2021-03-30 10:55:31\", \"toDate\":\"2021-03-31 10:55:31\"}"</p></li> 
</ul>
</li>

<li> Given a time range calculate pricing for that car.
<br>
<br>
<ul>
  <li><b>POST request -> CARS 👇</b> <p> curl --location --request POST http://localhost:8000/calculate-price/ --header Content-Type:application/json --data-raw "{\"carLicenseNumber\":\"jefefuef21\",  \"fromDate\":\"78\", \"toDate\":\"80\"}"</p></li> 
</ul>
</li>



<ul>









