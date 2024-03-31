import datetime
from calendar import calendar


# Tehdään logiikka, jolla luodaan 0 data tietueet niile päiville, joilta ei saada dataa.
# Tehdään se tässä, niin ei tarvitse frontendissä tehdä.
# Datan pitää olla muotoa [{"day": 1 "total_kwh": 0}]
def generate_zero_for_missing_days_in_month_query(fetched_data, year: int, month: int):
    # Luodaan listat kuukausista, joissa on 31 ja 30 päivää.
    _31days = [1, 3, 5, 7, 8, 10, 12]
    _30days = [4, 6, 9, 11]

    # Määritellään numbers_of_days listojen tai karkausvuoden perusteella.
    if month in _31days:
        numbers_of_days = 31
    elif month in _30days:
        numbers_of_days = 30
    else:
        if calendar.isleap(year):
            numbers_of_days = 29
        else:
            numbers_of_days = 28

    # Haetaan tietokannasta saadusta datasta päivät, jotka on saatu.
    days_fetched = [i["day"] for i in fetched_data]

    # Alustetaan new_data list ja index(käytetään returned_datan tiedon hakemisessa)
    data = []
    index = 0

    # Silmukoidaan valitun kuukauden päivien lukumäärän mukaisesti
    for day_number in range(1, numbers_of_days + 1):

        # Jos kyseinen päivä ei löydy tietokannasta, luodaan nolla tietue
        if day_number not in days_fetched:
            data_of_day = {"day": day_number, "total_kwh": 0}

        # Muussa tapauksessa listataan tietokannasta tullut datasta
        else:
            data_of_day = fetched_data[index]
            index += 1

        data.append(data_of_day)

    return data


# Palauttaa viikon tilastot. Jos viikonpäivälle ei löydy dataa, siihen lisätään tyhjä tietue.
# Tarvitsee vuoden karkausvuoden laskentaa varten, sekä viikonnumeron haluttua viikkoa varten
# Lisäksi tarvitsee datan muotoa [{"date": "2024-03-31", "total_kwh": 0}] (vaati datetime objektin)
def generate_zero_for_missing_days_in_week_query(fetched_data, year, week_number):
    # Tämä tuottii ongelmia kuukauden vaihtumisen kanssa, johtuen viikon alun laskelmasta,
    # joka perustuu tällä hetkellä pelkästään vuoden ja viikon numeroon.
    # Jos viikko kattaa kaksi eri kuukautta, viikon alku ei välttämättä vastaa kuun alkua.
    #- Dorian

    # Laske viikon alku
    first_day = datetime.date(year, 1, 1)
    start_of_week = first_day + datetime.timedelta(days=(week_number - 1) * 7 - first_day.weekday())

    # Säädä viikon alkua vastaamaan vastaavan kuukauden alkua
    start_of_week -= datetime.timedelta(days=start_of_week.day - 1)

    # Alusta tietoluettelo ja hakemisto fetched_data-tietojen iterointia varten
    dates_of_week = [start_of_week + datetime.timedelta(days=i) for i in range(7)]

    # Alusta tietoluettelo ja hakemisto fetched_data-tietojen iterointia varten
    data = []
    index = 0
    for i in range(7):
        # Tarkista, vastaako fetched_data päivämäärä viikon nykyistä päivämäärää
        if index < len(fetched_data) and dates_of_week[i] == fetched_data[index]["date"]:
            data.append(fetched_data[index])
            index += 1
        else:
            # Jos vastaavuutta ei löydy, liitä sanakirja, jossa on päivämäärä ja total_kwh-arvo 0
            data.append({"date": dates_of_week[i], "total_kwh": 0})

    return data


# Nolla tietueet hourly by day hauille. Syötä queryssä saatu data.
# Datan pitää olla muotoa [{"hour": 0 "total_kwh": 0}]
def generate_zero_for_missing_hours_in_day_query(fetched_data):
    # Haetaan tietokannasta saadusta datasta tunnit, joissa on dataa
    hours_fetched = [i["hour"] for i in fetched_data]

    # Alustetaan new_data list ja index(käytetään returned_datan tiedon hakemisessa)
    data = []
    index = 0

    # Silmukoidaan vuorokauden tuntien verran
    for hour in range(24):

        # Jos tunti ei löydy saadusta listasta, luodaan nolla tietue.
        if hour not in hours_fetched:
            hourly_data = {"hour": hour, "total_kwh": 0}

        # Muussa tapauksessa listataan tietokannasta tullut datasta
        else:
            hourly_data = fetched_data[index]
            index += 1

        data.append(hourly_data)

    return data


# Nollatietueet lämpötilaan liittyville hourly by day hauille. Syötä queryssä
# saatu data. Datan pitää olla muotoa [{"hour": 0 "temperature": 0}]
def generate_zero_for_missing_hours_in_day_for_temperature_query(fetched_data):
    # Haetaan tietokannasta saadusta datasta tunnit, joissa on dataa
    hours_fetched = [i["hour"] for i in fetched_data]

    # Alustetaan new_data list ja index(käytetään returned_datan tiedon hakemisessa)
    data = []
    index = 0

    # Silmukoidaan vuorokauden tuntien verran
    for hour in range(24):

        # Jos tunti ei löydy saadusta listasta, luodaan nolla tietue.
        if hour not in hours_fetched:
            hourly_data = {"hour": hour, "temperature": 0}

        # Muussa tapauksessa listataan tietokannasta tullut datasta
        else:
            hourly_data = fetched_data[index]
            index += 1

        data.append(hourly_data)

    return data

