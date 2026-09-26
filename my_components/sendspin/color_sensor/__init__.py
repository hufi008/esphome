import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import automation

from esphome.const import CONF_ID
from esphome.types import ConfigType

from .. import (
    CONF_SENDSPIN_ID,
    SendspinHub,
    request_color_support,
    sendspin_ns,
)

CODEOWNERS = ["@hufi008"]
DEPENDENCIES = ["sendspin"]

CONF_TYPE = "type"
CONF_ON_COLOR = "on_color"  # Hufi
CONF_ON_CLEAR = "on_clear"  # Hufi

SendspinColorSensor = sendspin_ns.class_(
    "SendspinColorSensor",
    cg.Component,
)

# Hufi
SendspinColorTypes = sendspin_ns.enum("SendspinColorTypes", is_class=True)
SENDSPIN_COLOR_TYPES = {
    "primary": SendspinColorTypes.PRIMARY,
    "accent": SendspinColorTypes.ACCENT,
    "background_dark": SendspinColorTypes.BACKGROUND_DARK,
    "background_light": SendspinColorTypes.BACKGROUND_LIGHT,
    "on_dark": SendspinColorTypes.ON_DARK,
    "on_light": SendspinColorTypes.ON_LIGHT,
}
# ifuH

Color = cg.global_ns.class_("Color")

_HUB_ID_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_SENDSPIN_ID): cv.use_id(SendspinHub),
})


def _request_color(config: ConfigType) -> ConfigType:
    request_color_support()
    return config


CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(SendspinColorSensor),
        cv.Required(CONF_TYPE): cv.enum(SENDSPIN_COLOR_TYPES),
        cv.Optional(CONF_ON_COLOR): automation.validate_automation({}),  # Hufi
        cv.Optional(CONF_ON_CLEAR): automation.validate_automation({}),  # Hufi
    })
    .extend(_HUB_ID_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA),
    cv.only_on_esp32,
    _request_color,
)


async def to_code(config: ConfigType) -> None:
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await cg.register_parented(var, config[CONF_SENDSPIN_ID])

    # Hufi
    cg.add(var.set_type(config[CONF_TYPE]))

    for conf in config.get(CONF_ON_COLOR, []):
        await automation.build_callback_automation(
            var,
            "add_on_color_callback",
            [(Color, "x")],
            conf,
        )

    for conf in config.get(CONF_ON_CLEAR, []):
        await automation.build_callback_automation(
            var,
            "add_on_clear_callback",
            [],
            conf,
        )
    # ifuH