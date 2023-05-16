import time

from pathlib import Path
from spacy.cli.init_config import fill_config
from spacy.cli.train import train
import spacy_transformers

# download('ru_core_news_md')

print('Initialization config')
fill_config(Path("./src/configs/config.cfg"), Path("./src/configs/base_config.cfg"))
print('Initialization is complete!\n')
start = time.time()

train(

    Path("./src/configs/config.cfg"),
    Path("./src/models/model_ner_large_5k"),  # trained model
    # overrides={"paths.train": "./data/annotations/labelled_annotations.spacy"},
    # use_gpu=0
)

end = time.time() - start
print(f"\nLearning time: {end}")

# best ~ 0.8
