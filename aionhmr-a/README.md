# AionHMR-a

This module implements **AionHMR-a**, an optimization-based framework for **age-inclusive 3D human shape and pose estimation** from a single RGB image.

---

## ✨ Overview

AionHMR-a is an optimization-based method that:

* Reconstructs 3D human meshes from images/videos
* Supports **adults, children, and infants**

---

## ⚙️ Setup

Make sure you installed the root and additional dependencies.

---

## 📦 Models

Please follow the instructions and download the models from [SLAHMR](https://github.com/vye16/slahmr/).

Additionally, download the [SMIL (SMPL format) template](https://agora.is.tue.mpg.de/download.php) and place it in `_DATA/body_models/` folder.

---

## 🚀 Inference

Run inference on images or videos:

```
bash main.sh <DATA_ROOT>
```

The code expects that you have placed all the images for inference in the `<DATA_ROOT>/images/` folder.

By default the output and the logs are saved in `./outputs/` but you can change it in `src/confs/config.yaml` and `src/confs/init.yaml`.