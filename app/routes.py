from flask import Blueprint, jsonify
from influxdb_client import InfluxDBClient
from config import Config

bp = Blueprint("routes", __name__)

influx_client = InfluxDBClient(
                                url = Config.INFLUX_URL,
                                org = Config.INFLUX_ORG,
                                token = Config.INFLUX_TOKEN
                                )

query_api = influx_client.query_api()

@bp.route("/api/latest")
def latest():
