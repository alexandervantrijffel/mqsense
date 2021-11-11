if ! type mosquitto_passwd 1>/dev/null; then
  echo "mosquitto_passwd is missing. Install with: sudo apt-get install mosquitto"
  exit 1
fi

cp -r mosquitto/data-mosquitto/passwords-unencrypted mosquitto/data-mosquitto/passwords
mosquitto_passwd -U mosquitto/data-mosquitto/passwords
