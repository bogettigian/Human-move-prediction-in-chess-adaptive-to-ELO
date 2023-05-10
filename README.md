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
sudo apt-get install -y build-essential cmake libboost-all-dev
```
For Windows, follow the instructions:
- Download MinGW from https://winlibs.com/#download-release and add it to environment variables
- Download libboost from https://www.boost.org/users/download/ and move it to MinGW/include/boost folder
- You probably have to comment out line 76 of the libs/trainingdata-tool/polyglot/src/getopt.h

Then run the following commands
```
cd libs/trainingdata-tool/
cmake .
cmake --build .
sudo chmod +x trainingdata-tool
cd ../../
```
and add trainingdata-tool to the path.

In order to build lczero-training, on Ubuntu, run the following command:
```
sudo apt-get install -y protobuf-compiler
```
For Windows, follow the instructions:
- Download protoc from https://github.com/protocolbuffers/protobuf/releases and add it to environment variables

Then run the following commands
```
cd libs/lczero-training/
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