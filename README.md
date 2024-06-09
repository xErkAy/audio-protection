# audio-protection

## How to use?
```sh
pip install -r requirements.txt
```

### Available params
```sh
--wav --person --passport --password
```
### Encode
```sh
python main.py encode --wav='test.wav' --person='Test Person' --passport='Test passport' --password='secure password'
```
### Decode
```sh
python main.py decode --wav='test.wav' --password='secure password'
```
