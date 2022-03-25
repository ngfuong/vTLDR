# vTLDR

Using PhoBERT pretrain, vTLDR provides a seq2seq model that performs the mini downstream task of Vietnamese news summarization.
A GUI for users to input plain text or news URL (only supports _tuoitre.vn_ domain at the moment) and output respective summary.

Notebook train_test_infer guide: [Colab](https://drive.google.com/file/d/1D6GyXRPnCqzWqATZsQodMzA3BkW70MK1/view?usp=sharing)
App demo video: [Youtube](https://youtu.be/ZDzRD2feEUE)
## Usage
### Installation
Clone repo
```
git clone https://github.com/ngfuong/vTLDR
cd vTLDR
```
Create virual environment and install requirements
```
python -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```
### App
Download checkpoint from [Drive](https://drive.google.com/drive/folders/1-f40PrWr3CahQbie-8F4N5WjrOUSYPfP?usp=sharing) and put into `training` folder.

Make sure `vncorenlp` folder have the `.jar` file and  its word segmentation component. You can download them as follow
```
mkdir -p vncorenlp/models/wordsegmenter
wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/VnCoreNLP-1.1.1.jar
wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/vi-vocab
wget https://raw.githubusercontent.com/vncorenlp/VnCoreNLP/master/models/wordsegmenter/wordsegmenter.rdr
mv VnCoreNLP-1.1.1.jar vncorenlp/ 
mv vi-vocab vncorenlp/models/wordsegmenter/
mv wordsegmenter.rdr vncorenlp/models/wordsegmenter/
```
To use app, launch
```
python app.py
```
Plain text or news URL (_tuoitre.vn_ domain) are supported as input.
### Training and Testing
For training, download Vietnews dataset
```
wget https://github.com/ThanhChinhBK/vietnews/archive/master.zip
unzip master.zip
```
Make sure the dataset is processed, refer to `data_preprocess.py`.
Train with default `config.yaml` file. Edit the file to change training configs.
```
python train.py
```
To test
```
python test.py
```

## References
1. Nguyen, Van-Hau & Nguyen, Thanh-Chinh & Nguyen, Minh-Tien & Hoai, Nguyen. (2019). VNDS: A Vietnamese Dataset for Summarization. 375-380. 10.1109/NICS48868.2019.9023886.
2. Rothe, Sascha & Narayan, Shashi & Severyn, Aliaksei. (2020). Leveraging Pre-trained Checkpoints for Sequence Generation Tasks. Transactions of the Association for Computational Linguistics. 8. 264-280. 10.1162/tacl_a_00313.
3. Nguyen, Dat Quoc & Nguyen, Anh. (2020). PhoBERT: Pre-trained language models for Vietnamese. 1037-1042. 10.18653/v1/2020.findings-emnlp.92.
4. ngockhanh5110, nlp-vietnamese-text-summarization, (2021), GitHub repository, https://github.com/ngockhanh5110/nlp-vietnamese-text-summarization
