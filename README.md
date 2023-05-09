# Aligning Superhuman AI with Human Behavior

## How to start

After cloning the repository locally, don't forget to run the following commands in order to also clone the git submodules:
```
git submodule sync --recursive
git submodule update --recursive --init
```

It is necessary to install mongodb, to do so follow the steps of the official documentation \
https://www.mongodb.com/docs/manual/installation/

## How to build libraries

In order to build trainingdata-tool, on Ubuntu, run the following command:
```
cd libs/trainingdata-tool/
sudo apt-get install -y build-essential cmake libboost-all-dev
cmake .
cmake --build .
sudo chmod +x trainingdata-tool
cd ../../
```

In order to build lczero-training, on Ubuntu, run the following command:
```
cd libs/lczero-training/
sudo apt-get install -y protobuf-compiler
# (sudo chmod +x init.sh)
bash init.sh
cd ../../
```

## How to generate input files
```
cd src/
pip install -r ./../requirements.txt
python ingestion.py
python pgn_generator.py
python chunk_generator.py
cd ../
```

## How to train model
```
cd libs/lczero-training/tf/
mkdir ./../../../data/network
mkdir ./../../../data/model
python ./train.py --cfg configs/example.yaml --output ./../../../data/model/mymodel.txt
```

## References

### Paper:
https://arxiv.org/pdf/2006.01855.pdf

### Blogs:
http://csslab.cs.toronto.edu/blog/2020/08/24/maia_chess_kdd/ \
https://www.microsoft.com/en-us/research/blog/the-human-side-of-ai-for-chess/

### Maia:
https://maiachess.com/ \
https://github.com/CSSLab/maia-chess \
http://csslab.cs.toronto.edu/datasets/#maia_kdd

### Liches database:
https://database.lichess.org/