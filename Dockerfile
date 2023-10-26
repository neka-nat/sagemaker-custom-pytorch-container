FROM pytorch/pytorch:2.1.0-cuda12.1-cudnn8-devel

RUN pip install --upgrade pip

RUN pip install torchvision

COPY train main_mnist.py /opt/ml/code/

RUN chmod +x /opt/ml/code/train

ENV PATH=$PATH:/opt/ml/code
