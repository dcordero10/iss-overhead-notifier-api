import requests
from datetime import datetime
from time import time, sleep
import smtplib

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()
iss_lat = float(data["iss_position"]["latitude"])
iss_lng = float(data["iss_position"]["longitude"])


MY_EMAIL: "dtester752@gmail.com"
MY_PASSWORD: "testemail"
MY_LAT = 37.548271
MY_LONG = -121.988571
parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunset = data["results"]["sunrise"]
sunrise = data["results"]["sunset"]
time_now = str(datetime.now())
sunset = sunset.split("T")[1].split(":")[0]
sunrise = sunrise.split("T")[1].split(":")[0]
time_now = time_now.split(":")[0].split(" ")[1]


print(sunset)
print(sunrise)
print(time_now)

while True:
    sleep(60 - time() % 60)
    if time_now >= sunset and time_now <=sunrise:
        if iss_lat - MY_LAT in range(-5, 5):
            if iss_lng - MY_LONG in range(-5,5):
                with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
                    connection.starttls()
                    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
                    connection.sendmail(
                        from_addr=MY_EMAIL,
                        to_addrs=MY_EMAIL,
                        msg=f"Subject: ISS OVERHEAD! \n\n Your Lat/Long is {MY_LAT} {MY_LONG} and the ISS is currently at {iss_lat} and {iss_lng}")
            else:
                False
        else:
            False
    else:
        False


