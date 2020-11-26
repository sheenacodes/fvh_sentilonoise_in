import connexion
import six

from swagger_server.models.sensors import Sensors  # noqa: E501
from swagger_server import util


def add_inventory(Sensors=None):  # noqa: E501
    """adds noise observations to UoP

    Adds an item to the system # noqa: E501

    :param Sensors: Observations from Sensors
    :type Sensors: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        Sensors = Sensors.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
