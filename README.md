# hexi
Motion Cueing Framework

## Setup

```bash
python3 -m pip install -r requirements.txt
```

## Getting Started

```bash
python3 -m hexi.server
```


## Plugin Development

### User Interface

To build the user interface of your plugin:

```bash
npm run build:plugin -- --env.pluginName PLUGIN_NAME
```

Optionally, you can add additional option `--watch` to watch modifications.

## Hexi Development

```bash
npm run build:coreDll
npm run build:core -- --watch
```

