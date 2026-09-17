import esphome.codegen as cg
import esphome.config_validation as cv

from esphome import automation
from esphome.const import CONF_ID
from esphome.types import ConfigType

from .. import (
    CONF_SENDSPIN_ID,
    SendspinHub,
    request_visualizer_support,
    register_visualizer_config,
    sendspin_ns,
    CONF_RATE_MAX,
    CONF_N_DISP_BINS,
    CONF_SCALE,
    CONF_F_MIN,
    CONF_F_MAX,
    VISUALIZER_SCALE_MEL,
    VISUALIZER_SCALE_LOG,
    VISUALIZER_SCALE_LIN,
)

CODEOWNERS = ["@hufi008"]
DEPENDENCIES = ["sendspin"]

CONF_ON_SPECTRUM = "on_spectrum"
CONF_ON_PEAK = "on_peak"
CONF_ON_BEAT = "on_beat"
CONF_ON_F_PEAK = "on_f_peak"
CONF_ON_LOUDNESS = "on_loudness"

SendspinVisualizer = sendspin_ns.class_(
    "SendspinVisualizer",
    cg.Component,
    cg.Parented.template(SendspinHub),
)

_HUB_ID_SCHEMA = cv.Schema({
    cv.GenerateID(CONF_SENDSPIN_ID): cv.use_id(SendspinHub),
})

def _register(config: ConfigType) -> ConfigType:
    request_visualizer_support()
    register_visualizer_config(config)
    return config

CONFIG_SCHEMA = cv.All(
    cv.Schema({
        cv.GenerateID(): cv.declare_id(SendspinVisualizer),

        cv.Optional(CONF_RATE_MAX, default="10Hz"):
            cv.All(
                cv.frequency,
                cv.float_range(min=1.0, max=60.0),
            ),

        cv.Optional(CONF_N_DISP_BINS, default=10):
            cv.int_range(min=1, max=32),

        cv.Optional(CONF_SCALE, default="mel"): cv.enum(
            {
                "mel": VISUALIZER_SCALE_MEL,
                "log": VISUALIZER_SCALE_LOG,
                "lin": VISUALIZER_SCALE_LIN,
            },
            lower=True,
        ),

        cv.Optional(CONF_F_MIN, default=40):
            cv.int_range(min=1, max=65535),

        cv.Optional(CONF_F_MAX, default=16000):
            cv.int_range(min=1, max=65535),

        cv.Optional(CONF_ON_SPECTRUM):
            automation.validate_automation({}),

        cv.Optional(CONF_ON_PEAK):
            automation.validate_automation({}),

        cv.Optional(CONF_ON_BEAT):
            automation.validate_automation({}),

        cv.Optional(CONF_ON_F_PEAK):
            automation.validate_automation({}),

        cv.Optional(CONF_ON_LOUDNESS):
            automation.validate_automation({}),
    })
    .extend(_HUB_ID_SCHEMA)
    .extend(cv.COMPONENT_SCHEMA),
    cv.only_on_esp32,
    _register,
)


async def to_code(config: ConfigType) -> None:
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await cg.register_parented(var, config[CONF_SENDSPIN_ID])

    for conf in config.get(CONF_ON_SPECTRUM, []):
        await automation.build_callback_automation(
            var,
            "add_on_spectrum_callback",
            [(cg.std_vector.template(cg.uint16), "x")],
            conf,
        )
    for conf in config.get(CONF_ON_PEAK, []):
        await automation.build_callback_automation(
            var,
            "add_on_peak_callback",
            [(cg.uint8, "x")],
            conf,
        )
    for conf in config.get(CONF_ON_BEAT, []):
        await automation.build_callback_automation(
            var,
            "add_on_beat_callback",
            [(cg.bool_, "x")],
            conf,
        )
    for conf in config.get(CONF_ON_F_PEAK, []):
        await automation.build_callback_automation(
            var,
            "add_on_f_peak_callback",
            [(cg.uint16, "frequency_hz"), (cg.uint16, "amplitude"), ],
            conf,
        )
    for conf in config.get(CONF_ON_LOUDNESS, []):
        await automation.build_callback_automation(
            var,
            "add_on_loudness_callback",
            [(cg.uint16, "x")],
            conf,
        )