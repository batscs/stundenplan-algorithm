:: Powershell single line cmd alternative:
:: $env:COMMAND="-s -g 10 -w -d -t"; docker-compose up -d

set COMMAND=-s -g 200 -w -t
docker-compose up
