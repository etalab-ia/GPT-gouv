# Utilisation de LLM sur Onyxia

## Utilisation de Falcon 40b Instruct en ligne de commande

Créer une machine avec le maximum de processeurs et 50Go de RAM.

```
cd ..
mc cp minio/projet-transformers/models/Falcon-40b-Instruct.ggmlv3.q4_0.bin .
sudo apt update
sudo apt install -y cmake htop
git clone https://github.com/jploski/ggml falcon-ggml
cd falcon-ggml
git checkout falcon40b
mkdir build && cd build && cmake .. && cmake --build . --config Release
bin/falcon -m ~/work/Falcon-40b-Instruct.ggmlv3.q4_0.bin -t 10 -n 200 -p "Décrit-moi un programme de la DiNUM visant à faire contribuer les datascientists de différentes administrations de l’état Français."
```

## Utilisation de LOLLMS-WebUI pour avoir une interface web de test

Créer une machine avec le maximum de processeurs et 50Go de RAM. Si vous souhaitez utiliser un petit modèle c'est possible de prendre une machine avec GPU.

Dans Networking activer l'option sur le port 9600.

```
cd ..
mkdir data
cd data
mc cp minio/projet-transformers/models/Falcon-40b-Instruct.ggmlv3.q4_0.bin .
cd ..
git clone https://github.com/ParisNeo/lollms-webui.git
cd lollms-webui
```
Dans `config.yaml` changer `localhost` par `0.0.0.0` (=> Ca n'a pas l'air de fonctionner !)

Lancer le script d'initialisation:
```
./webui.sh
```
Suivre les instructions.
Choisir _7 -  C Transformer (by marella)_ comme binding car c'est lui qui permet de charger Falcon-40B.

Donner le chemin `/home/onyxia/data/models/c_transformers/Falcon-40b-Instruct.ggmlv3.q4_0.bin` pour le model.

Finir par Ctrl+C car le binding réseau n'est pas bon.

```
cd
cp Falcon-40b-Instruct.ggmlv3.q4_0.bin /home/onyxia/data/models/c_transformers/
```

Lancer avec le bon binding :
```
python app.py --host 0.0.0.0
```

Dans l'interface Onyxia il y a un deuxième lien dans le Readme qui vous amène sur l'interface.

Il faut penser à regarder le terminal car parfois le serveur pose des questions !
