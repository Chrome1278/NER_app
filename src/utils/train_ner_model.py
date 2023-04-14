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
    Path("./src/models/model_ner"),  # trained model
    overrides={"paths.train": "./data/annotations/labelled_annotations.spacy"},
)

end = time.time() - start
print(f"\nLearning time: {end}")
