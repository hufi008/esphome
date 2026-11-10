import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c
from esphome.const import CONF_ID

DEPENDENCIES = ["i2c"]

cfs_rfid_ns = cg.esphome_ns.namespace("cfs_rfid")
CFSRfidComponent = cfs_rfid_ns.class_("CFSRfidComponent", cg.PollingComponent, i2c.I2CDevice)

CONFIG_SCHEMA = (
    cv.Schema({
        cv.Required(CONF_ID): cv.declare_id(CFSRfidComponent),
    })
    .extend(cv.polling_component_schema("2s"))
    .extend(i2c.i2c_device_schema(0x24))
)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)
