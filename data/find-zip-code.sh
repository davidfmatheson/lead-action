#!/bin/bash

if [[ $# -eq 0 ]]; then
	address="$(pbpaste)"
else
	address="$1"
fi

city=Providence
state=RI
echo $address, $city, $state
curl -s 'https://tools.usps.com/tools/app/ziplookup/zipByAddress' --data "companyName=&address1=$address&city=$city&state=$state" -H "User-Agent: Mozilla/5.0" | jq -r '.addressList[].zip5' | sort -u
# curl -s 'https://tools.usps.com/tools/app/ziplookup/zipByAddress' --data "companyName=&address1=$address&city=$city&state=$state" -H "User-Agent: Mozilla/5.0" | jq 
