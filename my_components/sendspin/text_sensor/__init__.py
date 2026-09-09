import esphome.codegen as cg
from esphome.components import text_sensor
import esphome.config_validation as cv
from esphome.const import CONF_ID, CONF_TYPE
from esphome.types import ConfigType

from .. import CONF_SENDSPIN_ID, SendspinHub, request_metadata_support, request_color_support, sendspin_ns

CODEOWNERS = ["@kahrendt"]
DEPENDENCIES = ["sendspin"]

SendspinTextSensor = sendspin_ns.class_(
    "SendspinTextSensor",
    text_sensor.TextSensor,
    cg.Component,
)

# Hufi
SendspinTextTypes = sendspin_ns.enum("SendspinTextTypes", is_class=True)
SENDSPIN_TEXT_TYPES = {
    "title": SendspinTextTypes.TITLE,
    "artist": SendspinTextTypes.ARTIST,
    "album": SendspinTextTypes.ALBUM,
    "album_artist": SendspinTextTypes.ALBUM_ARTIST,
    "primary": SendspinTextTypes.PRIMARY,
    "accent": SendspinTextTypes.ACCENT,
    "background_dark": SendspinTextTypes.BACKGROUND_DARK,
    "background_light": SendspinTextTypes.BACKGROUND_LIGHT,
    "on_dark": SendspinTextTypes.ON_DARK,
    "on_light": SendspinTextTypes.ON_LIGHT,
}
# ifuH

def _request_roles(config: ConfigType) -> ConfigType:
    """Request the necessary Sendspin roles for the text sensor."""
    # Hufi
    if config[CONF_TYPE] in (
        SendspinTextTypes.TITLE,
        SendspinTextTypes.ARTIST,
        SendspinTextTypes.ALBUM,
        SendspinTextTypes.ALBUM_ARTIST,
    ):
        request_metadata_support()

    if config[CONF_TYPE] in (
        SendspinTextTypes.PRIMARY,
        SendspinTextTypes.ACCENT,
        SendspinTextTypes.BACKGROUND_DARK,
        SendspinTextTypes.BACKGROUND_LIGHT,
        SendspinTextTypes.ON_DARK,
        SendspinTextTypes.ON_LIGHT,
    ):
        request_color_support()
    # ifuH

    return config

CONFIG_SCHEMA = cv.All(
    text_sensor.text_sensor_schema().extend(
        {
            cv.GenerateID(): cv.declare_id(SendspinTextSensor),
            cv.GenerateID(CONF_SENDSPIN_ID): cv.use_id(SendspinHub),
            cv.Required(CONF_TYPE): cv.enum(SENDSPIN_TEXT_TYPES),
        }
    ),
    cv.only_on_esp32,
    _request_roles,
)


async def to_code(config: ConfigType) -> None:
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await cg.register_parented(var, config[CONF_SENDSPIN_ID])
    await text_sensor.register_text_sensor(var, config)

    # Hufi
    cg.add(var.set_type(config[CONF_TYPE]))
    # ifuH