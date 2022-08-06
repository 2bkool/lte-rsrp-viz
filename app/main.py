from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import logging_
from app import db
from app.db import database
from app.config import EngineeringCenterProfile
from app.indoor.rsrp import RSRPMap
from app.indoor.signal import Signal, Status
from app.schemas import SignalResponse


app = FastAPI()
logger = logging_.get_logger(__name__)


app.mount('/static', StaticFiles(directory='app/static'), name='static')
templates = Jinja2Templates(directory='app/templates')


@app.get('/')
async def index():
    return EngineeringCenterProfile()


@app.get('/rescues/{rescue_code}')
async def rescue(request: Request, rescue_code: str):
    profile = EngineeringCenterProfile()
    for floor_no in profile.floors:
        rsrp_map = RSRPMap(profile, rescue_code, floor_no)

    return templates.TemplateResponse(
        'indoor.html',
        {'request': request,
         'rescue_code': rescue_code,
         'n_row': rsrp_map.matrix.shape[0],
         'n_col': rsrp_map.matrix.shape[1]})


@app.get('/rescues/{rescue_code}/floors/{floor_no}/data',
         response_model=SignalResponse)
async def get_data(rescue_code: str, floor_no: str):
    profile = EngineeringCenterProfile()
    _data = await db.get_data(rescue_code, floor_no)
    logger.debug(_data)

    if _data is None:
        return SignalResponse(status=Status.NO_SIGNAL)

    rsrp_map = RSRPMap(profile, rescue_code, floor_no)
    signal = Signal(profile, _data.lat, _data.lon, _data.alt)
    response = SignalResponse(row=signal.row, col=signal.col)

    try:
        row_, col_ = signal.adjust_position(rsrp_map.matrix)
    except IndexError:
        response.status = Status.OUT_OF_BOUNDS
    else:
        power = max(list(filter(None, [_data.power0, _data.power1])),
                    default=None)
        rsrp_map.update(row_, col_, power)
        response.row_ = row_
        response.col_ = col_

    try:
        signal_peak = Signal(profile, _data.lat_peak,
                             _data.lon_peak, _data.alt_peak)
        row_, col_ = signal_peak.adjust_position(rsrp_map.matrix)
    except (IndexError, ValueError) as e:
        logger.error(e)
        pass
    else:
        response.row_peak = row_
        response.col_peak = col_

    interpolated = rsrp_map.interpolate()

    response.lat = signal.lat
    response.lon = signal.lon
    response.matrix = interpolated.tolist()
    response.floor_peak = _data.floor_peak
    return response


@app.on_event('startup')
async def startup():
    await database.connect()


@app.on_event('shutdown')
async def shutdown():
    await database.disconnect()
