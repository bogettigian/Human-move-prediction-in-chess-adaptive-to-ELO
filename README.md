# Aligning Superhuman AI with Human Behavior

## How to build

After cloning the repository locally, don't forget to run the following commands in order to also clone the git submodules:
```
git submodule sync --recursive
git submodule update --recursive --init
```

It is necessary to install mongodb, to do so follow the steps of the official documentation \
https://www.mongodb.com/docs/manual/installation/

In order to build the tool, trainingdata-tool, on Ubuntu, run the following command:
```
cd libs/trainingdata-tool/
sudo apt-get install -y build-essential cmake libboost-all-dev
cmake .
cmake --build .
sudo chmod +x trainingdata-tool
cd ../../
```

## How to generate input files
```
cd src/
pip install -r ./../requirements.txt
python ingestion.py
python chunk_generator.py
cd ../
```

## How to train model
```
cd ../libs/lczero-training/
sudo apt-get install protobuf-compiler
bash init.sh
cd tf/
python ./train.py --cfg configs/example.yaml --output /tmp/mymodel.txt
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