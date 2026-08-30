import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import text_sensor, time
from esphome.const import CONF_ID, CONF_TIME_ID

# Namespace und Klasse definieren
my_moon_ns = cg.esphome_ns.namespace("my_moon")
MoonSensor = my_moon_ns.class_(
    "MoonSensor", text_sensor.TextSensor, cg.PollingComponent
)

# Sucht automatisch nach der aktiven RealTimeClock
CONFIG_SCHEMA = text_sensor.text_sensor_schema(MoonSensor).extend(
    {
        cv.GenerateID(CONF_TIME_ID): cv.use_id(time.RealTimeClock),
    }
).extend(cv.polling_component_schema("60s"))

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await text_sensor.register_text_sensor(var, config)
    
    # Übergibt die gefundene Zeitkomponente an den C++ Setter
    time_ = await cg.get_variable(config[CONF_TIME_ID])
    cg.add(var.set_time(time_))
