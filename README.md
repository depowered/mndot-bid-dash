# Frontend for [mndotbidprices.com](https://mndotbidprices.com)
A Dash-Plotly web application that displays data from the [depowered/mndot-bid-api](https://github.com/depowered/mndot-bid-api) backend.

## Serve Application
```
$ gunicorn --workers=2 --bind=0.0.0.0:8050 main:server
```
