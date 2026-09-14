import esphome.codegen as cg
from esphome.components import sensor
import esphome.config_validation as cv
from esphome.const import (
    CONF_ID,
    CONF_TYPE,
    CONF_YEAR,
    STATE_CLASS_MEASUREMENT,
    UNIT_MILLISECOND,
)
from esphome.types import ConfigType
from esphome import automation

from .. import (
    CONF_SENDSPIN_ID,
    SendspinHub,
    request_metadata_support,
    request_visualizer_support,
    register_visualizer_config,
    sendspin_ns,
    VisualizerDataType,
    VISUALIZER_DATA_SPECTRUM,
    CONF_RATE_MAX,
    CONF_N_DISP_BINS,
    CONF_SCALE,
    VISUALIZER_SCALE_MEL,
    VISUALIZER_SCALE_LOG,
    VISUALIZER_SCALE_LIN,
    CONF_F_MIN,
    CONF_F_MAX,
)

CODEOWNERS = ["@kahrendt"]
DEPENDENCIES = ["sendspin"]

CONF_TRACK = "track"
CONF_TRACK_PROGRESS = "track_progress"
CONF_TRACK_DURATION = "track_duration"
# Hufi
CONF_SPECTRUM = "spectrum"
CONF_ON_SPECTRUM = "on_spectrum"
# ifuH

SendspinTrackProgressSensor = sendspin_ns.class_(
    "SendspinTrackProgressSensor",
    sensor.Sensor,
    cg.PollingComponent,
)
SendspinMetadataSensor = sendspin_ns.class_(
    "SendspinMetadataSensor",
    sensor.Sensor,
    cg.Component,
)

SendspinNumericMetadataTypes = sendspin_ns.enum(
    "SendspinNumericMetadataTypes", is_class=True
)
_METADATA_TYPE_ENUM = {
    CONF_TRACK_DURATION: SendspinNumericMetadataTypes.TRACK_DURATION,
    CONF_YEAR: SendspinNumericMetadataTypes.YEAR,
    CONF_TRACK: SendspinNumericMetadataTypes.TRACK,
}

# Hufi
SendspinSpectrum = sendspin_ns.class_(
    "SendspinSpectrum",
    cg.Component,
)
# ifuH


# Hufi
def _request_roles(config: ConfigType) -> ConfigType:
    """Request the necessary Sendspin roles for the sensor."""
    if config[CONF_TYPE] == CONF_SPECTRUM:
        request_visualizer_support()
    else:
        request_metadata_support()
    return config
# ifuH

_HUB_ID_SCHEMA = cv.Schema({cv.GenerateID(CONF_SENDSPIN_ID): cv.use_id(SendspinHub)})


def _metadata_schema(**sensor_kwargs):
    """Schema for event-driven numeric metadata sensors (duration/year/track)."""
    return (
        sensor.sensor_schema(
            SendspinMetadataSensor,
            accuracy_decimals=0,
            **sensor_kwargs,
        )
        .extend(_HUB_ID_SCHEMA)
        .extend(cv.COMPONENT_SCHEMA)
    )

# Hufi
def _register(config: ConfigType) -> ConfigType:
    if config[CONF_TYPE] == CONF_SPECTRUM:
        register_visualizer_config(config)
    else:
        request_metadata_support()
    return config
# ifuH

CONFIG_SCHEMA = cv.All(
    cv.typed_schema(
        {
            CONF_TRACK_PROGRESS: sensor.sensor_schema(
                SendspinTrackProgressSensor,
                accuracy_decimals=0,
                state_class=STATE_CLASS_MEASUREMENT,
                unit_of_measurement=UNIT_MILLISECOND,
            )
            .extend(_HUB_ID_SCHEMA)
            .extend(cv.polling_component_schema("1s")),
            CONF_TRACK_DURATION: _metadata_schema(
                state_class=STATE_CLASS_MEASUREMENT,
                unit_of_measurement=UNIT_MILLISECOND,
            ),
            CONF_YEAR: _metadata_schema(),
            CONF_TRACK: _metadata_schema(),
            # Hufi
            CONF_SPECTRUM: cv.Schema({
                cv.GenerateID(): cv.declare_id(SendspinSpectrum),
                cv.Optional(CONF_RATE_MAX, default="10Hz"): cv.All(cv.frequency, cv.float_range(min=1.0, max=60.0)),
                cv.Optional(CONF_N_DISP_BINS, default=32): cv.int_range(min=1, max=255),
                cv.Optional(CONF_SCALE, default="mel"): cv.enum(
                    {
                        "mel": VISUALIZER_SCALE_MEL,
                        "log": VISUALIZER_SCALE_LOG,
                        "lin": VISUALIZER_SCALE_LIN,
                    },
                    lower=True),
                cv.Optional(CONF_F_MIN, default=40): cv.int_range(min=1, max=65535),
                cv.Optional(CONF_F_MAX, default=16000): cv.int_range(min=1, max=65535),
                cv.Optional(CONF_ON_SPECTRUM): automation.validate_automation({}),
            }).extend(_HUB_ID_SCHEMA).extend(cv.COMPONENT_SCHEMA),
            # ifuH
        },
        key=CONF_TYPE,
    ),
    cv.only_on_esp32,
    _register,
)


# Hufi
async def to_code(config: ConfigType) -> None:
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await cg.register_parented(var, config[CONF_SENDSPIN_ID])

    if config[CONF_TYPE] != CONF_SPECTRUM:
        await sensor.register_sensor(var, config)
    if config[CONF_TYPE] == CONF_SPECTRUM:
        parent = await cg.get_variable(config[CONF_SENDSPIN_ID])

        for conf in config.get(CONF_ON_SPECTRUM, []):
            await automation.build_callback_automation(
                var,
                "add_on_spectrum_callback",
                [(cg.std_vector.template(cg.uint16), "x")],
                conf,
            )
            
    if (metadata_type := _METADATA_TYPE_ENUM.get(config[CONF_TYPE])) is not None:
        cg.add(var.set_metadata_type(metadata_type))
# ifuH
