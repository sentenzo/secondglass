
```mermaid
stateDiagram-v2

[*] --> IDLE
IDLE --> TICKING: start
TICKING --> IDLE: stop
TICKING --> IDLE: restart
TICKING --> PAUSED: pause
TICKING --> TICKING: tick
TICKING --> RANG: tick
PAUSED --> IDLE: stop
PAUSED --> TICKING: restart
PAUSED --> TICKING: resume
RANG --> RANG: tick
RANG --> TICKING: restart
RANG --> IDLE: stop
IDLE --> [*]
TICKING --> [*]
PAUSED --> [*]
RANG --> [*]

```

```mermaid
flowchart TB

A((IDLE)) -->|start| B((TICKING))
B ==>|stop| A
B ==>|restart| A
B ==>|tick| B
B ==>|pause| C((PAUSED))
B ==>|tick|D((RANG))
C ==>|stop| A
C ==>|restart| B
C ==>|resume| B
D ==>|stop| A
D ==>|restart| B
D ==>|tick|D
```

| State     | Actions available                           |
| --------- | ------------------------------------------- |
| `IDLE`    | `start`, `close`                            |
| `TICKING` | `tick`, `pause`, `stop`, `restart`, `close` |
| `PAUSED`  | `resume`, `stop`, `restart`, `close`        |
| `RANG`    | `tick`, `stop`, `restart`, `close`          |





