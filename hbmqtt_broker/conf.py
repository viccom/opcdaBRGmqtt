
broker_config = {
    "listeners": {
        "default": {
            "max-connections": 1024,
            "type": "tcp"
        },
        # "my-tcp-ssl-1": {
        #     "bind": "127.0.0.1:6883",
        #     "ssl": "on",
        #     "cafile": "KeyManager Test RSA CA_chain.crt",
        #     "certfile": "localhost_chain.crt",
        #     "keyfile": "localhost_key.key"
        # },
        # "my-ws-ssl-1": {
        #     "bind": "127.0.0.1:6884",
        #     "type": "ws",
        #     "ssl": "on",
        #     "cafile": "KeyManager Test RSA CA_chain.crt",
        #     "certfile": "localhost_chain.crt",
        #     "keyfile": "localhost_key.key"
        # },
        "my-tcp-1": {
            "bind": "0.0.0.0:3883"
        },
        "my-ws-1": {
            "bind": "0.0.0.0:3884",
            "type": "ws"
        }
    },
    "timeout-disconnect-delay": 2,
    "auth": {
        "plugins": ["auth_anonymous"],
        "allow-anonymous": True,
        "password-file": "admin/static/userpwd"
    },
    "topic-check": {
        "enabled": True,
        "plugins": ["topic_taboo"]
    }
}

MQTT_PROT = 3883
MQTT_WS_PORT = 3884