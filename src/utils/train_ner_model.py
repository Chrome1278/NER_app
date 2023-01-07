import time

from pathlib import Path
from spacy.cli.init_config import fill_config
from spacy.cli.train import train

# download('ru_core_news_md')

print('Initialization config')
fill_config(Path("./src/configs/config.cfg"), Path("./src/configs/base_config.cfg"))
print('Initialization is complete!\n')
start = time.time()

train(
    Path("./src/configs/config.cfg"),
    Path("./src/models/tuning_models_news"),  # tuning_models
    overrides={"paths.train": "./data/annotations/annotations_new_data.spacy"}  # annotations_data.spacy
)

end = time.time() - start
print(f"\nLearning time: {end}")
