# Assignment

Tehnicna naloga

## Questions
1. Kakšen bandwidth mora sistem imeti, da lahko podpira procesiranje takšnega števila
obdelav na sekundo?
Bandwith je definiran kakor bits per second, imamo 1000 dokumentov na sekundo vsak po 1MB (1 MB = 8 Mbit), 8000 Mbps, kar je 8 Gbps

2. Kako velik storage je potreben za shranjevanje dokumentov enega meseca?
Mesec z 31 dnevi ima 2,678,400 sekund. Nas najvecji dokument, ker so stevilke dokumenta fixne je lahko velik 117 bajtov. Tako da porabimo 2,678,400,000 bajtov ali ~2.6784 Gb, potem je tu treba upostevati se velikost indexov

## Usage

Sistem lahko skoraj vzpostavimo preko docker compose. Servisa za kreiranje dokumentov in sporocanje ne delata preko composa, tako, da jih je treba zagnati rocno.
Prav tako, pa je potrebno preko minio console (http://localhost:9090) ustvariti ampq notification:
```code
URL amqp://guest:guest@rabbitmq:5672
Exchange: bucket-events
Exchange Type: direct
Durable: ON
```

ko ustvarimo notification, moramo restartati minio, to lahko naredimo preko prompta, ki se pojavi na konzoli.
Nato je potrebno ustvariti bucket in v bucket managementu subscribat na event, kjes se v ARN dropdownu zbere minio sqs in izberemo event type put.

## Skica
![Alt text](./skica.png)

## Shema
Uporabil sem mongodb, shema je:
```code
_id: auto generated unique identifier
identifier: str (stevilka dokumenta)
type: str (tip dokumenta)
datetime: datetime (datum dokumenta)
```

Indeksov nisem kreiral, ker se na mongodb ne spoznam najbolje in ne vem kako bi indexi vplivali na write performance ali na kolicino zasedenga rama/diska
Drugace bi pa indeksi morali biti nekako tako:
```code
index (identifier, type, datetime)
index (type, datetime)
index (datetime)
```

tako bi se pokrilo vse mozne kombinacije, ker v mongo db, se lahko uporabi recimo prvi index v kombinacijah: {identifier, type, datetime}, {identifier, type}, {identifier}
