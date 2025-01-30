import Agently
import utils.yaml_reader as yaml
from utils.logger import Logger
from workflows import main_workflow
from utils.path import root_path

# Settings and Logger
SETTINGS = yaml.read("./SETTINGS.yaml")
logger = Logger(console_level = "DEBUG" if SETTINGS.IS_DEBUG else "INFO")

# Proxy
model_proxy = (
    SETTINGS.MODEL_PROXY
    if hasattr(SETTINGS, "MODEL_PROXY")
    else
    (
        SETTINGS.PROXY
        if hasattr(SETTINGS, "PROXY")
        else None
    ) 
)

# Agent Factory
agent_factory = (
    Agently.AgentFactory(is_debug=SETTINGS.IS_DEBUG)
        .set_settings("current_model", SETTINGS.MODEL_PROVIDER)
        .set_settings(f"model.{ SETTINGS.MODEL_PROVIDER }.auth", SETTINGS.MODEL_AUTH)
        .set_settings(f"model.{ SETTINGS.MODEL_PROVIDER }.url", SETTINGS.MODEL_URL if hasattr(SETTINGS, "MODEL_URL") else None)
        .set_settings(f"model.{ SETTINGS.MODEL_PROVIDER }.options", SETTINGS.MODEL_OPTIONS if hasattr(SETTINGS, "MODEL_OPTIONS") else {})
        .set_settings("proxy", model_proxy)
)

# Start Workflow
def start_workflow(topic):
    SETTINGS.USE_CUSTOMIZE_OUTLINE = False
    SETTINGS.CUSTOMIZE_OUTLINE = None
    main_workflow.start(
        agent_factory=agent_factory,
        SETTINGS=SETTINGS,
        root_path=root_path,
        logger=logger,
    )
    return "Workflow started"

iface = gr.Interface(
    fn=start_workflow,
    inputs=gr.inputs.Textbox(label="Topic"),
    outputs="text",
    title="Agently Daily News Collector"
)


if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=5000)

# To-do
# 0. Fork original project
# 1. Build docker container
# 2. Deploy it in webserver
# 3. Adjust the UI
# 4. AWS Lambda deployment
# (5. Pull request to contribute web deployment feature to original repository)