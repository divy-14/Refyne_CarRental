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
  <li><b>GET request 👇</b> <p> curl -i --location --request GET  https://refyne-car-rental-api.herokuapp.com/cars </p></li>

  <li><b>POST request 👇</b> <p>curl --location --request POST https://refyne-car-rental-api.herokuapp.com/cars --header Content-Type:application/json --data-raw "{\"carLicenseNumber\":\"jefefuef21\",  \"Manufacturer\":\"HYUndai\",  \"Model\":\"MP\" , \"base_price\":\"189000\", \"pph\":\"1000\", \"security_deposit\":\"2000\"}"</p> </li>
  
  <li><b>GET request -> USERS 👇</b> <p>curl -i --location --request GET https://refyne-car-rental-api.herokuapp.com/user </p></li>
  
  <li><b>POST request 👇</b> <p>curl --location --request POST https://refyne-car-rental-api.herokuapp.com/user --header Content-Type:application/json --data-raw "{\"userName\":\"Jhonny\",  \"userMobile\":\"9876767890\"}"</p> </li>
</ul>
</li>

<li> Given a time range, figure out which cars are available for that duration
<br>
<br>
<ul>
  <li><b>POST request 👇</b> <p> curl -i --location --request POST http://localhost:8000/search-cars/ --header Content-Type:application/json --data-raw "{\"fromDate\":\"2021-03-30 10:55:31\", \"toDate\":\"2021-03-31 10:55:31\"}"</p></li> 
</ul>
</li>

<li> Given a time range calculate pricing for that car.
<br>
<br>
<ul>
  <li><b>POST request 👇</b> <p> curl --location --request POST https://refyne-car-rental-api.herokuapp.com/calculate-price --header Content-Type:application/json --data-raw "{\"carLicenseNumber\":\"jefefuef21\",  \"fromDate\":\"78\", \"toDate\":\"80\"}"</p></li> 
</ul>
</li>

<li> Given a user a return list of all the cars he has booked along with their price and durations
<br>
<br>
<ul>
  <li><b>GET request 👇</b> <p> curl -i --location --request GET https://refyne-car-rental-api.herokuapp.com/user/bookings/{mobileNumber} </p></li> 
</ul>
</li>

<li> Given a Car return a list of users who have booked the car along with their durations
<br>
<br>
<ul>
  <li><b>GET request 👇</b> <p> curl -i --location --request GET  https://refyne-car-rental-api.herokuapp.com/car/bookings/{carNumberPlate} </p></li> 
</ul>
</li>

<li> To book a car for certain durations.
<br>
<br>
<ul>
  <li><b>POST request 👇</b> <p> curl --location --request POST https://refyne-car-rental-api.herokuapp.com/car/book --header Content-Type:application/json --data-raw "{\"carLicenseNumber\":\"k1h3u13h1\",  \"fromDate\":\"2018-11-10 10:55:31\", \"toDate\":\"2018-11-10 10:55:31\", \"userid\":\"9810159145\"}" </p></li> 
</ul>
</li>

</ul>









