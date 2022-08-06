from urllib.parse import quote

# import sqlalchemy
import databases

from .config import settings


db_url = 'mysql+aiomysql://{}:{}@{}/{}'\
          .format(settings.db_user, quote(settings.db_password),
                  settings.db_host, settings.db_name)

database = databases.Database(db_url)
# engine = sqlalchemy.create_engine(DB_URL)


async def get_data(rescue_code, floor):
    q = """
        select
            rum.rum_code
            , rum.member_type
            , ml.latitude as lat
            , ml.longitude as lon
            , ml.altitude as alt
            , tgul_dmrs_ant0_rsrp as power0
            , tgul_dmrs_ant1_rsrp as power1
            , c.max_peak_floor as floor_peak
            , c.max_peak_latitude as lat_peak
            , c.max_peak_longitude as lon_peak
            , c.max_peak_altitude as alt_peak
            , if(c.max_peak_tgul_dmrs_ant0_rsrp > c.max_peak_tgul_dmrs_ant1_rsrp,
            c.max_peak_tgul_dmrs_ant0_rsrp, c.max_peak_tgul_dmrs_ant1_rsrp) as power_max
        from
            rescue_user_mapper rum
            , caller c
            , member_loc ml
        where 1=1
            and rum.rescue_code = c.rescue_code
            and rum.rum_code = ml.rum_code
            and rum.rescue_code = :rescue_code
            and ml.search_floor = :floor
            and ml.signal_capture_status = 1
        order by ml.id desc
        limit 1
    """
    return await database.fetch_one(query=q,
                                    values={'rescue_code': rescue_code,
                                            'floor': floor})
