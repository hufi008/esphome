import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.const import CONF_ID

generic_image_ns = cg.esphome_ns.namespace("generic_image")
GenericImage = generic_image_ns.class_("GenericImage", cg.Component)

MULTI_CONF = True
CONFIG_SCHEMA = cv.Schema({
    cv.GenerateID(): cv.declare_id(GenericImage),
}).extend(cv.COMPONENT_SCHEMA)

async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
