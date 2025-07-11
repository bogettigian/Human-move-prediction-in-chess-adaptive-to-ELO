# Human move prediction in chess adaptive to ELO

## How to start

After cloning the repository locally, don't forget to run the following commands in order to also clone the git submodules:
```
git submodule sync --recursive
git submodule update --recursive --init

pip install -r requirements.txt
```

### MongoDB

It is necessary to install mongodb, to do so follow the steps of the official documentation \
https://www.mongodb.com/docs/manual/installation/

### CUDA Toolkit
The project is designed to work with GPU, for that it is required to install CUDA Toolkit, and to do so follow the instructions in these pages: \
https://developer.nvidia.com/cuda-toolkit \
https://developer.nvidia.com/cudnn \
https://www.tensorflow.org/install/source

## How to build libraries

### trainingdata-tool
In order to build trainingdata-tool, on Ubuntu, run the following command:
```
sudo apt-get install -y build-essential cmake libboost-all-dev
```
For Windows, follow the instructions:
- Download libboost from https://www.boost.org/users/download/ 
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

### lczero-training
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

### lc0
In order to build lc0, on Ubuntu, run the following command:
```
cd libs/trainingdata-tool/lc0/
CC=gcc-10 CXX=g++-10 ./build.sh
cd ../../../
```
For Windows, follow the instructions from cmd:
```
cd libs/trainingdata-tool/lc0/
build-cuda.cmd
cd ../../../
```

## How to generate input files
```
cd src/
python pgn_ingestion.py
python pgn_generator.py
python chunk_generator.py
cd ../
```

## How to train model
```
cd libs/lczero-training/tf/
mkdir ./../../../data/network
mkdir ./../../../data/model
python ./train.py --cfg configs/example.yaml --output ./../../../data/model/mymodel.pb.gz
cd ./../../../
```

## How to Run model
```
./libs/trainingdata-tool/lc0/build/lc0 --weights=./data/model/mymodel.pb.gz --elo=1000
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