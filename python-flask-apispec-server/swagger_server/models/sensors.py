# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Sensors(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, sensors: List[Sensor]=None):  # noqa: E501
        """Sensors - a model defined in Swagger

        :param sensors: The sensors of this Sensors.  # noqa: E501
        :type sensors: List[Sensor]
        """
        self.swagger_types = {
            'sensors': List[Sensor]
        }

        self.attribute_map = {
            'sensors': 'sensors'
        }

        self._sensors = sensors

    @classmethod
    def from_dict(cls, dikt) -> 'Sensors':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Sensors of this Sensors.  # noqa: E501
        :rtype: Sensors
        """
        return util.deserialize_model(dikt, cls)

    @property
    def sensors(self) -> List[Sensor]:
        """Gets the sensors of this Sensors.


        :return: The sensors of this Sensors.
        :rtype: List[Sensor]
        """
        return self._sensors

    @sensors.setter
    def sensors(self, sensors: List[Sensor]):
        """Sets the sensors of this Sensors.


        :param sensors: The sensors of this Sensors.
        :type sensors: List[Sensor]
        """
        if sensors is None:
            raise ValueError("Invalid value for `sensors`, must not be `None`")  # noqa: E501

        self._sensors = sensors
