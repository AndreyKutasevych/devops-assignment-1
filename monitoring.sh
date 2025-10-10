#!/usr/bin/bash
#
# Some basic monitoring functionality; Tested on Amazon Linux 2023.
#
echo "Monotoring start"
TOKEN=`curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600"`
INSTANCE_ID=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/instance-id)
INSTANCE_PUBLIC_IP=$(curl -s -H "X-aws-ec2-metadata-token: $TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4)
MEMORYUSAGE=$(free -m | awk 'NR==2{printf "%.2f%%", $3*100/$2 }')
PROCESSES=$(expr $(ps -A | grep -c .) - 1)
HTTPD_PROCESSES=$(ps -A | grep -c httpd)
REGUESTS_304=$(sudo grep " 304 " /var/log/httpd/access_log | wc -l)
REGUESTS_200=$(sudo grep " 200 " /var/log/httpd/access_log | wc -l)


echo "Instance ID: $INSTANCE_ID"
echo "Memory utilisation: $MEMORYUSAGE"
echo "No of processes: $PROCESSES"
echo "Public IP address: $INSTANCE_PUBLIC_IP"
echo "-------"
echo "Error log entries: $(sudo grep -i "error" /var/log/httpd/error_log | wc -l)"
echo "-------"
echo "Total accesses: $(sudo wc -l /var/log/httpd/access_log | awk '{print $1}')"
echo "-------"
echo "404 errors: $(sudo grep " 404 " /var/log/httpd/access_log | wc -l)"
echo "-------"
echo "Successful requests: $((REGUESTS_200+REGUESTS_304))"
echo "Last 5 accesses:"
sudo tail -5 /var/log/httpd/access_log | awk '{print $1, $7, $9}'

if [ $HTTPD_PROCESSES -ge 1 ]
then
    echo "Web server is running"
else
    echo "Web server is NOT running"
fi
echo "Monitoring script execution finished"
