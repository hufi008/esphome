import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor, time
from esphome.const import CONF_ID, CONF_TIME_ID, CONF_TYPE

CONF_FORMAT = "format"
CONF_SUN_ID = "sun_id"

# Registrierung unserer Custom-Komponente
my_sun_ns = cg.esphome_ns.namespace("my_sun")
MySunSensor = my_sun_ns.class_(
    "MySunSensor", text_sensor.TextSensor, cg.PollingComponent
)

# Registrierung der offiziellen Core-Sun Komponente für den ID-Typ
sun_ns = cg.esphome_ns.namespace("sun")
CoreSun = sun_ns.class_("Sun")

# Erlaubte Typen für sunrise / sunset
SunType = my_sun_ns.enum("SunType")
SUN_TYPES = {
    "sunrise": SunType.SUN_TYPE_SUNRISE,
    "sunset": SunType.SUN_TYPE_SUNSET,
}

CONFIG_SCHEMA = text_sensor.text_sensor_schema(MySunSensor).extend(
    {
        cv.Required(CONF_TYPE): cv.enum(SUN_TYPES, lower=True),
        cv.Optional(CONF_FORMAT, default="%H:%M"): cv.string,
        cv.GenerateID(CONF_TIME_ID): cv.use_id(time.RealTimeClock),
        cv.GenerateID(CONF_SUN_ID): cv.use_id(CoreSun), # KORREKTUR: CoreSun statt MockObj
    }
).extend(cv.polling_component_schema("60s"))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await text_sensor.register_text_sensor(var, config)
    
    cg.add(var.set_type(config[CONF_TYPE]))
    cg.add(var.set_format(config[CONF_FORMAT]))
    
    time_ = await cg.get_variable(config[CONF_TIME_ID])
    cg.add(var.set_time(time_))
    
    sun_ = await cg.get_variable(config[CONF_SUN_ID])
    cg.add(var.set_sun(sun_))
