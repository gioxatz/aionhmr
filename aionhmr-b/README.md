# AionHMR-b

This module implements **AionHMR-b**, a transformer-based framework for **age-inclusive 3D human mesh recovery** designed for **action-preserving anonymization**.

---

## ✨ Overview

AionHMR-b is a deep learning model that:

* Reconstructs 3D human meshes from images/videos
* Supports **adults, children, and infants**
* Enables **privacy-preserving anonymization pipelines**

---

## ⚙️ Setup

Make sure you installed root dependencies first.

Also, you should download the [SMPL](https://smplify.is.tue.mpg.de/) neutral model (`basicModel_neutral_lbs_10_207_0_v1.0.0.pkl`) and place it in `~/.cache/AionHMR/data/`.


---

## 📦 Pretrained Models

Download the pretrained checkpoint from [Google Drive](https://drive.google.com/file/d/1z6TjB9dGllUvpDvU75QGrQHRxe0-I9Zj/view?usp=sharing).

Place them in: `~/.cache/AionHMR/checkpoints/`

---

## 🚀 Demo

Run inference on images:

```
python demo/demo_image.py \
    --img_folder example_data/images \
    --out_folder demo_out \
    --batch_size 32 \
    --side_view \
    --full_frame \
    --save_mesh

```

---

## 🏋️ Training

### 1. Prepare Dataset

Download datasets and place them in ```aionhmr_training_data/``` folder:

* HMR2.0 Training Datasets: [Link](https://github.com/shubham-goel/4D-Humans) 
* AionHMR-b child-focused Dataset
  * Images: [SyRIP](https://github.com/ostadabbas/Infant-Pose-Estimation), [Relative Human](https://github.com/Arthur151/Relative_Human)
  * [Annotations](https://drive.google.com/drive/folders/1SFa3tjq4LxQtzbXMT8xbW0wpOBXcefJK?usp=sharing)

Expected structure:

```
aionhmr_training_data/
 ├── dataset_tars
 ├── cmu_mocap.npz
```

Note: You can change the path of the folder that you've downloaded the datasets here:
`src/configs/datasets_tar.yaml`

---

### 2. Train from Scratch

```bash
python train.py exp_name=aionhmr data=mix_all experiment=hmr_vit_transformer trainer=gpu launcher=local
```

---

### 3. Fine-Tuning

```bash
python finetune.py exp_name=aionhmr data=mix_all experiment=hmr_vit_transformer trainer=gpu launcher=local
```
Note: You can change the path of the checkpoint to fine-tune on this file: ```src/configs_hydra/train.yaml```.

Checkpoints and logs are saved to `logs/` by default. You can change it here: `src/configs_hydra/paths/default.yaml`.

---

## 📊 Evaluation

Download [evaluation metadata](https://drive.google.com/drive/folders/1TH09-x_tCC3ceMUzr0gAd_VvAvU7nMNq?usp=sharing), [ChildPlay images](https://www.idiap.ch/en/scientific-research/data/childplay-gaze) and HMR2.0 [evaluation metadata](https://github.com/shubham-goel/4D-Humans) and place them in ```evaluation_data/``` folder.

Evaluate a pretrained model:

```bash 
python eval.py --dataset SYRIP --task 2D
```

You can select different datasets and tasks to evaluate on.