#!python
# coding=utf-8
from collections import namedtuple

from shapely.geometry import Point, LineString

from pocean.utils import (
    unique_justseen,
)

trajectory_meta = namedtuple('Trajectory', [
    'min_z',
    'max_z',
    'min_t',
    'max_t',
    'geometry'
])

trajectories_meta = namedtuple('TrajectoryCollection', [
    'min_z',
    'max_z',
    'min_t',
    'max_t',
    'trajectories'
])


def trajectory_calculated_metadata(df, geometries=True):
    trajectories = {}
    for tid, tgroup in df.groupby('trajectory'):
        tgroup = tgroup.sort_values('t')

        if geometries:
            null_coordinates = tgroup.x.isnull() | tgroup.y.isnull()
            coords = list(unique_justseen(zip(
                tgroup.loc[~null_coordinates, 'x'].tolist(),
                tgroup.loc[~null_coordinates, 'y'].tolist()
            )))
        else:
            # Calculate the geometry as the linestring between all of the profile points
            first_row = tgroup.iloc[0]
            coords = [(first_row.x, first_row.y)]

        geometry = None
        if len(coords) > 1:
            geometry = LineString(coords)
        elif len(coords) == 1:
            geometry = Point(coords[0])

        trajectories[tid] = trajectory_meta(
            min_z=tgroup.z.min(),
            max_z=tgroup.z.max(),
            min_t=tgroup.t.min(),
            max_t=tgroup.t.max(),
            geometry=geometry
        )

    return trajectories_meta(
        min_z=df.z.min(),
        max_z=df.z.max(),
        min_t=df.t.min(),
        max_t=df.t.max(),
        trajectories=trajectories
    )