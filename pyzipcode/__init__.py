from __future__ import absolute_import
import time
import logging

import pandas as pd
import us
from sqlalchemy import create_engine
import sqlalchemy.exc as exceptions

from . import settings


logger = logging.getLogger(__name__)


class ConnectionManager(object):
    """
    Assumes a database that will work with cursor objects
    """

    def __init__(self, engine=None):
        # test out the connection...
        if engine is None:
            self.engine = create_engine(settings.url)
        else:
            self.engine = engine
        with self.engine.connect() as conn:
            pass

    def query(self, sql):
        conn = None
        retry_count = 0
        while not conn and retry_count <= 10:
            # If there is trouble reading the file, retry for 10 attempts
            # then just give up...
            try:
                if self.engine is None or retry_count >= 5:
                    engine = self.engine
                else:
                    engine = create_engine(settings.url)
                with engine.connect() as conn:
                    break
            except exceptions.OperationalError:
                retry_count += 1
                time.sleep(0.001)

        if not conn and retry_count > 10:
            raise exceptions.OperationalError("Can't connect to postgres db.")
        conn = engine.raw_connection()
        cur = conn.cursor()
        cur.execute(sql)
        results = cur.fetchall()
        cur.close()
        return results


class ZipCode(object):
    def __init__(self, row):
        self.zip = row['zipcode']
        self.county = row['county']
        self.county_fips = row['countyfips']
        self.city = row['city']
        self.state = row['state']
        self.state_full_name = row['statefullname']
        self.longitude = row['longitude']
        self.latitude = row['latitude']
        self.area_code = row['areacode']
        self.population = row['population']
        self.row = row


class ZipNotFoundException(Exception):
    pass


class ZipCodeDatabase(object):

    def __init__(self, conn=None):
        conn = ConnectionManager(conn)
        self.engine = conn.engine
        self.table = settings.table

    def format_result(self, query):
        zips = pd.read_sql(sql=query, con=self.engine)
        if len(zips) > 0:
            return [ZipCode(_zip) for index, _zip in zips.iterrows()]
        else:
            return None

    def get(self, _zip):
        if len(_zip) > 5:
            _zip = _zip[:5]
        _zip = str(_zip).zfill(5)
        zip_query = """SELECT * FROM {table} WHERE zipcode='{zipcode}'
                    """.format(table=self.table, zipcode=_zip)
        return self.format_result(zip_query)

    def find_zip(self, city=None, state=None):

        if city is None:
            city = "%"
        else:
            city = city.upper()

        if state is None:
            state = "%"
        elif len(state) > 2:
            states = us.states.mapping('name', 'abbr')
            try:
                state = states[state.title()]
            except:
                logger.info('Input state does not exist!')
                if city == '%':
                    raise Exception('No city input either, quittin!')
            state = state.upper()
        zip_find_query = """SELECT * FROM {table} WHERE
                            city LIKE '{city}'
                        AND state LIKE '{state}'
                        """.format(table=self.table, city=city, state=state)
        return self.format_result(zip_find_query)

    def get_zipcodes_around_radius(self, _zip, radius):
        zips = self.get(_zip)
        zip_range_query = """SELECT * FROM %s WHERE
                                longitude >= %d AND longitude <= %d
                            AND latitude >= %d  AND latitude <= %d"""
        if zips is None:
            raise ZipNotFoundException("Could not find zip code")
        else:
            _zip = zips[0]

        radius = float(radius)

        long_range = (_zip.longitude - (radius / 69.0),
                      _zip.longitude + (radius / 69.0))
        lat_range = (_zip.latitude - (radius / 49.0),
                     _zip.latitude + (radius / 49.0))

        return self.format_result(zip_range_query % (
            self.table,
            long_range[0], long_range[1],
            lat_range[0], lat_range[1]
        ))

    def __getitem__(self, _zip):
        returned_zip = self.get(str(_zip))
        if returned_zip is None:
            raise IndexError("""Couldn't find zip - {zipcode}
                             """.format(zipcode=_zip))
        else:
            return returned_zip[0]
