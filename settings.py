import logging

logging.basicConfig(
    filename='log.log',
    filemode='a',
    level=logging.DEBUG,
    # format='[%(levelname)s %(asctime)s %(module)s:%(lineno)d] %(message)s',
)
logger = logging.getLogger(__name__)


DATA_PATH = "data/"
# FIXED_FILE_NAME = f"{DATA_PATH}fixed.csv"
# ERROR_FILE_NAME = f"{DATA_PATH}corrupt_data.csv"
DEFUALT_DATA_FILE = f"{DATA_PATH}oddetect.csv"
DEFUALT_IMAGE_FILE = f"paths0.png"
# FIXED_FILE_NAME_PICKLE = f"{DATA_PATH}paths.pkl.xz"


GENERAL_SETTINGS = dict({'hard_reload_data_files': False,
                            'auto_load_path_by_path': True,
                            'num_of_blocks_in_image': 10,
                            'path_by_path_limit': 20,
                            'start_draw_heatmap_limit': 200})